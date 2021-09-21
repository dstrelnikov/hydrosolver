hydrosolver
===========

[![Documentation Status](https://readthedocs.org/projects/hydrosolver/badge/?version=sphinx-docs)](https://hydrosolver.readthedocs.io/en/sphinx-docs/?badge=sphinx-docs)


Optimization driven hydroponic nutrient calculator and a domain-specific language.

License: [GNU GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html)


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

The documentation is provided in the `docs/` directory.
Hydrosolver's functions and classes are reasonably documented.
Whenever in doubt, use `help()` in Python's interpreter to get more information.

Several hints for a quick-start are provided in the `examples/` directory.
