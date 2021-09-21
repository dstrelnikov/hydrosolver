Working with solutions
======================

A more advanced entity in hydrosolver is ``Solution``.
Solutions consist of a few compositions and can be constructed in different ways.
Solutions can be added, scaled, extended and merged.


Defining a solution
-------------------

To define a solution we must first define the compositions constituting it. Let us consider a simple example:

>>> from hydrosolver.composition import Composition
>>> from hydrosolver.solution import Solution
>>> water = Composition('Pure water')
>>> CN = Composition.from_dict(
...     {'Calcium nitrate tetrahydrate':
...         {'N (NO3-)': 0.1186, 'Ca': 0.1697}}
...     )
>>> solution_CN_10 = Solution(
...     compositions=[CN, water],
...     formulation=[0.1, 0.9],
...     )
>>> solution_CN_10
Composition                     Amount in kg    Amount in g
----------------------------  --------------  -------------
Calcium nitrate tetrahydrate             0.1            100
Pure water                               0.9            900
Total:                                   1             1000
<BLANKLINE>
Composition: Resulting composition
<BLANKLINE>
Nutrient      Ratio    Amount mg/kg
----------  -------  --------------
N (NO3-)    0.01186           11860
Ca          0.01697           16970

Here we just defined a 10% (by mass) aqueous solution of calcium nitrate tetrahydrate. It's total mass is given by ``solution_CN_10.mass`` and equals to 1 [kg].
However, if the solution to construct consists of multiple compositions, it becomes more difficult to adjust the mass of the water.
For this purpose there is an alternative constructor ``Solution.dissolve()``:

>>> solution_CN_10 = Solution.dissolve(
...     mass=1,
...     water=water,
...     compositions_=[CN],
...     formulation_=[0.1],
...     )
>>> solution_CN_10
Composition                     Amount in kg    Amount in g
----------------------------  --------------  -------------
Calcium nitrate tetrahydrate             0.1            100
Pure water                               0.9            900
Total:                                   1             1000
<BLANKLINE>
Composition: Resulting composition
<BLANKLINE>
Nutrient      Ratio    Amount mg/kg
----------  -------  --------------
N (NO3-)    0.01186           11860
Ca          0.01697           16970

As one can see, for ``dissolve`` we first pass the desired total mass of the solution, then the composition which will be used for aligning (typically the water) and the truncated lists of compositions and their amounts without the last element, which will be substituted with ``water``.
This way fits more for defining solutions consisting of many compositions:

>>> MS = Composition.from_dict(
...     {'Magnesium sulfate heptahydrate':
...         {'Mg': 0.0986, 'S': 0.1301}}
...     )
>>> my_solution = Solution.dissolve(
...     mass=1,
...     water=water,
...     compositions_=[CN, MS],
...     formulation_=[0.002, 0.001],
...     )
>>> my_solution
Composition                       Amount in kg    Amount in g
------------------------------  --------------  -------------
Calcium nitrate tetrahydrate             0.002              2
Magnesium sulfate heptahydrate           0.001              1
Pure water                               0.997            997
Total:                                   1               1000
<BLANKLINE>
Composition: Resulting composition
<BLANKLINE>
Nutrient        Ratio    Amount mg/kg
----------  ---------  --------------
N (NO3-)    0.0002372           237.2
Mg          9.86e-05             98.6
Ca          0.0003394           339.4
S           0.0001301           130.1


Operations on solutions
-----------------------

The available operations on solutions can be split into two cathegories.

Operations preserving compositions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Any solution can be multiplied by a scalar. Two solutions defined in the same basis (i.e. consisting of the same compositions listed in the same order) can be added (and hence subtracted):

>>> 100 * my_solution
Composition                       Amount in kg    Amount in g
------------------------------  --------------  -------------
Calcium nitrate tetrahydrate               0.2            200
Magnesium sulfate heptahydrate             0.1            100
Pure water                                99.7          99700
Total:                                   100           100000
<BLANKLINE>
Composition: Resulting composition
<BLANKLINE>
Nutrient        Ratio    Amount mg/kg
----------  ---------  --------------
N (NO3-)    0.0002372           237.2
Mg          9.86e-05             98.6
Ca          0.0003394           339.4
S           0.0001301           130.1

>>> solution_CN_20 = Solution.dissolve(1, water, [CN], [0.2])
>>> 5 * solution_CN_20 + 10 * solution_CN_20
Composition                     Amount in kg    Amount in g
----------------------------  --------------  -------------
Calcium nitrate tetrahydrate               3           3000
Pure water                                12          12000
Total:                                    15          15000
<BLANKLINE>
Composition: Resulting composition
<BLANKLINE>
Nutrient      Ratio    Amount mg/kg
----------  -------  --------------
N (NO3-)    0.02372           23720
Ca          0.03394           33940


Another operation preserving the compositions is ``align()``. It adjusts the total mass of the solution to the specified value by changing the amount of the last composition (typically water):

>>> solution_CN_20.align(10)
>>> solution_CN_20
Composition                     Amount in kg    Amount in g
----------------------------  --------------  -------------
Calcium nitrate tetrahydrate             0.2            200
Pure water                               9.8           9800
Total:                                  10            10000
<BLANKLINE>
Composition: Resulting composition
<BLANKLINE>
Nutrient       Ratio    Amount mg/kg
----------  --------  --------------
N (NO3-)    0.002372            2372
Ca          0.003394            3394


Operations extending compositions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

An existing solution can be modified by adding another composition in the specified amount:

>>> MAP = Composition.from_dict(
...     {'Monoammonium phosphate':
...         {'N (NH4+)': 0.12177, 'P': 0.26928}}
...     )
>>> my_solution.add(MAP, 0.001)
>>> my_solution
Composition                       Amount in kg    Amount in g
------------------------------  --------------  -------------
Calcium nitrate tetrahydrate             0.002              2
Magnesium sulfate heptahydrate           0.001              1
Monoammonium phosphate                   0.001              1
Pure water                               0.996            996
Total:                                   1               1000
<BLANKLINE>
Composition: Resulting composition
<BLANKLINE>
Nutrient         Ratio    Amount mg/kg
----------  ----------  --------------
N (NO3-)    0.0002372           237.2
N (NH4+)    0.00012177          121.77
P           0.00026928          269.28
Mg          9.86e-05             98.6
Ca          0.0003394           339.4
S           0.0001301           130.1

This operation does not return a new solution but always modifies the given one in place.
Notice that by default the aligning operation is performed when ``add`` is called.

Any solutions can be merged which will result in a nes solution:

>>> solution_a = Solution.dissolve(1, water, [CN], [0.002])
>>> solution_b = Solution.dissolve(1, water, [MS, MAP], [0.001, 0.001])
>>> solution_a.merge(solution_b)
Composition                       Amount in kg    Amount in g
------------------------------  --------------  -------------
Calcium nitrate tetrahydrate             0.002              2
Magnesium sulfate heptahydrate           0.001              1
Monoammonium phosphate                   0.001              1
Pure water                               1.996           1996
Total:                                   2               2000
<BLANKLINE>
Composition: Resulting composition
<BLANKLINE>
Nutrient         Ratio    Amount mg/kg
----------  ----------  --------------
N (NO3-)    0.0001186          118.6
N (NH4+)    6.0885e-05          60.885
P           0.00013464         134.64
Mg          4.93e-05            49.3
Ca          0.0001697          169.7
S           6.505e-05           65.05
