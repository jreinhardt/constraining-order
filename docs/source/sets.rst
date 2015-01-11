Sets
====

In addition to constraint satisfaction, Constraining Order also contains an
implementation of Intervals and IntervalSets over the real numbers and
datastructures for sets in several dimensions.


DiscreteSet
-----------

The use of the :class:`~constrainingorder.sets.DiscreteSet` is very similar
to the built in :class:`frozenset`:

.. doctest:: discreteset

   >>> from constrainingorder.sets import DiscreteSet
   >>> a = DiscreteSet([1,2,'a','b'])
   >>> b = DiscreteSet([1,'a','c',3])

DiscreteSets support the usual set operations and membership tests

.. doctest:: discreteset

   >>> a.union(b)
   DiscreteSet([1,2,3,'a','b','c'])
   >>> a.intersection(b)
   DiscreteSet([1,'a'])
   >>> a.difference(b)
   DiscreteSet([2,'b'])
   >>> 1 in a
   True
   >>> "Foo" in b
   False

The main difference is that a DiscreteSet can represent a set of
"everything", which makes sense sometimes

.. doctest:: discreteset

   >>> c = DiscreteSet.everything()
   >>> c.union(a)
   DiscreteSet.everything()
   >>> c.intersection(a)
   DiscreteSet([1,2,'a','b'])

One can also iterate over all members

.. doctest:: discreteset

   >>> [m for m in a.iter_members()]
   [1, 2, 'a', 'b']

Interval
--------

To initialize a Interval one passes the bounds and indicates whether they are
included in the interval, or alternatively one of the convenience class
methods

.. doctest:: interval

   >>> from constrainingorder.sets import Interval
   >>> a = Interval((0,1),(True,True))
   >>> b = Interval.open(1,3)
   >>> c = Interval.leftopen(2,4)

Intervals only support the intersection operation, as for the others the
result might not be a single connected interval.

.. doctest:: interval

   >>> b.intersection(c)
   Interval((2, 3),(False, False))

One can check membership in Intervals

.. doctest:: interval

   >>> 0.3 in a
   True
   >>> 1.3 in a
   False

Intervals can also represent the full real axis and a single point:

.. doctest:: interval

   >>> d = Interval.everything()
   >>> e = Interval.from_value(2.4)

IntervalSets
------------

The main use of Intervals is in IntervalSets, which can represent fairly
general sets of real numbers. They get initialized by a sequence of
Intervals, or one of the convenience functions

.. doctest:: intervalset

   >>> from constrainingorder.sets import Interval,IntervalSet
   >>> a = IntervalSet([Interval.open(0,3), Interval.open(5,8)])
   >>> b = IntervalSet([Interval.closed(2,3), Interval.closed(7,10)])
   >>> c = IntervalSet.from_values([4, -1])
   >>> d = IntervalSet.everything()

In contrast to Intervals, IntervalSets support all of the common set
operations

.. doctest:: intervalset

   >>> a.union(b)
   IntervalSet([Interval((0, 3),(False, True)),Interval((5, 10),(False, True))])
   >>> a.intersection(b)
   IntervalSet([Interval((2, 3),(True, False)),Interval((7, 8),(True, False))])
   >>> a.difference(b)
   IntervalSet([Interval((0, 2),(False, False)),Interval((5, 7),(False, False))])

Membership tests work as expected

.. doctest:: intervalset

   >>> 2 in a
   True
   >>> 4 in a
   False
   >>> -1 in c
   True

Like DiscreteSets, one can iterate over the members if the IntervalSet only contains isolated points

.. doctest:: intervalset

   >>> c.is_discrete()
   True
   >>> [m for m in c.iter_members()]
   [-1, 4]
