Sets
====

Constraining Order contains DataStructures to represent sets of discrete elements and real numbers.

A DiscreteSet is a wrapper around pythons builtin :class:`frozenset`. The
main difference is that a DiscreteSet can represent a set of all possible
elements.

In addition, there are data structures to represent sets of real numbers, in
form of connected :class:`Intervals <constrainingorder.sets.Interval>` and
collections of such intervals, called :class:`IntervalSet
<constrainingorder.sets.IntervalSet>`.

DiscreteSet
-----------

.. autoclass:: constrainingorder.sets.DiscreteSet
   :members:
   :special-members: __init__, __contains__

Interval
--------

.. autoclass:: constrainingorder.sets.Interval
   :members:
   :special-members: __init__, __contains__


IntervalSet
-----------

.. autoclass:: constrainingorder.sets.IntervalSet
   :members:
   :special-members: __init__, __contains__

