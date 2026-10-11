"""Capture archived OpenVSP geometry; run in the isolated VSP environment.

The oblique image rotates the display geometry only; the saved model is unchanged.
"""
def main():
    import sys,threading,time,os
    from tools.boat_analysis.aerodynamics.vsp.vsp_runtime import VSP_ROOT,ROOT,load_vsp
    sys.path.insert(0,str(VSP_ROOT/'python/openvsp_config'))
    import openvsp_config
    openvsp_config.LOAD_GRAPHICS=True
    v=load_vsp()
    def capture():
        time.sleep(3)
        v.Lock()
        v.ReadVSPFile(str(ROOT/'evidence/vsp-geometry/reference-64.vsp3'))
        v.SetBackground(1.,1.,1.)
        v.SetShowBorders(False)
        for geom in v.FindGeoms(): v.SetGeomDrawType(geom,v.GEOM_DRAW_SHADE)
        v.Update();v.UpdateGUI();v.FitAllViews()
        out=ROOT/'evidence/vsp-geometry';out.mkdir(exist_ok=True)
        v.ScreenGrab(str(out/'reference-planform.png'),1400,900,False)
        for geom in v.FindGeoms():
            v.SetParmVal(geom,'X_Rel_Rotation','XForm',35)
            v.SetParmVal(geom,'Z_Rel_Rotation','XForm',-35)
        v.Update();v.UpdateGUI();v.FitAllViews()
        v.ScreenGrab(str(out/'reference-perspective.png'),1400,900,False)
        v.Unlock()
        assert all((out/n).is_file() for n in ['reference-perspective.png','reference-planform.png'])
        print('capture complete',flush=True)
        os._exit(0)
    threading.Thread(target=capture,daemon=True).start()
    v.StartGUI()


if __name__ == "__main__":
    main()
