Custom constraints
==================

Constraining Order is designed to make it easy to add custom constraints.
This tutorial will show this for the example of one of the most prominent
constraint satisfaction problems, the 8 queens problem.

8 queens problem
----------------

The task is to place 8 queens on a chessboard in such a way that no queen can
attack any other queen, i.e. no two queens occupy the same row, column or
same diagonals.

One way to model this is by using 8 variables, one for a queen in each
column. In this way, the requirement that there has to be one queen in every
column is already built in, which reduces the number of constraints and the
domain of the variables and improves performance.

As values for the variables we choose tuples with the actual coordinates on
the board, this makes it easier to formulate the diagonal constraints. We
name the variables with lowercase letter, the traditional naming schema of
the columns of a chess board. Coordinates will be zero indexed, as this is
more convenient in python.

.. testcode:: queens

    from constrainingorder.sets import DiscreteSet
    from constrainingorder.variables import DiscreteVariable

    variables = {}
    for i,col in enumerate('abcdefgh'):
        domain = DiscreteSet([(j,i) for j in range(8)])
        variables[col] = DiscreteVariable(col,domain=domain)

As we already built in the column constraint, it remains to express the row
and diagonal constraints. We will take care of all of them by creating a new
constraint type, a QueensConstraint:

.. testcode:: queens

    from constrainingorder.constraints import Constraint
    from itertools import product

    class QueensConstraint(Constraint):
        """
        Constraint that ensures that a number of queens on a chessboard can
        not attack each other
        """
        def __init__(self,queens):
            """
            Create a new Queens constraint.

            :param variable: Variables representing the position of queens on a chess board
            :type variable: list of DiscreteVariables
            """
            Constraint.__init__(self,dict((var,var.domain) for var in queens))

        def _conflict(self,val1,val2):
            #check for row conflict
            if val1[0] == val2[0]:
                return True
            #check for rising diagonal conflict
            if val1[0] - val1[1] == val2[0] - val2[1]:
                return True
            #check for falling diagonal conflict
            if val1[0] + val1[1] == val2[0] + val2[1]:
                return True
        def satisfied(self,lab):
            for v1,v2 in product(self.vnames,repeat=2):
                if v1 == v2:
                    continue
                if v1 not in lab or v2 not in lab:
                    return False
                if self._conflict(lab[v1],lab[v2]):
                    return False
            return True
        def consistent(self,lab):
            for v1,v2 in product(self.vnames,repeat=2):
                if v1 not in lab or v2 not in lab or v1 == v2:
                    continue
                if self._conflict(lab[v1],lab[v2]):
                    return False
            return True

A constraint needs to derive from the
:class:`~constrainingorder.constraints.Constraint` class and implement the
two methods `satisfied` and `consistent`.

In the constructor we pass a dictionary of variables and the values for them
which are consistent with this constraint. In this case, there is no field on
the board excluded a priori, so we use the full domain of the variable.

As both of the methods we have to implement check for conflicts between the
queens, it makes sense to write a small utility method that does this check
to avoid code duplication. It compares the first component of the tuples to
check for a row conflict. To check whether the two queens are on the same
diagonal, we compare the sum and difference of the row and column components.
It might not be obvious, but it is easy to check that fields with the same
sum or difference of rows and columns are on the same diagonal. Not that we don't check for column conflicts, as they are taken care of by the setup of our variables.

The `satisfied` method checks that the labelling (a dictionary with variable
names and values) assigns values to all variables affected by this
constraint, and that there are no conflicts. The parameter names of the
affected variables are accessible in the attribute
:attr:`~constrainingorder.constraints.Constraint.vnames`, that the Constraint
class sets up for us.

The `consistent` method is a bit weaker, as it just checks for conflicts, but
doesn't care about missing values. It allows the solution and reduction
algorithms to detect inconsistencies even if not all queens are placed yet.

And thats it. We can now use this constraint just like the in-built ones:

.. testcode:: queens

    from constrainingorder import Space
    from constrainingorder.solver import solve

    constraint = QueensConstraint(variables.values())
    space = Space(variables.values(),[constraint])


    for solution in solve(space,method='backtrack'):
        for i in range(8):
            for j in range(8):
                if (i,j) in solution.values():
                    print 'X',
                else:
                    print '.',
            print
        break

In contrast to the sudoku solver discussed in the :doc:`quickstart`, the 8 queens problem space can not be reduced, as no fields can be eliminated a priori, for every field there exist solutions where a queen occupies this field.

We also don't specify a variable ordering, as in this case the total number of variables is rather low, and solution is quick in any case.

.. testoutput:: queens

    X . . . . . . .
    . . . . . X . .
    . . . . . . . X
    . . X . . . . .
    . . . . . . X .
    . . . X . . . .
    . X . . . . . .
    . . . . X . . .


Custom Binary relations
-----------------------

A riddle from this weeks newspaper:

  Professor Knooster is visiting Shroombia. The people of Shroombia is
  divided into two groups, the shrimpfs that always lie and the wex that
  always tell the truth. For his research the professor asked 10 Shroombians
  about their groups. The answers:

  * Zeroo: Onesy is a shrimpf
  * Onesy: Threesy is a shrimpf
  * Twoo: Foursy is a shrimpf
  * Threesy: Sixee is a shrimpf
  * Foursy: Seveen is a shrimpf
  * Fivsy: Ninee is a shrimpf
  * Sixee: Twoo is a shrimpf
  * Seveen: Eightsy is a shrimpf
  * Eightsy: Fivsy is a shrimpf

  The professor sighed: "I will never find out who is in which group if you
  continue like this." Then the last Shroombian answered

  * Ninee: Zeroo and Sixee belong to different groups

This riddle can be modelled as a CSP, and it gives the opportunity to discuss a special kind of constraint, namely binary relations.

First set up the variables

.. testcode:: shroombia

   from constrainingorder.variables import DiscreteVariable
   from constrainingorder.sets import DiscreteSet

   domain = DiscreteSet(['Shrimpf','Wex'])
   variables = []
   for i in range(10):
       variables.append(DiscreteVariable(str(i),domain=domain))

So every variable represents one Shroombian, who can be either a shrimpf or a wex.

Almost all hints are of the same structure: one Shroombian accuses another
Shroombian of being a shrimpf. The hint is fulfilled either if the accusing
shroombian is a Shrimpf (who is always lying) and the accused shroombian is
not actually a Shrimpf, or if the accusor is a Wex (who is always telling the
truth) and the accused is a in fact a Shrimpf.

We can represent this in form of a custom constraint. As each hint affects
two shroombians, such constraints are binary relations. The implementation of
binary relations is much simpler than for general constraints.

.. testcode:: shroombia

   from constrainingorder.constraints import BinaryRelation

   class Accusation(BinaryRelation):
       def relation(self,val1,val2):
           return (val1 == 'Shrimpf' and val2 == 'Wex') or\
                  (val1 == 'Wex' and val2 == 'Shrimpf')

For classes derived from BinaryRelations it suffices to implement a single
method that returns True if the two values fulfill the relation and False
otherwise. Specific constraints are obtained by instantiating this class with two variables.

For DiscreteVariables with small domains one can represent binary relations also by listing all tuples of values that fulfill the relation. An equivalent implementation would be derived from DiscreteBinaryRelation.

.. testcode:: shroombia2

   from constrainingorder.constraints import DiscreteBinaryRelation

   class Accusation(DiscreteBinaryRelation):
       def __init__(self,var1,var2):
           DiscreteBinaryRelation.__init__(self,var1,var2,[
               ('Shrimpf','Wex'), ('Wex','Shrimpf')
           ])

In addition we need to implement a new constraint for the last hint. As it affects three shroombians, this is not a binary relation.

.. testcode:: shroombia

   from constrainingorder.constraints import Constraint
   class AllegedNonEqual(Constraint):
       def __init__(self,var1,var2,var3):
           Constraint.__init__(self,{
               var1 : var1.domain,
               var2 : var2.domain,
               var3 : var3.domain}
           )
           self.v1 = var1.name
           self.v2 = var2.name
           self.v3 = var3.name

       def satisfied(self,lab):
           if not (self.v1 in lab and self.v2 in lab and self.v3 in lab):
               return False
           elif lab[self.v1] == 'Shrimpf':
               return lab[self.v2] == lab[self.v3]
           elif lab[self.v1] == 'Wex':
               return lab[self.v2] != lab[self.v3]

       def consistent(self,lab):
           if not (self.v1 in lab and self.v2 in lab and self.v3 in lab):
               return True
           elif lab[self.v1] == 'Shrimpf':
               return lab[self.v2] == lab[self.v3]
           elif lab[self.v1] == 'Wex':
               return lab[self.v2] != lab[self.v3]

Now we can specify the constraints

.. testcode:: shroombia

   cons = []
   cons.append(Accusation(variables[0],variables[1]))
   cons.append(Accusation(variables[1],variables[3]))
   cons.append(Accusation(variables[2],variables[4]))
   cons.append(Accusation(variables[3],variables[6]))
   cons.append(Accusation(variables[4],variables[7]))
   cons.append(Accusation(variables[5],variables[9]))
   cons.append(Accusation(variables[6],variables[2]))
   cons.append(Accusation(variables[7],variables[8]))
   cons.append(Accusation(variables[8],variables[5]))

   cons.append(AllegedNonEqual(variables[9],variables[0],variables[6]))

And solve the problem

.. testcode:: shroombia

    from constrainingorder import Space
    from constrainingorder.solver import solve

    space = Space(variables,cons)

    for solution in solve(space,method='backtrack'):
        for name, group in sorted(solution.items()):
            print name, group

.. testoutput:: shroombia

    0 Shrimpf
    1 Wex
    2 Shrimpf
    3 Shrimpf
    4 Wex
    5 Shrimpf
    6 Wex
    7 Shrimpf
    8 Wex
    9 Wex

