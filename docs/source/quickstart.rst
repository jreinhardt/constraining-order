Quickstart
==========

For a quick introduction we will write a Sudoku solver. `Sudokus
<https://en.wikipedia.org/Sudoku>`_ are popular puzzles that are often found
in Newspapers. The task is to fill in numbers in a (already partly filled)
9x9 grid, such that no number is present twice in a row, column or one of the
9 3x3 blocks.

Sudokus are constraint satisfaction problems. The 81 fields of the grid are
the variables, their domain is the set of numbers from 1 to 9, and the
constraints are the number placement rules.

Variables
---------

The first step is to model the space our problem lives in. For that we need
the variables and their domains. We can make use of python to do this very
compactly for all 81 variables

.. testcode::

    from constrainingorder.sets import DiscreteSet
    from constrainingorder.variables import DiscreteVariable

    numbers = range(1,10)
    domain = DiscreteSet(numbers)
    variables = {}
    for i in numbers:
        for j in numbers:
            name = 'x%d%d' % (i,j)
            variables[name] = DiscreteVariable(name,domain=domain)

A DiscreteSet is a datastructure representing a set of discrete elements,
very similar to pythons built-in set. But it can also represent the "set of
everything", which is sometimes convenient. For details see 
.. todo:: Add DiscreteSet reference

A DiscreteVariable is a variable that can take on values from a DiscreteSet.
Each variable has a name. The variables `x11` is the number in the first row
and first column, the variable `x12` the one in the first row and second
column and so on. We store them in a dictionary, so that we can easily to
refer to them by name when building the constraints. This is often
convenient, but not always necessary.

Constraints
-----------

The constraints model the requirements, that no number is allowed to occur
twice in a row, column or block. Or equivalently, that all numbers in a row,
column or block are different (as there are exactly nine different numbers).
Luckily constraining order already comes with a constraint of this type, so
we just have to use it:

.. testcode::

    from constrainingorder.constraints import AllDifferent

    cons = []
    #row constraints
    for i in numbers:
        cons.append(AllDifferent([variables['x%d%d'%(i,j)] for j in numbers]))
    #column constraints
    for i in numbers:
        cons.append(AllDifferent([variables['x%d%d'%(j,i)] for j in numbers]))
    #block constraints
    for i in range(0,3):
        for j in range(0,3):
            #assemble list of parameternames for this block
            names = []
            for k in range(0,3):
                for l in range(0,3):
                    names.append('x%d%d' % (3*i + k + 1,3*j + l + 1))
            #create constraint
            cons.append(AllDifferent([variables[n] for n in names]))

If we wanted to find all possible completely filled sudokus, we could now try
to enumerate all solutions to this problem (see below), but this would take a
very, very long while, as there are 6.67 10^21 different ones see
[Felgenhauer]_.

In the sudokus found in newspapers some numbers are already given, in such a
way that there is only one solution. We can add these filled in numbers by
adding additional constraints that restrict certain variables to just a single
value. Again this kind of constraint is already included in Constraining Order:

.. testcode::

    from constrainingorder.constraints import FixedValue

    cons.append(FixedValue(variables['x11'],1))
    cons.append(FixedValue(variables['x14'],8))
    cons.append(FixedValue(variables['x21'],6))
    cons.append(FixedValue(variables['x22'],3))
    cons.append(FixedValue(variables['x25'],5))
    cons.append(FixedValue(variables['x27'],9))
    cons.append(FixedValue(variables['x32'],9))
    cons.append(FixedValue(variables['x36'],3))
    cons.append(FixedValue(variables['x37'],5))
    cons.append(FixedValue(variables['x44'],2))
    cons.append(FixedValue(variables['x47'],6))
    cons.append(FixedValue(variables['x49'],3))
    cons.append(FixedValue(variables['x51'],3))
    cons.append(FixedValue(variables['x53'],2))
    cons.append(FixedValue(variables['x57'],1))
    cons.append(FixedValue(variables['x59'],7))
    cons.append(FixedValue(variables['x61'],9))
    cons.append(FixedValue(variables['x63'],8))
    cons.append(FixedValue(variables['x66'],6))
    cons.append(FixedValue(variables['x73'],6))
    cons.append(FixedValue(variables['x74'],5))
    cons.append(FixedValue(variables['x78'],7))
    cons.append(FixedValue(variables['x83'],9))
    cons.append(FixedValue(variables['x85'],6))
    cons.append(FixedValue(variables['x88'],2))
    cons.append(FixedValue(variables['x89'],5))
    cons.append(FixedValue(variables['x96'],8))
    cons.append(FixedValue(variables['x99'],9))

Space
-----

With the variables and the constraints we can set up a Space. A Space collects
all the variables and constraints, and keeps track of the possible values (the
domain) for each variable. We print the domain for the first few variables.

.. testcode::

    from constrainingorder import Space

    space = Space(variables.values(),cons)
    for vname, domain in sorted(space.domains.items())[:15]:
        print vname, domain

This outputs

.. testoutput::

    x11 {1,2,3,4,5,6,7,8,9}
    x12 {1,2,3,4,5,6,7,8,9}
    x13 {1,2,3,4,5,6,7,8,9}
    x14 {1,2,3,4,5,6,7,8,9}
    x15 {1,2,3,4,5,6,7,8,9}
    x16 {1,2,3,4,5,6,7,8,9}
    x17 {1,2,3,4,5,6,7,8,9}
    x18 {1,2,3,4,5,6,7,8,9}
    x19 {1,2,3,4,5,6,7,8,9}
    x21 {1,2,3,4,5,6,7,8,9}
    x22 {1,2,3,4,5,6,7,8,9}
    x23 {1,2,3,4,5,6,7,8,9}
    x24 {1,2,3,4,5,6,7,8,9}
    x25 {1,2,3,4,5,6,7,8,9}
    x26 {1,2,3,4,5,6,7,8,9}

A space can also tell us if a labelling (a dictionary with parameter names
and values) is consistent with the constraints or satisfies them.

Solution
--------

With the Space set up, we can now solve the CSP with backtracking, i.e. by
filling in a number into a field and then checking if this is consistent with
the constraints. If it is put a number into another field, if not, try another
number, or if all numbers have been tried, go back to the previous field and
try another number there.

This procedure can take a long time, as there are 9^81 possibilities that
have to be tried. One possibility to speed this up is to reduce the problem
space.  For some fields possible numbers  can be eliminated, as they are not
consistent with the posed constraints. For example if the value of a field is
fixed to 3, then its value can not be something else, and also the 3 can be
removed from the domain of the fields in the same row, column and block.

In the constraint satisfaction literature this is called problem reduction.
Constraining Order has an algorithm included for problem reduction called ac3, that does that.

.. testcode::

    from constrainingorder.solver import ac3

    ac3(space)
    for vname, domain in sorted(space.domains.items())[:15]:
        print vname, domain

Which now yields

.. testoutput::

    x11 {1}
    x12 {2,4,5,7}
    x13 {4,5,7}
    x14 {8}
    x15 {9,2,4,7}
    x16 {9,2,4,7}
    x17 {2,3,4,7}
    x18 {3,4,6}
    x19 {2,4,6}
    x21 {6}
    x22 {3}
    x23 {4,7}
    x24 {1,4,7}
    x25 {5}
    x26 {1,2,4,7}

We can see that the domains of the variables have been reduces dramatically,
which will speed up backtracking by a huge factor. Another thing that has a
big impact on the performance is the order in which the variables are tried.
In general one wants find conflicts as early as possible, as this eliminates
whole branches of the search tree at once. For the case of sudoku a columns
wise ordering (or row or blockwise) has proven to be effective.

Finally we can solve the sudoku by backtracking. The solve function is a
generator which iterates over all found solutions. In this case we only want
one, so break out of the loop after the first one is found.

.. testcode::

    from constrainingorder.solver import solve

    #column wise ordering
    ordering = []
    for i in numbers:
        for j in numbers:
            ordering.append('x%d%d' % (i,j))

    #find first solution and print it, then stop
    for solution in solve(space,method='backtrack',ordering=ordering):
        for i in numbers:
            for j in numbers:
                print solution['x%d%d' % (i,j)],
            print
        break

The output of the solution should look like this

.. testoutput::

    1 2 5 8 9 4 7 3 6
    6 3 7 1 5 2 9 4 8
    8 9 4 6 7 3 5 1 2
    4 5 1 2 8 7 6 9 3
    3 6 2 9 4 5 1 8 7
    9 7 8 3 1 6 2 5 4
    2 4 6 5 3 9 8 7 1
    7 8 9 4 6 1 3 2 5
    5 1 3 7 2 8 4 6 9

References
----------

.. [Felgenhauer]  Bertram Felgenhauer and Frazer Jarvis.  Enumerating possible sudoku grids. Technical report, 2005

