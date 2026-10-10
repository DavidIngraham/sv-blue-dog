"""Inspect original STEP geometry without relying on SolidWorks session state."""
import json
from pathlib import Path
from OCP.STEPControl import STEPControl_Reader
from OCP.IFSelect import IFSelect_RetDone
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_SOLID

ROOT=Path(__file__).resolve().parents[2]

def load_shape(path):
    reader=STEPControl_Reader()
    if reader.ReadFile(str(path)) != IFSelect_RetDone:
        raise ValueError('Cannot read STEP')
    reader.TransferRoots()
    return reader.OneShape()

def properties(shape):
    box=Bnd_Box();BRepBndLib.AddOptimal_s(shape,box)
    volume=GProp_GProps();BRepGProp.VolumeProperties_s(shape,volume)
    surface=GProp_GProps();BRepGProp.SurfaceProperties_s(shape,surface)
    c=volume.CentreOfMass()
    return {'bounds_mm':list(box.Get()),'signed_volume_mm3':volume.Mass(),'surface_mm2':surface.Mass(),'volume_centroid_mm':[c.X(),c.Y(),c.Z()]}

if __name__=='__main__':
    path=ROOT/'cad/SweptCrescentWing.STEP';shape=load_shape(path)
    solids=[];it=TopExp_Explorer(shape,TopAbs_SOLID)
    while it.More():
        solids.append(properties(it.Current()));it.Next()
    print(json.dumps({'source':str(path.relative_to(ROOT)),'overall':properties(shape),'solids':solids},indent=2))
