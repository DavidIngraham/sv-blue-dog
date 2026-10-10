from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
VSP_ROOT=ROOT/'.tools/openvsp-3.54.0/OpenVSP-3.54.0-win64'

def load_vsp():
    for name in ['openvsp_config','openvsp']:
        sys.path.insert(0,str(VSP_ROOT/'python'/name))
    import openvsp_config
    openvsp_config._IGNORE_IMPORTS=True
    import openvsp as vsp
    vsp.SetVSPAEROPath(str(VSP_ROOT))
    return vsp

if __name__=='__main__':
    vsp=load_vsp()
    print(vsp.GetVSPVersion(),vsp.CheckForVSPAERO(str(VSP_ROOT)))
