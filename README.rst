Constraining Order
==================

Constraining order is a pure python library for solving certain classes of
constraint satisfaction problems. In particular it contains an implementation
of IntervalSets to represent fairly general sets of real numbers.

Constraining order is neither very powerful, nor very performant, and for
serious problems there are more powerful solutions available:

* [gecode](http://www.gecode.org) (which looks amazing and superbly documented)
* [or-tools](https://code.google.com/p/or-tools/)
* [choco](http://www.choco-solver.org/)

The creation of constraining order was sparked by the realisation that several
of my problems require the solution of relatively simple constraint
satisfaction problems, while it was unacceptable to pull in a heavy dependency
for that.

The API of constraining order is slightly inspired by gecode (as I had looked
at its documentation before writing it) and the nomenclature I use roughly
follows

    Tsang, E. Foundations of Constraint Satisfaction Academic Press, 1996

which I used to read up a bit on the topic.

The name `constraining order` is a pun on restraining order, as it was not yet
taken for a software project and even makes a bit of sense as long as you don't
think about it.
