hydrosolver
===========

[![Documentation Status](https://readthedocs.org/projects/hydrosolver/badge/?version=latest)](https://hydrosolver.readthedocs.io/en/latest/?badge=latest)


Optimization driven hydroponic nutrient calculator and a domain-specific language.

**Author:** Dmytro Strelnikov  
**License:** [GNU GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html)

---

Enjoy the power of mathematical optimization:

```python
>>> MKP = Composition.from_dict(
... {'Monopotassium phosphate': {'P': 0.2276, 'K': 0.2873}}
... )
>>> MS = Composition.from_dict(
... {'Magnesium sulfate heptahydrate': {'Mg': 0.0986, 'S': 0.1301}}
... )
>>> CaN = Composition.from_dict(
... {'Calcium nitrate tetrahydrate': {'N (NO3-)': 0.1186, 'Ca': 0.1697}}
... )
>>> composition_target = Composition.from_dict(
... {'Target composition': {
...     'N (NO3-)': 0.000120, 'P': 0.000040, 'K': 0.000055,
...     'Mg': 0.000100, 'Ca': 0.000170, 'S': 0.000130,
...     }
... }
... )
>>> solution_init = Solution.dissolve(
...     100,
...     Composition(name='RO water'),
...     [CaN, MS, MKP],
... )
>>> solution_optimal = optimize(solution_init, composition_target)
Composition                       Amount in kg    Amount in g
------------------------------  --------------  -------------
Calcium nitrate tetrahydrate         0.100507        100.507
Magnesium sulfate heptahydrate       0.10047         100.47
Monopotassium phosphate              0.0185388        18.5388
RO water                            99.7805        99780.5
Total:                             100            100000

Composition: Resulting composition

Nutrient          Ratio    Amount mg/kg
----------  -----------  --------------
N (NO3-)    0.000119201        119.201
P           4.21942e-05         42.1942
K           5.32619e-05         53.2619
Mg          9.90635e-05         99.0635
Ca          0.00017056         170.56
S           0.000130712        130.712
```


## What is it?

Hydrosolver is a Python module implementing a domain-specific language for operations with hydroponic nutrient solutions.
It also features mathematical optimization tools helping to mix the most suitable solution using only available ingredients.


## Why?

I've recently got a new hobby - hydroponic plant growing. I checked many of the available hydroponics calculators and found out that each of them has a fatal flaw - it wasn't written by me.

Also, I got terribly sick on the weekend and promised myself to not work until a full recovery. On the second day I got bored and took my laptop to bed. My cat and I had an exciting programming session and the first version of hydrosolver appeared.


## Who can use it?

If you feel more comfortable in Python REPL and a text editor than in a sophisticated GUI application, just like me, then give hydrosolver a try.


## How to use it?

Hydrosolver introduces two main entities: `Composition` and `Solution`. 

`Composition` is an arbitrary substance which can contain some of the nutrients which are usually considered in hydroponic plant growing.
It will mostly represent the water you use, a salt or a complex fertilizer.
You can define a composition on the go or load one from a file.

Compositions are internally represented as vectors (see `composition.nutrients_stencil`). Therefore they generate a vector space, i.e. compositions may be added and scaled.

`Solution` is a mix of a few `Composition`s in given amounts.
Normally, one or more compositions constituting the solution must be water.
However, in hydrosolver there is no artificial limitation preventing you from creating dry "solutions".

Similarly to the vector space of compositions, there is an infinite-dimensional vector space of solutions.
Solutions defined in the same basis (i.e. consisting of the same compositions listed in the same order) generate a finite-dimensional subspace.
Such solutions may be added and scaled in the usual way.

There are also operations (for instance, `add` and `merge`) which take their results in subspaces of higher dimensions.


## Documentations

The online documentation is available on [Read the Docs](https://hydrosolver.readthedocs.io/).

Several hints for a quick-start are provided in the `examples/` directory.
