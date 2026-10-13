"""Domain facades; generated contracts own argument shapes and preconditions."""
import numpy as np
from .boundary import ModelAdapter
from .preparation import prepare_operating as prepare
from .runtime import ROOT

CONTRACT = ROOT/'.tools/coupled-operation-contract.json'


class OperationKernel(ModelAdapter):
    model_name = 'operation'

    def evaluate(self, design, parameters, state, aero, mass, hydro):
        return self.kernel.evaluate(design=design, parameters=parameters, state=state,
                                    aero=aero, mass=mass, hydro=hydro)


class StructureKernel(ModelAdapter):
    model_name = 'structure'

    def evaluate(self, design, parameters, mass, geometry, loads, waterline):
        return self.kernel.evaluate(design=design, parameters=parameters, mass=mass,
                                    geometry=geometry, loads=loads, waterline=waterline)


class RouteKernel(ModelAdapter):
    model_name = 'route'

    def evaluate(self, water, states, policy=None, wind_from=None):
        if wind_from is not None:
            if wind_from not in ('east', 'west'):
                raise ValueError('wind_from must be east or west')
            policy = np.array(self.contract['routeParameters'] if policy is None else policy, dtype=float, copy=True)
            if policy.shape != np.shape(self.contract['routeParameters']):
                raise ValueError('Invalid route policy shape')
            policy[-1] = float(wind_from == 'east')
        return self.kernel.evaluate(water=water, states=states, policy=policy)


class ConceptKernel(ModelAdapter):
    model_name = 'concept'

    def evaluate(self, design, mass, geometry, duration, power, policy=None):
        return self.kernel.evaluate(design=design, mass=mass, geometry=geometry,
                                    passage=[duration, power], policy=policy)


if __name__ == '__main__':
    prepare()
