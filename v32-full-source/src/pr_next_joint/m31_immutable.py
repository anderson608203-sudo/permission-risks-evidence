"""Enrich an old compiler artifact only from identical creation code, runtime and complete metadata."""
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

from .facts import walk


def restore(bundle, standard, original):
    if not any(n.get("mutability")=="immutable" for a in bundle.get("ast_sources",{}).values() for n in walk(a)):
        return None
    rows=[c for c in bundle["contracts"] if c.get("runtime") and not c.get("immutable_references")]
    if not rows:
        return None
    trusted=os.environ.get("PRNEXT_IMMUTABLE_SOLC_DIR")
    record={"state":"not_reconstructed","invocations":0,"targets":[]}
    if not trusted:
        return {**record,"reason":"local_trusted_compiler_directory_not_configured"}
    version=(rows[0].get("metadata") or {}).get("compiler",{}).get("version","")
    if not re.fullmatch(r"\d+\.\d+\.\d+\+commit\.[0-9A-Fa-f]{8}",version):
        return {**record,"reason":"full_compiler_version_not_available"}
    root=Path(trusted).resolve()
    names=("solc-windows-amd64-v"+version+".exe","solc-linux-amd64-v"+version,"solc-"+version.split("+")[0])
    compiler=next((root/n for n in names if (root/n).is_file() and (root/n).resolve().parent==root),None)
    if not compiler:
        return {**record,"reason":"matching_compiler_not_installed"}
    source=copy.deepcopy(standard)
    selection=source["settings"].setdefault("outputSelection",{}).setdefault("*",{}).setdefault("*",[])
    for key in ("evm.bytecode.object","evm.deployedBytecode.object","metadata","evm.deployedBytecode.immutableReferences"):
        if key not in selection:selection.append(key)
    record["invocations"]=1
    try:
        run=subprocess.run([str(compiler),"--standard-json"],input=json.dumps(source).encode(),capture_output=True,timeout=60,check=True)
        generated=json.loads(run.stdout)["contracts"]
        certificate=hashlib.sha256(compiler.read_bytes()).hexdigest()
        for c in rows:
            old=original["contracts"][c["file"]][c["name"]]
            new=generated[c["file"]][c["name"]]
            if new["metadata"]!=old["metadata"] or any(new["evm"][k]["object"]!=old["evm"][k]["object"] for k in ("bytecode","deployedBytecode")):
                continue
            ranges=new["evm"]["deployedBytecode"].get("immutableReferences",{})
            if ranges and all(isinstance(p.get("start"),int) and isinstance(p.get("length"),int)
                         and 0 <= p["start"] < p["start"]+p["length"] <= len(c["runtime"])//2 for v in ranges.values() for p in v):
                c["immutable_references"]=ranges
                record["targets"].append({"target":c["file"]+":"+c["name"],"locations":ranges})
        return {**record,"state":"certified" if record["targets"] else "no_matching_ranges",
                "compiler":version,"compiler_binary_sha256":certificate}
    except (OSError,subprocess.SubprocessError,ValueError,KeyError) as error:
        return {**record,"reason":"local_reconstruction_unavailable","exception":type(error).__name__}

