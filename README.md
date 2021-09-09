hydrosolver
===========

Optimization driven hydroponic nutrient calculator and a DSL.

License: [GNU GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html)

## Why?

I've recently got a new hobby - hydroponic plant growing. I checked many of the available hydroponics calculators and found out that each of them has a fatal flaw - it wasn't written by me.

Also, I got terribly sick on the weekend and promised myself to not work until a full recovery. On the second day I got bored and took my laptop to bed. My cat and I had an exciting programming session and the first version of hydrosolver appeared.


## Who can use it?

If you feel more comfortable in Python REPL and a text editor than in a sophisticated GUI application, just like me, then give hydrosolver a try.


## How to use it?
Hydrosolver introduces two main entities: `Composition` and `Solution`. 

`Composition` is an arbitrary substance which can contain some of the nutrients considered for hydroponic plant growing. It will mostly represent water, some salt or a complex fertilizer.

`Solution` is a mix of `Composition`'s in given amounts. Normally, one or more compositions constituting the solution must be water. However, there is no issue with creating dry "solutions".

Please find more details in the `examples/` directory.
