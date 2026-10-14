"""Project mesh integration around generated SysML hydrostatic calculations."""
import numpy as np
from sysml_python import execution_session
from tools.boat_analysis.geometry.hydro import equilibrium as _equilibrium, free_pitch_equilibrium as _free_pitch_equilibrium

# Keep numerical solves within a verified runtime snapshot.
equilibrium = execution_session()(_equilibrium)
free_pitch_equilibrium = execution_session()(_free_pitch_equilibrium)


class MeshHydrostatics:
    """Adapt project tetrahedral meshes to generated model calculations."""

    @staticmethod
    def balance(moments, cg, mass, density):
        from tools.boat_analysis.generated import hydrostatic_balance
        return hydrostatic_balance(moments=moments, cg=cg, mass=mass, density=density).as_array()

    @staticmethod
    def moments(tetrahedra, waterline):
        from tools.boat_analysis.generated import wet_moment
        points = np.asarray(tetrahedra, dtype=float)
        if points.ndim != 3 or points.shape[1:] != (4, 3) or len(points) == 0:
            raise ValueError('Nonempty tetrahedra (n,4,3) required')
        rows = wet_moment.batch(shared={'waterline': waterline},
                                cases={'vertices': points.reshape(-1, 12)}).values
        result = rows.sum(axis=0)
        if not np.isfinite(result).all():
            raise ValueError('Nonfinite mesh moment sum')
        return result
