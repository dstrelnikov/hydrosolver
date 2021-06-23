hydrosolver
===========

Optimization driven hydroponics nutrient calculator.


## Why?

I've recently got a new hobby - hydroponic plant growing. I checked many of the available hydroponics calculators and found out that each of them has a fatal flaw - it wasn't written by me.

Also, I got terribly sick on the weekend and promised myself to not work until a full recovery. On the second day I got bored and took my laptop to bed. My cat and I had an exciting programming session and the first version of hydrosolver appeared.


## How to use it?

Hydrosolver operates the following entities: `Composition` and `Solution`. 

### Compositions

Any fertilizer is a composition. Let's create one.

```
from hydrosolver.composition import Composition

epsom_salt = Composition(
        name='Epsom Salt',
        macronutrients=[
            0.0,
            0.0,
            0.0,
            0.0,
            0.09861000665379185,
            0.0,
            0.13011408818708514,
        ]
)

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

Notice, that the tap water is also a composition since it has some nutrients.

```
water_berlin = Composition(
        name='Water (Berlin)',
        macronutrients=[
            0.0,
            0.0,
            0.0,
            0.000005,
            0.0000104,
            0.00011,
            0.00003638779589032540,
        ],
        micronutrients=[
            0.00000003,
            0.,
            0.,
            0.,
            0.,
            0.,
        ],
)

>>> water_berlin
Composition: Water (Berlin)

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
```

Compositions can be mixed together, and adjusted in concentration:

```
CAN = Composition(
        name='CAN',
        macronutrients=[
            0.144,
            0.011,
            0.0,
            0.0,
            0.0,
            0.19406644742193763,
            0.0,
        ]
)

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
from hydrosolver.solution import solution

masterblend_tomato = Composition(
        name='Masterblend 4-18-38 Tomato Formula',
        macronutrients=[
            0.035,
            0.005,
            0.03927841356407048,
            0.1577285418546632,
            0.005,
            0.0,
            0.007,
        ],
        micronutrients=[
            0.004,
            0.0005,
            0.002,
            0.002,
            0.005,
            0.0001,
        ],
)

leafy_greens = Solution(
        mass_total=10,
        water=water_berlin,
        formulation=[0.0053, 0.0053, 0.00265],
        fertilizers=[masterblend_tomato, CAN, epsom_salt],
        )

>>> leafy_greens
Composition                                    Amount in kg    Amount in g
-------------------------------------------  --------------  -------------
Magnesium sulfate heptahydrate (Epsom Salt)            0.05             50
CAN                                                    0.05             50
Water (Berlin)                                         9.9            9900
Total:                                                10             10000

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

Pay attention that the water is treated specially in the solution definition. If you use reverse osmosis water then put just an empty `Composition()` in the corresponding position.

You can get the resulting composition from a solution as `leafy_greens.composition`.


### Optimization

If you have some desired `Composition` in mind you can set it as a target to a `Solution`.

```
import numpy as np

fertilizers = [masterblend_tomato, CAN, epsom_salt]

solution = Solution(
        10,
        db['Water (Berlin)'],
        np.zeros(len(fertilizers)),
        fertilizers,
        )

>>> solution
Composition                           Amount in kg    Amount in g
----------------------------------  --------------  -------------
Masterblend 4-18-38 Tomato Formula               0              0
CAN                                              0              0
Epsom Salt                                       0              0
Water (Berlin)                                  10          10000
Total:                                          10          10000

Composition: Resulting composition

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


solution.composition_target = leafy_greens.composition
```

Why did we just create a dummy solution and set up its target? Now we can recover the original recipe!

```
from hydrosolver import optimization

>>> optimization.solve_lstsq(solution)
Composition                           Amount in kg    Amount in g
----------------------------------  --------------  -------------
Masterblend 4-18-38 Tomato Formula         0.0053            5.3
CAN                                        0.0053            5.3
Epsom Salt                                 0.00265           2.65
Water (Berlin)                             9.98675        9986.75
Total:                                    10             10000

Composition: Resulting composition

Macronutrient          Ratio    Amount mg/kg
---------------  -----------  --------------
N (NO3-)         9.487e-05           94.87
N (NH4+)         8.48e-06             8.48
P                2.08176e-05         20.8176
K                8.85895e-05         88.5895
Mg               3.91679e-05         39.1679
Ca               0.000212709        212.709
S                7.45298e-05         74.5298

Micronutrient          Ratio    Amount mg/kg
---------------  -----------  --------------
Fe               2.14996e-06         2.14996
Zn               2.65e-07            0.265
B                1.06e-06            1.06
Mn               1.06e-06            1.06
Cu               2.65e-06            2.65
Mo               5.3e-08             0.053
```

That was actually quite easy since we mixed `leafy_greens` from exactly the same fertilizers. But don't get tricked by `solve_lstsq`: if the linear system has no exact solution, the least square method can find the optimal formulation outside the feasible set (i.e. negative amounts of fertilizers, etc). I leave the verification of this fact as an exercise for the reader.

Let us try to get the desired composition with another set of fertilizers.

```
haka_basis_2 = Composition(
        name='Hakaphos Basis 2',
        macronutrients=[
            0.03,
            0.0,
            0.01963920678203524,
            0.1660300440575402,
            0.02412167526796348,
            0.0,
            0.0,
        ],
        micronutrients=[
            0.0015,
            0.00015,
            0.0001,
            0.0005,
            0.0002,
            0.00001,
        ],
)

fertilizers = [haka_basis_2, CAN, epsom_salt]

solution = Solution(
        10,
        db['Water (Berlin)'],
        np.zeros(len(fertilizers)),
        fertilizers,
        )

solution.composition_target = leafy_greens.composition

descent = optimization.gradient_descent(solution, iter_max=150, step_init=0.1, step_prediction=True)

Starting the gradient descent procedure...
  i.j            step              R     norm(grad)    norm(Pgrad)
                       2.9338279e-06  7.7810447e-04  7.7810447e-04
  1.0   1.0000000e-01  2.9111881e-06  7.7458434e-04  7.7458434e-04
  2.0   2.0182195e-01  2.8661405e-06  7.6753543e-04  7.6753543e-04
 [...]
 32.3   1.4919715e+01  2.3960037e-08  4.7287745e-09  4.7287745e-09
 33.0   2.0172918e+01
The descend procedure has looped:
project(formulation_next) == formulation.
Terminating.

solution_optimized = descent[-1]

>>> solution_optimized
Composition         Amount in kg    Amount in g
----------------  --------------  -------------
Hakaphos Basis 2      0.00506747        5.06747
CAN                   0.00538727        5.38727
Epsom Salt            0.00247688        2.47688
Water (Berlin)        9.98707        9987.07
Total:               10             10000

Composition: Resulting composition

Macronutrient          Ratio    Amount mg/kg
---------------  -----------  --------------
N (NO3-)         9.27792e-05         92.7792
N (NH4+)         5.926e-06            5.926
P                9.9521e-06           9.9521
K                8.91287e-05         89.1287
Mg               4.70346e-05         47.0346
Ca               0.000214407        214.407
S                6.85684e-05         68.5684

Micronutrient          Ratio    Amount mg/kg
---------------  -----------  --------------
Fe               7.90081e-07      0.790081
Zn               7.6012e-08       0.076012
B                5.06747e-08      0.0506747
Mn               2.53373e-07      0.253373
Cu               1.01349e-07      0.101349
Mo               5.06747e-09      0.00506747
```

Wow! Not exactly what we wanted but quite close. Feel free to adjust the optimized recipe to your own taste manually.
