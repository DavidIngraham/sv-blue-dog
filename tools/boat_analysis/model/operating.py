"""Domain facades; generated contracts own argument shapes and preconditions."""
import numpy as np
from .boundary import ModelAdapter
from .preparation import prepare_operating as prepare
from .runtime import ROOT

CONTRACT = ROOT/'.tools/coupled-operation-contract.json'


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


if __name__ == '__main__':
    prepare()
