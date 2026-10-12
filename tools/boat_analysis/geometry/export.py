"""Export the analysis volume meshes as named, outward-oriented GLB surfaces."""
from pathlib import Path
import json
import hashlib
import numpy as np
import trimesh
from .vessel import metrics,operating_envelope

COLORS={'hull':'#347ba8','wing':'#ead9a8','keel':'#21857d','rudder':'#df773b','ballast':'#576375'}
# Boat: X forward, Y lateral, Z up. glTF: Y up; retain a right-handed frame.
TO_GLTF=np.array([[1.,0.,0.],[0.,0.,1.],[0.,-1.,0.]])


def exterior(tetrahedra):
    t=np.asarray(tetrahedra,dtype=float)
    volume=np.abs(np.linalg.det(t[:,1:]-t[:,:1]))/6
    t=t[volume>max(1e-20,volume.max()*1e-12)]
    vertices,inverse=np.unique(np.round(t.reshape(-1,3),12),axis=0,return_inverse=True)
    indices=inverse.reshape(-1,4)
    faces=[]
    for opposite in range(4):
        f=indices[:,[i for i in range(4) if i!=opposite]].copy()
        a,b,c=vertices[f].transpose(1,0,2)
        inward=np.einsum('ij,ij->i',np.cross(b-a,c-a),vertices[indices[:,opposite]]-a)>0
        f[inward]=f[inward][:,[0,2,1]]
        faces.append(f)
    faces=np.concatenate(faces)
    _,first,counts=np.unique(np.sort(faces,axis=1),axis=0,return_index=True,return_counts=True)
    if np.any(counts>2):raise ValueError('Nonmanifold volume mesh')
    mesh=trimesh.Trimesh(vertices=vertices,faces=faces[first[counts==1]],process=False)
    if not mesh.is_watertight or not mesh.is_winding_consistent:raise ValueError('Open or inconsistent exterior')
    if not np.isclose(mesh.volume,metrics(t)[4],rtol=1e-8,atol=1e-12):raise ValueError('Export volume differs from analysis')
    return mesh


def material(mesh,name,color,alpha=1.):
    rgba=trimesh.visual.color.hex_to_rgba(color).astype(float)/255;rgba[3]=alpha
    mesh.visual=trimesh.visual.TextureVisuals(material=trimesh.visual.material.PBRMaterial(
        name=name,baseColorFactor=rgba,metallicFactor=0.,roughnessFactor=.75,
        alphaMode='BLEND' if alpha<1 else 'OPAQUE',doubleSided=True))
    return mesh


def export_candidate(model,design,destination,resolution=12,provenance=None):
    """Recompute the neutral pose with the same native mass/hydrostatic kernels."""
    from .hydro import equilibrium
    x=np.array([design[n] for n in model.c['designNames']])
    bodies,mass,_,_=model.configuration(x,0.,resolution=resolution)
    cg=np.array([mass['cgX'],mass['cgY'],mass['cgZ']])
    state=equilibrium(model.hydro,bodies,cg,mass['totalMass'],0.,0.,density=model.parameters[31])
    meshes={b.name:exterior(b.tetrahedra) for b in bodies}
    scene=trimesh.Scene()
    def add(mesh,name,color,alpha=1.):
        mesh=material(mesh.copy(),name,color,alpha)
        mesh.vertices=mesh.vertices@TO_GLTF.T
        scene.add_geometry(mesh,node_name=name,geom_name=name)
    for name,mesh in meshes.items():add(mesh,name,COLORS[name])
    length=design['length_m'];beam=design['beam_m'];h=state['waterline_m']
    water=trimesh.creation.box(extents=[length*1.25,max(beam*1.5,.8),.001])
    water.apply_translation([0,0,h]);add(water,'waterline','#82c7e3',.22)
    dot=trimesh.creation.icosphere(subdivisions=2,radius=.025);dot.apply_translation(cg)
    add(dot,'center-of-gravity','#ca2567')
    for name,pivot in [('wing',design['mast_x_fraction']*length),('rudder',-design['rudder_arm_fraction']*length)]:
        points=meshes[name].vertices
        radius=np.linalg.norm(points[:,:2]-[pivot,0],axis=1).max()
        ring=trimesh.creation.annulus(r_min=radius-.003,r_max=radius+.003,height=.003,sections=96)
        ring.apply_translation([pivot,0,points[:,2].min()])
        add(ring,name+'-sweep','#a653ad',.7)
    destination=Path(destination);destination.parent.mkdir(parents=True,exist_ok=True)
    scene.export(destination,file_type='glb')
    metadata={'design':design,'massKg':mass['totalMass'],'cgM':cg.tolist(),'waterlineM':h,
              'pose':'Upright, fixed zero pitch, neutral wing and rudder; heave balanced.',
              'units':'m','boatAxes':'X forward, Y lateral, Z up','glbAxes':'X forward, Y up, Z negative boat Y',
              'exporterSha256':hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),'geometryResolution':resolution,'envelope':operating_envelope(design,model.parameters[33],resolution),'provenance':provenance,'components':{n:{'volumeM3':float(m.volume),'boundsM':m.bounds.tolist()} for n,m in meshes.items()},
              'scope':'Analysis outer envelopes; not detailed manufacturing CAD. Equipment shapes and installation are not defined.'}
    destination.with_suffix('.json').write_text(json.dumps(metadata,indent=2)+'\n')
    return meshes,metadata
