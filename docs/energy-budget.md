# Sustained-operation energy roll-up

<!-- Generated from SysML by scripts/render_requirements.py; edit the model, not this file. -->

Generated natively from the synthetic example. These are illustrative inputs, not measurements or hardware selections. Conversion losses and uncertainty factors are included per load; peak powers are conservatively coincident. See sustained-operations.md for the executable campaign, evidence checklist and limitations.

| Load | Active power | Idle power | Active fraction | Conversion efficiency | Uncertainty factor | Average bus power | Peak bus power |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Guidance and mission computer | 2 \[W\] | 0.8 \[W\] | 1 | 0.9 | 1.15 | 2.5555555555555554 \[W\] | 2.5555555555555554 \[W\] |
| Position and wind sensors | 0.5 \[W\] | 0.1 \[W\] | 1 | 0.9 | 1.15 | 0.6388888888888888 \[W\] | 0.6388888888888888 \[W\] |
| Traffic sensing | 1 \[W\] | 0.2 \[W\] | 1 | 0.9 | 1.15 | 1.2777777777777777 \[W\] | 1.2777777777777777 \[W\] |
| Sail actuator | 8 \[W\] | 0.05 \[W\] | 0.02 | 0.9 | 1.15 | 0.26705555555555555 \[W\] | 10.222222222222221 \[W\] |
| Steering actuator | 6 \[W\] | 0.05 \[W\] | 0.05 | 0.9 | 1.15 | 0.4440277777777778 \[W\] | 7.666666666666666 \[W\] |
| Telemetry radio and command gateway | 6 \[W\] | 0.1 \[W\] | 0.02 | 0.9 | 1.15 | 0.2785555555555556 \[W\] | 7.666666666666666 \[W\] |
| Navigation signals | 0.6 \[W\] | 0 \[W\] | 0.5 | 0.9 | 1.15 | 0.3833333333333333 \[W\] | 0.7666666666666666 \[W\] |
| Recording electronics | 0.2 \[W\] | 0.05 \[W\] | 0.5 | 0.9 | 1.15 | 0.1597222222222222 \[W\] | 0.25555555555555554 \[W\] |
| Recovery controller and ingress sensing | 0.1 \[W\] | 0.05 \[W\] | 1 | 0.9 | 1.15 | 0.12777777777777777 \[W\] | 0.12777777777777777 \[W\] |
| Power management quiescent demand | 0.2 \[W\] | 0.2 \[W\] | 1 | 0.9 | 1.15 | 0.25555555555555554 \[W\] | 0.25555555555555554 \[W\] |
| Optional payload absent | 0 \[W\] | 0 \[W\] | 0 | 0.9 | 1.15 | 0 \[W\] | 0 \[W\] |

| Budget | Average demand | Coincident peak |
| --- | --- | --- |
| sailing | 6.388249999999998 \[W\] | 31.433333333333326 \[W\] |
