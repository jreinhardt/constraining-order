.. Constraining order documentation master file, created by
   sphinx-quickstart on Thu Jan  8 12:48:10 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Constraining Order's documentation!
==============================================

Constraining Order is a pure python library for solving certain classes of
constraint satisfaction problems (CSP). In particular it contains an
implementation of IntervalSets to represent fairly general sets of real
numbers.

Constraining Order is licensed under the MIT license.

Constraining Order is relatively flexible in the sense that many CSPs can be
quickly modeled and new constraints can be implemented very easily. However
it is not tuned towards high performance.

For serious problems there are much more powerful solutions available:

* `gecode <http://www.gecode.org>`_ (which looks amazing and superbly
  documented)
* `or-tools <https://code.google.com/p/or-tools/>`_
* `choco <http://www.choco-solver.org/>`_
* or one of the many specialized `constraint programming languages
  <https://en.wikipedia.org/wiki/Constraint_programming>`_

For python there are several packages for constraint satisfaction problems:

* `ortools <https://pypi.python.org/pypi/ortools/1.3795>`_
* `gecode-python <https://pypi.python.org/pypi/gecode-python/0.27>`_ outdated,
  inactive
* `logilab-constraints
  <https://pypi.python.org/pypi/logilab-constraint/0.5.0>`_ sparse
  documentation, inactive
* `pyconstraints <https://pypi.python.org/pypi/pyconstraints/1.0.1>`_ sparse
  documentation, inactive

For a nice overview over the theoretical foundations, see e.g. [Tsang96]_.

Contents:

.. toctree::
   :maxdepth: 2

   quickstart
   sets
   custom_constraints


API Reference:

.. toctree::
   :maxdepth: 2

   sets_api
   csp_api

.. todolist::


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

References
==========

.. [Tsang96] Tsang, E. Foundations of Constraint Satisfaction Academic Press, 1996
