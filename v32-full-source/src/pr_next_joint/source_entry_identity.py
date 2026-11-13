"""Compiler/native corroborated entry metadata, without rewriting original AST.

Old Solidity ASTs omit selectors and kind. A derived binding must join the
compiler ABI and a native full signature at the exact declaring source span.
"""
import json,posixpath
from .core import require,digest

def function_kind(node):
    if node.get('nodeType')!='FunctionDefinition':return node.get('kind')
    if node.get('kind') in ('function','constructor','fallback','receive'):return node['kind']
    if 'kind' in node:return 'unresolved_kind'
    if type(node.get('isConstructor')) is not bool:return 'unresolved_kind'
    if node['isConstructor']:return 'constructor'
    return 'function' if node.get('name') else 'fallback'

def function_mutability(node):
    value=node.get('stateMutability')
    if value in ('pure','view','payable','nonpayable'):return value
    if 'stateMutability' in node:return None
    if type(node.get('constant')) is bool and type(node.get('payable')) is bool:
        if node['constant'] and not node['payable']:return 'view'
        if not node['constant']:return 'payable' if node['payable'] else 'nonpayable'
    return None

def elementary_expression_name(node):
    value=node.get('typeName')
    if isinstance(value,str):return value
    return value.get('name','') if isinstance(value,dict) else ''

def builtin_call(node,lookup,names=('require','assert')):
    # A return without a value has expression=None and is not a call.
    if not isinstance(node,dict) or node.get('nodeType')!='FunctionCall':return False
    f=node.get('expression')
    if not isinstance(f,dict) or f.get('nodeType')!='Identifier':return False
    name=f.get('name');ref=f.get('referencedDeclaration')
    if name not in names:return False
    if type(ref) is not int or ref in lookup.nodes:return False
    # 0.4.x uses positive virtual declaration IDs. Modern compilers commonly
    # use negative ones. Compiler function type, not the display name, binds it.
    typ=f.get('typeDescriptions',{}).get('typeIdentifier','')
    aliases={'keccak256':('keccak256','sha3'),'sha3':('sha3','keccak256'),'selfdestruct':('selfdestruct','suicide'),'suicide':('suicide','selfdestruct')}
    return any(typ.startswith('t_function_'+kind+'_') for kind in aliases.get(name,(name,)))

def builtin_object(node,lookup,name):
    expected={'msg':'t_magic_message','block':'t_magic_block','tx':'t_magic_transaction'}.get(name)
    ref=node.get('referencedDeclaration')
    return bool(expected and node.get('nodeType')=='Identifier' and node.get('name')==name
        and type(ref) is int and ref not in lookup.nodes and node.get('typeDescriptions',{}).get('typeIdentifier')==expected)

def source_file(path):
    p=str(path or '').replace('\\','/')
    if not p or p.startswith('/') or ':' in p or '..' in p.split('/'):return None
    return posixpath.normpath(p)

def simple_type(node):
    if node.get('nodeType')!='ElementaryTypeName':return None
    name=node.get('name');return {'uint':'uint256','int':'int256','byte':'bytes1','address payable':'address'}.get(name,name)


def declared_type_pair(typ,lookup):
    """Display/native and ABI type from exact compiler AST declarations.

    Contract references are addresses in ABI. Enums use their compiler-sized
    integer. No conversion is inferred from a name or from a desired ABI.
    """
    basic=simple_type(typ)
    if basic:return basic,basic
    if typ.get('nodeType')=='ArrayTypeName':
        pair=declared_type_pair(typ.get('baseType',{}),lookup)
        if pair is None:return None
        length=typ.get('length')
        if length is None:suffix='[]'
        elif length.get('nodeType')=='Literal' and str(length.get('value','')).isdigit():
            suffix='['+str(int(length['value']))+']'
        else:return None
        return pair[0]+suffix,pair[1]+suffix
    if typ.get('nodeType')!='UserDefinedTypeName':return None
    decl=lookup.nodes.get(typ.get('referencedDeclaration'),{})
    if decl.get('nodeType')=='ContractDefinition' and decl.get('name'):
        return decl['name'],'address'
    if decl.get('nodeType')=='EnumDefinition':
        name=decl.get('canonicalName');count=len(decl.get('members',[]))
        if name and count:return name,'uint'+str(max(8,((count-1).bit_length()+7)//8*8))
    return None


def entry_functions(lookup):
    """ABI functions plus compiler-identified inherited special entrypoints."""
    result=list(lookup.contract['functions']);signatures={f['signature'] for f in result}
    for kind in ('fallback','receive'):
        signature=kind+'()'
        if signature in signatures:continue
        node=lookup.entry_identity.special(kind)
        if node:
            result.append({'signature':signature,'selector':None,'types':[],'outputs':[],
                'source_anchor':lookup.anchor(node),'special_kind':kind})
    return result

class EntryIdentity:
    def __init__(self,lookup):
        self.lookup=lookup;self.records={};self._selectors={};self.dispatch_proofs={}
    def anchor(self,node):return self.lookup.anchor(node)
    def native(self,node):
        anchor=self.anchor(node);scope=self.lookup.nodes.get(node.get('scope'),{})
        matched=[f for f in self.lookup.bundle.get('native_ir',{}).get('functions',[]) if
            f.get('contract')==scope.get('name') and source_file(f.get('source',{}).get('file'))==source_file(anchor['file'])
            and source_file(anchor['file']) is not None
            and f.get('source',{}).get('start')==anchor['start'] and f.get('source',{}).get('length')==anchor['length']]
        # Preserve native source-span identity; canonicalize only types proved
        # by the declaration at that exact span (contract/enum/typed arrays).
        pairs=[declared_type_pair(p.get('typeName',{}),self.lookup)
               for p in node.get('parameters',{}).get('parameters',[])]
        if any(p is None for p in pairs):return matched
        display=node.get('name','')+'('+','.join(p[0] for p in pairs)+')'
        canonical=node.get('name','')+'('+','.join(p[1] for p in pairs)+')'
        return [{**f,'signature':canonical,'source_native_signature':f['signature'],
                 'signature_basis':'exact_source_AST_declared_ABI_type'}
                if display!=canonical and f.get('signature')==display else f for f in matched]
    def declared_contract(self,node):
        decl=self.lookup.nodes.get(node.get('scope'),{});anchor=self.anchor(decl) if decl.get('src') else {}
        matches=[c for c in self.lookup.bundle['contracts'] if c['name']==decl.get('name') and c['file']==anchor.get('file')]
        return matches[0] if len(matches)==1 else None
    def selector(self,node):
        original=node.get('functionSelector')
        if original is not None:
            signatures={n.get('signature') for n in self.native(node)}
            if signatures:
                require(len(signatures)==1,'entry_native_signature_ambiguous')
                matches={f['selector'] for c in self.lookup.bundle['contracts'] for f in c['functions'] if f['signature'] in signatures}
                require(not matches or matches=={original},'entry_native_selector_conflict')
            return original
        if node.get('id') in self._selectors:return self._selectors[node['id']]
        if function_kind(node)!='function':return None
        native=self.native(node);signatures={n.get('signature') for n in native}
        if len(signatures)!=1:return None
        sig=next(iter(signatures))
        # Abstract declarations need not have deployable bytecode. The ABI
        # mapping is signature-wide; entry ownership is checked separately by C3.
        matches={f['selector'] for c in self.lookup.bundle['contracts'] for f in c['functions'] if f['signature']==sig}
        if len(matches)!=1:return None
        value=next(iter(matches))
        self._selectors[node['id']]=value
        self.record(node,sig,value,'compiler_ABI_native_exact_source')
        return value
    def record(self,node,signature,selector,basis):
        anchor=self.anchor(node);bundle=self.lookup.bundle
        hashes={r.get('source_anchor',{}).get('sha256') for r in bundle.get('functions',[])+bundle.get('state_declarations',[]) if r.get('source_anchor',{}).get('file')==anchor['file'] and r.get('source_anchor',{}).get('sha256')}
        self.records[str(node['id'])+':'+signature]={'program_id':bundle['program_id'],'build_id':bundle['build_id'],
            'target':self.lookup.contract['file']+':'+self.lookup.contract['name'],'signature':signature,'selector':selector,
            'ast_id':node['id'],'declaring_scope':node.get('scope'),'source':anchor,'kind':function_kind(node),
            'original_selector':node.get('functionSelector'),'original_kind':node.get('kind'),'basis':basis,
            'ast_source_sha256':digest(bundle['ast_sources'][anchor['file']]),'native_sha256':bundle.get('native_ir',{}).get('sha256'),
            'source_sha256':next(iter(hashes)) if len(hashes)==1 else None,
            'native_matches':[{'signature':n['signature'],'source':n['source'],'contract':n['contract']} for n in self.native(node)]}
        proof=self.dispatch_proofs.get(str(node['id'])+':'+signature)
        if proof:self.records[str(node['id'])+':'+signature]['dispatch_proof']=proof
    def select_entry(self,candidates,order,sig,selector):
        for scope in order:
            matches=list({n['id']:n for n in candidates if n.get('scope')==scope}.values())
            if not matches:continue
            if len(matches)==1:return matches[0]
            # Only resolve an actual same-scope function/getter ambiguity, using
            # validated compiler dispatcher-to-source correspondence.
            p=self.lookup;target=p.contract['file']+':'+p.contract['name']
            from .compiler_entry_evidence import CompilerEntryEvidence
            table=p.bundle.get('_compiler_entry_evidence',{})
            proof=table.get(target,{}) if isinstance(table,CompilerEntryEvidence) else {}
            branch=proof.get('branches',{}).get(selector)
            types={n.get('nodeType') for n in matches}
            valid=proof.get('program_id')==p.bundle['program_id'] and proof.get('build_id')==p.bundle['build_id']
            if len(matches)==2 and types=={'FunctionDefinition','VariableDeclaration'} and valid and branch:
                selected=[n for n in matches if tuple(map(int,n['src'].split(':')))==
                    (branch['source_start'],branch['source_length'],branch['source_file_id'])]
                if len(selected)==1:
                    chosen=selected[0]
                    self.dispatch_proofs[str(chosen['id'])+':'+sig]={k:v for k,v in proof.items() if k!='branches'}|{'selector':selector,**branch}
                    return chosen
            require(False,'entry_same_scope_ambiguous:'+sig)
        return None
    def select(self,candidates,order,reason):
        if not candidates:return None
        for scope in order:
            matches=[n for n in candidates if n.get('scope')==scope]
            if matches:
                require(len(matches)==1,reason)
                return matches[0]
        return None
    def getter_shape(self,node,abi):
        if node.get('stateVariable') is not True or node.get('visibility')!='public':return False
        if node.get('functionSelector') is not None:return node['functionSelector']==abi['selector']
        args=[];typ=node.get('typeName',{})
        while typ.get('nodeType') in ('Mapping','ArrayTypeName'):
            if typ['nodeType']=='Mapping':
                pair=declared_type_pair(typ.get('keyType',{}),self.lookup)
                if pair is None:return False
                args.append(pair[1]);typ=typ.get('valueType',{})
            else:args.append('uint256');typ=typ.get('baseType',{})
        pair=declared_type_pair(typ,self.lookup)
        outputs=[pair[1]] if pair else None
        if typ.get('nodeType')=='UserDefinedTypeName':
            decl=self.lookup.nodes.get(typ.get('referencedDeclaration'),{})
            if decl.get('nodeType')=='StructDefinition':
                members=[m.get('typeName',{}) for m in decl.get('members',[]) if m.get('typeName',{}).get('nodeType') not in ('Mapping','ArrayTypeName')]
                pairs=[declared_type_pair(m,self.lookup) for m in members]
                if pairs and all(pairs):outputs=[p[1] for p in pairs]
        return bool(outputs and abi['signature']==node['name']+'('+','.join(args)+')' and abi['types']==args and abi['outputs']==outputs)
    def special(self,kind):
        p=self.lookup;order=p.contract_node.get('linearizedBaseContracts',[p.contract_node['id']])
        nodes=[n for n in p.implementations if function_kind(n)==kind]
        return self.select(nodes,order,'special_entry_ambiguous:'+kind)
    def function(self,sig):
        p=self.lookup;order=p.contract_node.get('linearizedBaseContracts',[p.contract_node['id']])
        if sig not in p.abi and sig in ('fallback','fallback()','()','receive','receive()'):
            kind='receive' if sig.startswith('receive') else 'fallback';node=self.special(kind)
            require(node is not None,'special_entry_not_found:'+kind)
            self.record(node,kind+'()',None,'compiler_special_kind_and_inheritance')
            return node
        if sig=='constructor':
            fs=[n for n in p.implementations if function_kind(n)=='constructor' and n.get('scope')==p.contract_node['id']]
            require(len(fs)<=1,'constructor_ast_ambiguous')
            if fs:self.record(fs[0],sig,None,'compiler_kind_or_legacy_isConstructor')
            return fs[0] if fs else None
        abi=p.abi[sig];selector=abi['selector']
        require(len({f['signature'] for f in p.contract['functions'] if f['selector']==selector})==1,'entry_selector_collision')
        candidates=[];ambiguous=[]
        for node in p.implementations:
            if function_kind(node)!='function' or node.get('visibility') not in ('public','external'):continue
            original=node.get('functionSelector')
            if original is not None:
                if self.selector(node)==selector:
                    signatures={n.get('signature') for n in self.native(node)}
                    require(not signatures or signatures=={sig},'entry_native_signature_conflict:'+sig)
                    candidates.append(node)
                continue
            native=self.native(node);signatures={n.get('signature') for n in native}
            if sig in signatures:
                if len(signatures)!=1:ambiguous.append(node)
                elif self.selector(node)==selector:candidates.append(node)
        require(not ambiguous,'legacy_entry_native_signature_ambiguous:'+sig)
        getters=[n for n in p.decls.values() if n.get('scope') in order and self.getter_shape(n,abi)]
        chosen=self.select_entry(candidates+getters,order,sig,selector)
        if chosen:
            if chosen.get('nodeType')=='VariableDeclaration':
                self.record(chosen,sig,selector,'compiler_public_getter_shape')
                return {'generated_getter':chosen}
            self.record(chosen,sig,selector,'compiler_selector' if chosen.get('functionSelector') is not None else 'compiler_ABI_native_exact_source')
            return chosen
        same_name=[n for n in p.implementations if function_kind(n)=='function' and n.get('name')==sig.split('(')[0]]
        require(not same_name,'implemented_entry_identity_unresolved:'+sig)
        require(False,'missing_implemented_entry:'+sig)
