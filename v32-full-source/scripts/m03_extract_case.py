"""One original solc invocation, retained-output native facts, no program run."""
import argparse,copy,hashlib,json,os,pathlib,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from pr_next_joint.core import digest,require
from pr_next_joint.facts import build_bundle

def save(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def source_paths(standard,root):
    """Check every path before writing any materialized source."""
    items=[]
    for name,item in standard['sources'].items():
        require(isinstance(name,str) and '\\' not in name and ':' not in name,'source_path_format')
        relative=pathlib.PurePosixPath(name)
        require(not relative.is_absolute() and '..' not in relative.parts,'source_path_scope')
        path=(root/name).resolve()
        require(path.is_relative_to(root.resolve()),'source_path_scope')
        require(isinstance(item.get('content'),str),'inline_source_content_required')
        items.append((path,item['content'].encode('utf-8')))
    require(bool(items),'sources_required')
    return items

def extract_retained(standard,compiled,bundle,receipt,work):
    # Same retained-output adapter as c2_static_remote, without running C2.
    # These imports must not require the Linux packages merely to inspect CLI.
    from crytic_compile import CryticCompile
    from crytic_compile.compilation_unit import CompilationUnit
    from crytic_compile.compiler.compiler import CompilerVersion
    from crytic_compile.platform.solc_standard_json import SolcStandardJson,parse_standard_json_output
    from slither.slither import Slither
    from pr_next_joint.native_facts import extract
    class RetainedOutput(SolcStandardJson):
        def compile(self,crytic_compile,**kwargs):
            unit=CompilationUnit(crytic_compile,'m03_retained_output')
            optimizer=standard['settings'].get('optimizer',{})
            unit.compiler_version=CompilerVersion(compiler='solc',version=receipt['compiler_version'],
                optimized=optimizer.get('enabled',False),optimize_runs=optimizer.get('runs'))
            parse_standard_json_output(compiled,unit,solc_working_dir=str(work))
    previous=pathlib.Path.cwd()
    try:
        os.chdir(work)
        return extract(Slither(CryticCompile(RetainedOutput(copy.deepcopy(standard)),cwd=str(work))),bundle,copy.deepcopy(receipt))
    finally:os.chdir(previous)

def run(standard_input,compiler,output,group,expected_version='0.8.20',runner=None,native_loader=None):
    src=pathlib.Path(standard_input).resolve();compiler=pathlib.Path(compiler).resolve()
    out=pathlib.Path(output).resolve();out.mkdir(parents=True,exist_ok=False)
    receipt={'group':group,'status':'started','compiler_path':str(compiler),
             'compiler_invocations':0,'native_extractions':0,'program_execution':False,
             'input_material_origin':'compiler_artifacts',
             'build_comparison':'same output supplied to build_bundle; no independent frozen-version comparison'}
    def streams(stdout,stderr):
        for name,value in [('compiler.stdout',stdout),('compiler.stderr',stderr)]:
            if isinstance(value,bytes):value=value.decode('utf-8',errors='replace')
            (out/name).write_text(value or '',encoding='utf-8')
    try:
        raw=src.read_bytes();standard=json.loads(raw.decode('utf-8-sig'))
        work=out/'sources';paths=source_paths(standard,work)
        receipt.update(compiler_binary_sha256=hashlib.sha256(compiler.read_bytes()).hexdigest(),
            standard_input_sha256=hashlib.sha256(raw).hexdigest(),standard_input_digest=digest(standard))
        (out/'standard-input.json').write_bytes(raw)
        for path,content in paths:
            path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(content)
        receipt['compiler_invocations']=1;save(out/'extract_receipt.json',receipt)
        try:
            process=(runner or subprocess.run)([str(compiler),'--standard-json'],input=json.dumps(standard,ensure_ascii=False),
                capture_output=True,text=True,encoding='utf-8',cwd=work,timeout=120)
        except subprocess.TimeoutExpired as error:
            streams(error.stdout,error.stderr);raise
        streams(process.stdout,process.stderr)
        receipt['compiler_exit_code']=process.returncode
        compiled=None
        try:compiled=json.loads(process.stdout)
        except (ValueError,TypeError):pass
        if isinstance(compiled,dict):save(out/'standard-output.json',compiled)
        require(process.returncode==0,'compiler_exit:'+str(process.returncode))
        require(isinstance(compiled,dict),'compiler_output_not_json')
        errors=[e for e in compiled.get('errors',[]) if e.get('severity')=='error']
        receipt['errors']=errors;require(not errors,'compile_errors')
        versions={json.loads(c['metadata'])['compiler']['version'].split('+')[0]
                  for contracts in compiled['contracts'].values() for c in contracts.values() if c.get('metadata')}
        require(versions=={expected_version},'compiler_metadata_version_mismatch')
        receipt['compiler_version']=expected_version
        receipt['standard_output_sha256']=hashlib.sha256((out/'standard-output.json').read_bytes()).hexdigest()
        bundle=build_bundle(group,standard,compiled,compiled,receipt)
        bundle['ast_sources']={f:x['ast'] for f,x in compiled['sources'].items()}
        native=(native_loader or extract_retained)(standard,compiled,bundle,receipt,work)
        require(all(native.get(k)==bundle[k] for k in ['program_id','build_id']),'native_identity_mismatch')
        bundle['native_ir']={'sha256':digest(native),'functions':[{k:v for k,v in f.items() if k!='nodes'} for f in native['functions']],
            'ssa_operation_count':native.get('ssa_operation_count'),'slither_version':native.get('slither')}
        bundle['coverage']['slither_fresh']='executed_from_retained_original_compiler_output'
        bundle['material_origin']='compiler_artifacts'
        receipt.update(status='compiled_and_extracted',native_extractions=1,native_sha256=digest(native),
            program_id=bundle['program_id'],build_id=bundle['build_id'],native_adapter='retained_original_output')
        save(out/'ProgramBundle.json',bundle);save(out/'native_ssa.json',native)
        save(out/'extract_receipt.json',receipt)
        return {'status':receipt['status'],'program_id':bundle['program_id'],'build_id':bundle['build_id']}
    except Exception as error:
        receipt.update(status='timeout' if isinstance(error,subprocess.TimeoutExpired) else 'failed',
            error_class=type(error).__name__,error=str(error),no_safety_conclusion=True)
        save(out/'extract_receipt.json',receipt)
        raise

def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument('--standard-input',required=True);p.add_argument('--compiler',required=True)
    p.add_argument('--out',required=True);p.add_argument('--group',required=True)
    p.add_argument('--compiler-version',default='0.8.20')
    a=p.parse_args(argv)
    result=run(a.standard_input,a.compiler,a.out,a.group,a.compiler_version)
    print(json.dumps(result));return result

if __name__=='__main__':main()
