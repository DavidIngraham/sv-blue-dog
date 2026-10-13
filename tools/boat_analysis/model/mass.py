"""Typed facade for the model-defined mass calculation."""
from numpy.typing import ArrayLike
from .design_types import Design, Parameters
from .boundary import ModelAdapter
from .preparation import prepare_mass as prepare
from .runtime import ROOT

CONTRACT = ROOT/'.tools/coupled-contract.json'


class MassKernel(ModelAdapter):
    model_name = 'mass'

    def evaluate(self, design: Design | ArrayLike, geometry: ArrayLike,
                 parameters: Parameters | ArrayLike | None = None):
        return self.kernel.evaluate(design=design, geometry=geometry, parameters=parameters)


if __name__ == '__main__':
    prepare()
