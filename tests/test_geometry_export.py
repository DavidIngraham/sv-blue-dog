"""Check export geometry independently of the browser renderer."""
import numpy as np
import pytest
import trimesh
from tools.boat_analysis.geometry.export import exterior,TO_GLTF


def test_tetrahedron_exterior_is_closed_outward_and_volume_preserving():
    t=np.array([[[0,0,0],[2,0,0],[0,3,0],[0,0,4]]],dtype=float)
    for order in ([0,1,2,3],[3,1,2,0]):
        mesh=exterior(t[:,order])
        assert mesh.is_watertight and mesh.is_winding_consistent
        assert mesh.volume==pytest.approx(4.)
        assert np.allclose(mesh.bounds,[[0,0,0],[2,3,4]])


def test_shared_internal_face_is_removed():
    t=np.array([[[0,0,0],[1,0,0],[0,1,0],[0,0,1]],[[0,0,0],[1,0,0],[0,1,0],[0,0,-1]]],float)
    mesh=exterior(t)
    assert len(mesh.faces)==6
    assert mesh.volume==pytest.approx(1/3)
    assert np.linalg.det(TO_GLTF)==pytest.approx(1)


def test_candidate_glb_matches_analysis_volumes_and_dimensions(tmp_path):
    import sys
    if sys.platform!='linux':pytest.skip('Native hydrostatic kernel requires Linux')
    from tools.publishing.concepts import render
    entries=render(tmp_path)
    assert [r['design']['length_m'] for r in entries]==pytest.approx([2,1.4])
    for entry in entries:
        scene=trimesh.load(tmp_path/entry['file'],force='scene')
        for name,values in entry['components'].items():
            mesh=scene.geometry[name]
            assert mesh.is_watertight
            assert mesh.volume==pytest.approx(values['volumeM3'],rel=1e-5)
            # GLB stores float32 coordinates; undo its up-axis mapping.
            assert np.allclose((mesh.vertices@TO_GLTF).min(axis=0),values['boundsM'][0],atol=1e-6)
            assert np.allclose((mesh.vertices@TO_GLTF).max(axis=0),values['boundsM'][1],atol=1e-6)
