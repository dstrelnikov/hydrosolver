Working with solutions
======================

A more advanced entity in hydrosolver is ``Solution``.
Solutions consist of a few compositions and can be constructed in different ways.
Solutions added and scaled, extended and merged.


Defining a solution
-------------------

To define a solution we must first define the compositions constituting it. Let us consider a simple example::

    from hydrosolver.composition import Composition
    from hydrosolver.solution import Solution

    water = Composition('Pure water')
    CN = Composition.from_dict(
        {'Calcium nitrate tetrahydrate': {'N (NO3-)': 0.1186, 'Ca': 0.1697}}
        )

    solution_CN_10 = Solution(
        [CN, water],
        [0.1, 0.9],
        )

Here we just defined a 10% (by mass) aqueous solution of calcium nitrate tetrahydrate.
