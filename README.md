hydrosolver
===========

Optimization driven hydroponics nutrient calculator.


## Why?

I've recently got a new hobby - hydroponic plant growing. I checked many of the available hydroponics calculators and found out that each of them has a fatal flaw - it wasn't written by me.

Also, I got terribly sick on the weekend and promised myself to not work until a full recovery. On the second day I got bored and took my laptop to bed. My cat and I had an exciting programming session and the first version of hydrosolver appeared.


## How to use it?

Hydrosolver operates the following entities: `Composition` and `Solution`. 

### Compositions

Any fertilizer is a composition. Notice, that the tap water is also a composition since it has some nutrients.

Let's create one:
```
>>> from hydrosolver.composition import Composition

>>> epsom_salt = Composition(
...         name='Epsom Salt',
...         macronutrients=[
...             0.0,
...             0.0,
...             0.0,
...             0.0,
...             0.09861000665379185,
...             0.0,
...             0.13011408818708514,
...         ]
... )

>>> epsom_salt
Composition: Epsom Salt

Macronutrient       Ratio    Amount mg/kg
---------------  --------  --------------
N (NO3-)         0                      0
N (NH4+)         0                      0
P                0                      0
K                0                      0
Mg               0.09861            98610
Ca               0                      0
S                0.130114          130114

Micronutrient      Ratio    Amount mg/kg
---------------  -------  --------------
Fe                     0               0
Zn                     0               0
B                      0               0
Mn                     0               0
Cu                     0               0
Mo                     0               0
```

Compositions can be mixed together, and adjusted in concentration:

```
>>> CAN = Composition(
...         name='CAN',
...         macronutrients=[
...             0.144,
...             0.011,
...             0.0,
...             0.0,
...             0.0,
...             0.19406644742193763,
...             0.0,
...         ]
... )

>>> epsom_salt + 0.1 * CAN
Composition: Epsom Salt + 0.1 * (CAN)

Macronutrient         Ratio    Amount mg/kg
---------------  ----------  --------------
N (NO3-)         0.0072             7200
N (NH4+)         0.00055             550
P                0                     0
K                0                     0
Mg               0.049305          49305
Ca               0.00970332         9703.32
S                0.065057          65057

Micronutrient      Ratio    Amount mg/kg
---------------  -------  --------------
Fe                     0               0
Zn                     0               0
B                      0               0
Mn                     0               0
Cu                     0               0
Mo                     0               0
```


### Solutions

When we mix a few compositions we get a solution. Here is an example:

```
>>> from hydrosolver.composition import Composition

>>> water = Composition(
...         name='Water in Berlin',
...         macronutrients=[
...             0.0,
...             0.0,
...             0.0,
...             0.000005,
...             0.0000104,
...             0.00011,
...             0.00003638779589032540,
...         ],
...         micronutrients=[
...             0.00000003,
...             0.,
...             0.,
...             0.,
...             0.,
...             0.,
...         ],
... )

>>> water
Composition: Water in Berlin

Macronutrient          Ratio    Amount mg/kg
---------------  -----------  --------------
N (NO3-)         0                    0
N (NH4+)         0                    0
P                0                    0
K                5e-06                5
Mg               1.04e-05            10.4
Ca               0.00011            110
S                3.63878e-05         36.3878

Micronutrient      Ratio    Amount mg/kg
---------------  -------  --------------
Fe                 3e-08            0.03
Zn                 0                0
B                  0                0
Mn                 0                0
Cu                 0                0
Mo                 0                0

>>> solution = Solution(
...         10,
...         [0.050, 0.050],
...         water,
...         epsom_salt, CAN,
...         )

>>> solution
Composition        Amount in kg    Amount in g
---------------  --------------  -------------
Epsom Salt                 0.05             50
CAN                        0.05             50
Water in Berlin            9.9            9900
Total:                    10             10000

Composition: Resulting composition

Macronutrient          Ratio    Amount mg/kg
---------------  -----------  --------------
N (NO3-)         0.00072             720
N (NH4+)         5.5e-05              55
P                0                     0
K                4.95e-06              4.95
Mg               0.000503346         503.346
Ca               0.00107923         1079.23
S                0.000686594         686.594

Micronutrient       Ratio    Amount mg/kg
---------------  --------  --------------
Fe               2.97e-08          0.0297
Zn               0                 0
B                0                 0
Mn               0                 0
Cu               0                 0
Mo               0                 0

```

