# Independent thermal example

This example has no boat geometry, requirements or evidence-store dependency. `Thermal::JouleHeat` is exported through `pyproject.toml` as `joule_heat`; no Python adapter is authored.

Use the local `sysml-python-runtime` package, set `OPENSYSML_BINARY` to a pinned OpenSysML executable, and run:

```python
from sysml_python import Project
Project("pyproject.toml").prepare()
from generated import joule_heat
assert joule_heat(current=2, resistance=10).power == 40
print(joule_heat.batch(shared={"resistance": 10}, cases={"current": [1, 2, 3]}).values)
```

The current native execution backend requires Linux and GCC. This is the first independent proof, not yet the final distributable project template.
