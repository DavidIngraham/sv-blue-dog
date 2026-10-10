# Sail, keel and rudder sizing screen

<!-- Generated from SysML by scripts/render_requirements.py; edit the model, not this file. -->

[Method, limitations and design interpretation](<appendage-sizing.md>)

Synthetic inputs, not selected hardware. Zero area outputs when driveSolutionExists is false are invalid-result sentinels, not zero demand. Computation validity is distinct from modeledFit and supportedSizing. Read all gates together. Changing geometry or ballast requires resistance and hydrostatics to be updated.

## Flow

| Case | Boat speed | True wind | TWA (rad) | Apparent wind |
| --- | --- | --- | --- | --- |
| Reference | 3.721614637823934 \[SI::'m/s'\] | 5 \[SI::'m/s'\] | 0.7853981633974483 \[rad\] | 8.072558763251562 \[SI::'m/s'\] |
| Lower effort / more ballast | 3.721614637823934 \[SI::'m/s'\] | 5 \[SI::'m/s'\] | 0.7853981633974483 \[rad\] | 8.072558763251562 \[SI::'m/s'\] |
| Slow control probe | 0.5 \[SI::'m/s'\] | 5 \[SI::'m/s'\] | 0.7853981633974483 \[rad\] | 5.365215177971219 \[SI::'m/s'\] |
| Full-sail high wind | 3.721614637823934 \[SI::'m/s'\] | 15 \[SI::'m/s'\] | 0.7853981633974483 \[rad\] | 17.826883741515733 \[SI::'m/s'\] |
| Higher hull resistance | 3.721614637823934 \[SI::'m/s'\] | 5 \[SI::'m/s'\] | 0.7853981633974483 \[rad\] | 8.072558763251562 \[SI::'m/s'\] |

## Inputs

| Case | Bare hull resistance | Sail area | Keel area | Rudder area |
| --- | --- | --- | --- | --- |
| Reference | 4 \[N\] | 0.55 \[SI::'m²'\] | 0.012 \[SI::'m²'\] | 0.005 \[SI::'m²'\] |
| Lower effort / more ballast | 4 \[N\] | 0.55 \[SI::'m²'\] | 0.012 \[SI::'m²'\] | 0.005 \[SI::'m²'\] |
| Slow control probe | 4 \[N\] | 0.55 \[SI::'m²'\] | 0.012 \[SI::'m²'\] | 0.005 \[SI::'m²'\] |
| Full-sail high wind | 4 \[N\] | 0.55 \[SI::'m²'\] | 0.012 \[SI::'m²'\] | 0.005 \[SI::'m²'\] |
| Higher hull resistance | 12 \[N\] | 0.55 \[SI::'m²'\] | 0.012 \[SI::'m²'\] | 0.005 \[SI::'m²'\] |

## StabilityInputs

| Case | Effort height | Underwater force depth | Ballast | Other mass | Mass budget |
| --- | --- | --- | --- | --- | --- |
| Reference | 0.6 \[m\] | 0.2 \[m\] | 6 \[kg\] | 4 \[kg\] | 12 \[kg\] |
| Lower effort / more ballast | 0.3 \[m\] | 0.2 \[m\] | 8 \[kg\] | 4 \[kg\] | 12 \[kg\] |
| Slow control probe | 0.6 \[m\] | 0.2 \[m\] | 6 \[kg\] | 4 \[kg\] | 12 \[kg\] |
| Full-sail high wind | 0.6 \[m\] | 0.2 \[m\] | 6 \[kg\] | 4 \[kg\] | 12 \[kg\] |
| Higher hull resistance | 0.6 \[m\] | 0.2 \[m\] | 6 \[kg\] | 4 \[kg\] | 12 \[kg\] |

## SailDemand

| Case | Drive roots exist | Min area for drive | Upper drive root | Max area for heel | Drive/heel interval exists |
| --- | --- | --- | --- | --- | --- |
| Reference | true | 0.39925721227799876 \[SI::'m²'\] | 9.711781862946044 \[SI::'m²'\] | 0.2967903778462748 \[SI::'m²'\] | false |
| Lower effort / more ballast | true | 0.39925721227799876 \[SI::'m²'\] | 9.711781862946044 \[SI::'m²'\] | 0.598046888053536 \[SI::'m²'\] | true |
| Slow control probe | false | 0 \[SI::'m²'\] | 0 \[SI::'m²'\] | 0.7691300781057392 \[SI::'m²'\] | false |
| Full-sail high wind | true | 0.05282163047525398 \[SI::'m²'\] | 3.6491212182079025 \[SI::'m²'\] | 0.06617196304714147 \[SI::'m²'\] | true |
| Higher hull resistance | true | 1.1132606039155621 \[SI::'m²'\] | 8.99777847130848 \[SI::'m²'\] | 0.2967903778462748 \[SI::'m²'\] | false |

## FoilDemand

| Case | Minimum keel area | Minimum rudder area | Ballast required |
| --- | --- | --- | --- |
| Reference | 0.007147889887748487 \[SI::'m²'\] | 0.0017423419944007786 \[SI::'m²'\] | 12.577819211276708 \[kg\] |
| Lower effort / more ballast | 0.007147889887748487 \[SI::'m²'\] | 0.0017423419944007786 \[SI::'m²'\] | 7.219905871387219 \[kg\] |
| Slow control probe | 0.16509205041173908 \[SI::'m²'\] | 0.056439592085371366 \[SI::'m²'\] | 3.8033860240669504 \[kg\] |
| Full-sail high wind | 0.03080113690134811 \[SI::'m²'\] | 0.00584880848981738 \[SI::'m²'\] | 62.37266380212628 \[kg\] |
| Higher hull resistance | 0.007147889887748487 \[SI::'m²'\] | 0.0017423419944007786 \[SI::'m²'\] | 12.577819211276708 \[kg\] |

## Geometry

| Case | Keel span | Keel mean chord | Rudder span | Rudder mean chord |
| --- | --- | --- | --- | --- |
| Reference | 0.25 \[m\] | 0.048 \[m\] | 0.14 \[m\] | 0.03571428571428571 \[m\] |
| Lower effort / more ballast | 0.25 \[m\] | 0.048 \[m\] | 0.14 \[m\] | 0.03571428571428571 \[m\] |
| Slow control probe | 0.25 \[m\] | 0.048 \[m\] | 0.14 \[m\] | 0.03571428571428571 \[m\] |
| Full-sail high wind | 0.25 \[m\] | 0.048 \[m\] | 0.14 \[m\] | 0.03571428571428571 \[m\] |
| Higher hull resistance | 0.25 \[m\] | 0.048 \[m\] | 0.14 \[m\] | 0.03571428571428571 \[m\] |

## Loads

| Case | Drive margin | Keel trim load | Rudder trim load (signed) | Heel moment | Righting moment |
| --- | --- | --- | --- | --- | --- |
| Reference | 1.7996267196455902 \[N\] | 18.8002489965332 \[N\] | 2.0889165551703552 \[N\] | 16.711332441362842 \[SI::'kg⋅m²⋅s⁻²'\] | 13.526625462509422 \[SI::'N⋅m'\] |
| Lower effort / more ballast | 1.7996267196455902 \[N\] | 18.8002489965332 \[N\] | 2.0889165551703552 \[N\] | 10.444582775851776 \[SI::'kg⋅m²⋅s⁻²'\] | 17.03550061667923 \[SI::'N⋅m'\] |
| Slow control probe | -1.7558415612765303 \[N\] | 7.254602520586953 \[N\] | 0.8060669467318837 \[N\] | 6.44853557385507 \[SI::'kg⋅m²⋅s⁻²'\] | 13.526625462509422 \[SI::'N⋅m'\] |
| Full-sail high wind | 40.389486192445254 \[N\] | 84.32170886800027 \[N\] | 9.369078763111142 \[N\] | 74.95263010488914 \[SI::'kg⋅m²⋅s⁻²'\] | 13.526625462509422 \[SI::'N⋅m'\] |
| Higher hull resistance | -6.20037328035441 \[N\] | 18.8002489965332 \[N\] | 2.0889165551703552 \[N\] | 16.711332441362842 \[SI::'kg⋅m²⋅s⁻²'\] | 13.526625462509422 \[SI::'N⋅m'\] |

## Actuation

| Case | Demand torque | Coefficient-envelope torque | Available torque | Keel foil root side moment | Rudder root side moment |
| --- | --- | --- | --- | --- | --- |
| Reference | 0.09950062249133299 \[SI::'kg⋅m²⋅s⁻²'\] | 0.329168975069252 \[SI::'kg⋅m²⋅s⁻²'\] | 0.5 \[SI::'N⋅m'\] | 3.712546686849975 \[SI::'kg⋅m²⋅s⁻²'\] | 0.3243362382928873 \[SI::'kg⋅m²⋅s⁻²'\] |
| Lower effort / more ballast | 0.09950062249133299 \[SI::'kg⋅m²⋅s⁻²'\] | 0.329168975069252 \[SI::'kg⋅m²⋅s⁻²'\] | 0.5 \[SI::'N⋅m'\] | 3.712546686849975 \[SI::'kg⋅m²⋅s⁻²'\] | 0.3243362382928873 \[SI::'kg⋅m²⋅s⁻²'\] |
| Slow control probe | 0.07063650630146738 \[SI::'kg⋅m²⋅s⁻²'\] | 0.0354 \[SI::'kg⋅m²⋅s⁻²'\] | 0.5 \[SI::'N⋅m'\] | 1.5477379726100537 \[SI::'kg⋅m²⋅s⁻²'\] | 0.18963702940684782 \[SI::'kg⋅m²⋅s⁻²'\] |
| Full-sail high wind | 0.2633042721700007 \[SI::'kg⋅m²⋅s⁻²'\] | 0.329168975069252 \[SI::'kg⋅m²⋅s⁻²'\] | 0.5 \[SI::'N⋅m'\] | 15.997820412750052 \[SI::'kg⋅m²⋅s⁻²'\] | 1.08875327012667 \[SI::'kg⋅m²⋅s⁻²'\] |
| Higher hull resistance | 0.09950062249133299 \[SI::'kg⋅m²⋅s⁻²'\] | 0.329168975069252 \[SI::'kg⋅m²⋅s⁻²'\] | 0.5 \[SI::'N⋅m'\] | 3.712546686849975 \[SI::'kg⋅m²⋅s⁻²'\] | 0.3243362382928873 \[SI::'kg⋅m²⋅s⁻²'\] |

## Scaling

| Case | Sail Reynolds | Keel Reynolds | Rudder Reynolds | Keel aspect ratio | Rudder aspect ratio |
| --- | --- | --- | --- | --- | --- |
| Reference | 161451.17526503123 | 178637.50261554884 | 106331.84679496955 | 5.208333333333333 | 3.9200000000000004 |
| Lower effort / more ballast | 161451.17526503123 | 178637.50261554884 | 106331.84679496955 | 5.208333333333333 | 3.9200000000000004 |
| Slow control probe | 107304.30355942437 | 24000 | 14285.714285714286 | 5.208333333333333 | 3.9200000000000004 |
| Full-sail high wind | 356537.6748303146 | 178637.50261554884 | 106331.84679496955 | 5.208333333333333 | 3.9200000000000004 |
| Higher hull resistance | 161451.17526503123 | 178637.50261554884 | 106331.84679496955 | 5.208333333333333 | 3.9200000000000004 |

## Gates

| Case | Drive | Heel | Keel | Rudder | Torque | Mass | Numerical fit | Supported sizing |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Reference | true | false | true | true | true | true | false | false |
| Lower effort / more ballast | true | true | true | true | true | true | true | false |
| Slow control probe | false | true | false | false | true | true | false | false |
| Full-sail high wind | true | false | false | false | true | true | false | false |
| Higher hull resistance | false | false | true | true | true | true | false | false |
