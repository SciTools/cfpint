# cfpint
Extensions to [pint](https://pint.readthedocs.io/en/stable/index.html) units, to support [CF compatible units](https://cfconventions.org/cf-conventions/cf-conventions.html#units).

## Purpose
Specifically, we would eventually like to replace the existing [cf-units](https://github.com/SciTools/cf-units) package in [Iris](https://github.com/SciTools/iris/issues/6929).

But the package is intended to be usable in its own right, without the Iris context defining it.

## Principles
For the time being, at least, **cfpint** should ... 

* provide convenient handling of CF compatible units ***as*** pint [Unit](https://pint.readthedocs.io/en/stable/api/base.html#pint.Unit)s.
* provide solutions matching "at least most of" the functions of cf-units
* support conversion of pint units to and from CF-compatible strings
* **not** replicate all of cf-units, or its API

Meanwhile, **Iris** should ...

* initially support *both/either* cf_units and cfpint units
    * ... but will eventually remove cf-units compatibility
* preserve (most) existing behaviours and operations
    * ... but units of results may differ in detail
* expose (cf)pint units transparently as units of its objects
* support inter-conversion between cfpint, cf-units and CF-compatible strings
* allow users to use pint operations (familiar, powerful), and not obscure them
* support conversion of existing user code to use pint-based units

