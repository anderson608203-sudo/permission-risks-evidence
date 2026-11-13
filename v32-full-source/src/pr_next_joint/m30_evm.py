"""Concrete differential execution on the original compiler bytecode. No RPC or state overrides."""
import hashlib
import json
import re


class Unavailable(Exception):
    """The selected environment or operation cannot support a trustworthy witness."""


def argument(kind, address, number=1):
    if kind == "address":
        return address
    if kind == "bool":
        return bool(number)
    if re.fullmatch(r"u?int(?:\d+)?", kind):
        return number
    if kind == "string":
        return "local"
    if kind == "bytes":
        return b""
    if re.fullmatch(r"bytes(?:[1-9]|[12][0-9]|3[012])", kind):
        return bytes(int(kind[5:]))
    raise Unavailable("constructor_or_operation_argument_type_outside_bound:" + kind)


def environment(contract):
    from eth.vm import forks
    named = {"homestead":"HomesteadVM","tangerineWhistle":"TangerineWhistleVM",
        "spuriousDragon":"SpuriousDragonVM", "byzantium":"ByzantiumVM","constantinople":"ConstantinopleVM",
        "petersburg":"PetersburgVM","istanbul":"IstanbulVM","berlin":"BerlinVM","london":"LondonVM",
        "paris":"ParisVM","shanghai":"ShanghaiVM","cancun":"CancunVM","prague":"PragueVM"}
    meta = contract.get("metadata") or {}
    if isinstance(meta, str):
        try:
            meta = json.loads(meta)
        except ValueError as e:
            raise Unavailable("compiler_metadata_unreadable") from e
    name = meta.get("settings", {}).get("evmVersion")
    if not name:
        raise Unavailable("compiler_execution_fork_unspecified")
    if name not in named:
        raise Unavailable("compiler_execution_fork_unsupported:" + str(name))
    return name, getattr(forks, named[name])


class World:
    """Each branch starts at a persisted root. Queries use real signed transactions at fixed block context."""
    def __init__(self, contract):
        from eth.chains.base import MiningChain
        from eth.db.atomic import AtomicDB
        from eth_keys import keys
        from eth_abi import encode
        from eth._utils.address import generate_contract_address

        self.encode = encode
        self.name, vm_class = environment(contract)
        self.contract = contract
        self.funcs = {f["signature"]: f for f in contract["functions"]}
        self.receives_empty = any(entry.get("type")=="receive" for entry in contract.get("abi",[]))
        if any(not isinstance(contract.get(k),str) or not re.fullmatch(r"(?:[0-9a-fA-F]{2})+",contract[k])
               for k in ("creation","runtime")):
            raise Unavailable("missing_or_unlinked_bytecode")
        self.keys = [keys.PrivateKey(i.to_bytes(32,"big")) for i in range(21,26)]
        self.actors = [k.public_key.to_canonical_address() for k in self.keys]
        self.admin, self.user, self.recipient, self.delegate, self.other = self.actors
        cls = MiningChain.configure(__name__="PermissionLocalWitness", vm_configuration=((0,vm_class),), chain_id=1337)
        genesis = {"difficulty":0 if self.name in ("paris","shanghai","cancun","prague") else 1,
                   "gas_limit":30000000,"timestamp":1704067200}
        if self.name in ("london","paris","shanghai","cancun","prague"):
            genesis["base_fee_per_gas"] = 0
        accounts = {a:{"balance":10**23,"code":b"","nonce":0,"storage":{}} for a in self.actors}
        self.chain = cls.from_genesis(AtomicDB(),genesis,accounts)
        self.header = self.chain.get_canonical_head()
        self.vm = self.chain.get_vm(self.header)
        self.log = []
        self.address = generate_contract_address(self.admin, 0)
        args = [argument(t,self.admin,32) for t in contract["constructor_types"]]
        data = bytes.fromhex(contract["creation"]) + encode(contract["constructor_types"],args)
        self.creation_sha256 = hashlib.sha256(bytes.fromhex(contract["creation"])).hexdigest()
        self.constructor_arguments = self.encode(contract["constructor_types"],args).hex()
        # Avoid writing the entire creation bytecode to every finding.
        deployed = self.tx(self.admin,b"",data,0,"<deployment>",gas=6000000)
        if not deployed["ok"] or not self.state.get_code(self.address):
            raise Unavailable("deployment_failed_with_disclosed_constructor_arguments")
        actual = bytes(self.state.get_code(self.address))
        expected = bytes.fromhex(contract["runtime"])
        if actual != expected:
            # Compiler-declared immutable slots may be initialized by initcode.
            masked = bytearray(actual)
            if len(actual) != len(expected):
                raise Unavailable("deployed_runtime_length_mismatch")
            for sites in (contract.get("immutable_references") or {}).values():
                for site in sites:
                    a,b=site["start"],site["start"]+site["length"]
                    masked[a:b]=expected[a:b]
            if bytes(masked) != expected:
                raise Unavailable("deployed_runtime_identity_mismatch")
        self.runtime_sha256=hashlib.sha256(actual).hexdigest()
        self.origin = self.snapshot()

    @property
    def state(self):
        return self.vm.state

    def snapshot(self):
        self.state.persist()
        return self.state.state_root, list(self.log)

    def restore(self, snapshot):
        root, log = snapshot
        self.vm = self.chain.get_vm(self.header.copy(state_root=root))
        self.log = list(log)

    def tx(self, actor, target, data, value, fn, gas=650000):
        from eth_utils.exceptions import ValidationError
        from eth.exceptions import VMError
        unsigned = self.vm.create_unsigned_transaction(nonce=self.state.get_nonce(actor),gas_price=1,gas=gas,
                                                       to=target,value=value,data=data)
        signed = unsigned.as_signed_transaction(self.keys[self.actors.index(actor)])
        touched={}
        state=self.state
        state.lock_changes()
        write=state.set_storage
        def observe_write(address,slot,value):
            cell=(address,slot)
            if cell not in touched:
                touched[cell]=state.get_storage(address,slot)
            return write(address,slot,value)
        state.set_storage=observe_write
        try:
            result = self.state.apply_transaction(signed)
        except (ValidationError, VMError) as e:
            raise Unavailable("transaction_environment_rejected:" + type(e).__name__) from e
        finally:
            del state.set_storage
        children=list(result.children)
        external=[]
        while children:
            child=children.pop()
            addr=child.msg.code_address
            if (child.msg.data and addr and not child.msg.is_create and not child.msg.code
                    and int.from_bytes(addr,"big")>10):
                raise Unavailable("external_implementation_missing_at_called_address")
            external.append({"to":child.msg.storage_address.hex(),"value":child.msg.value,"data_bytes":len(child.msg.data),
                             "code_bytes":len(child.msg.code),"success":not child.is_error})
            children.extend(child.children)
        receipt={"operation":fn,"actor":actor.hex(),"input":data.hex() if target else "see_creation_and_constructor_arguments",
                 "value":value,"ok":not result.is_error,"gas_used":result.get_gas_used(),
                 "output":result.output.hex()[:256],"error":type(result.error).__name__ if result.is_error else None,
                 "beneficiaries":[a.hex() for a in sorted(result.get_self_destruct_beneficiaries())],"nested_calls":external,
                 "changed_slots":[[a.hex(),hex(slot),hex(before),hex(state.get_storage(a,slot))]
                       for (a,slot),before in touched.items() if state.get_storage(a,slot)!=before]}
        self.log.append(receipt)
        return receipt

    def arguments(self, fn, address, number=1):
        if fn in ("receive()","fallback()"):
            return []
        entry=self.funcs.get(fn)
        if not entry:
            raise Unavailable("ABI_entry_missing")
        return [argument(t,address,number) for t in entry["types"]]

    def call(self, fn, actor, args=None, *, address=None, number=1, value=0):
        from eth_abi.exceptions import EncodingError
        if not self.state.get_code(self.address):
            raise Unavailable("target_has_no_runtime_code")
        if fn == "fallback()" or fn == "receive()":
            # Empty calldata would dispatch receive() first if it exists.
            data = b"\xff\xff\xff\xff" if fn == "fallback()" and self.receives_empty else b""
            if data and any((f.get("selector") or "").removeprefix("0x")==data.hex() for f in self.funcs.values()):
                raise Unavailable("fallback_probe_selector_collision")
        else:
            f=self.funcs.get(fn)
            if not f or not f.get("selector"):
                raise Unavailable("ABI_entry_missing")
            if args is None: args=self.arguments(fn,address or actor,number)
            if len(f["types"])!=len(args):
                raise Unavailable("arguments_do_not_match_observable_declaration")
            try:
                data=bytes.fromhex(f["selector"].removeprefix("0x"))+self.encode(f["types"],args)
            except EncodingError as e:
                raise Unavailable("arguments_outside_declared_ABI_types") from e
        return self.tx(actor,self.address,data,value,fn)

    def read(self, fn, *args):
        """An independent eth_call-style read; storage and caller nonce are restored."""
        before=self.snapshot()
        try:
            receipt=self.call(fn,self.other,list(args))
            if not receipt["ok"] or len(receipt["output"])!=64:
                raise Unavailable("observable_getter_unavailable")
            return int(receipt["output"],16)
        finally:
            self.restore(before)

    def unique_getter_slot(self, fn, *args):
        before=self.snapshot()
        state=self.state
        original=state.get_storage
        observed=set()
        def record(address,slot,*a,**kw):
            observed.add((address.hex(),hex(slot)))
            return original(address,slot,*a,**kw)
        state.get_storage=record
        try:
            receipt=self.call(fn,self.other,list(args))
            if not receipt["ok"] or len(receipt["output"])!=64 or len(observed)!=1:
                raise Unavailable("getter_does_not_isolate_one_storage_cell")
            return next(iter(observed))
        finally:
            del state.get_storage
            self.restore(before)

    def proof(self):
        return {"backend":"py-evm-0.12.1b1","evm_fork":self.name,"fork_basis":"compiler target; conditional local experiment",
                "block_number":0,"timestamp":1704067200,"creation_sha256":self.creation_sha256,
                "deployed_runtime_sha256":self.runtime_sha256,"encoded_constructor_arguments":self.constructor_arguments,
                "externally_funded_accounts":[a.hex() for a in self.actors],"initial_eoa_balance":10**23,
                "contract_storage_injected":False,"contract_funds_injected":False}

