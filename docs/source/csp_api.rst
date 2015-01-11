Constraint Satisfaction
=======================

Variables
---------

Variables are derived from a common baseclass

.. autoclass:: constrainingorder.variables.Variable
   :members:

Constrainingorder at the moment contains two types of Variables, DiscreteVariables and RealVariables

.. autoclass:: constrainingorder.variables.DiscreteVariable
   :members:
   :special-members: __init__

.. autoclass:: constrainingorder.variables.RealVariable
   :members:
   :special-members: __init__

Constraints
-----------

Constraints are derived from a common baseclass

.. autoclass:: constrainingorder.constraints.Constraint
   :members:

Constrainingorder ships with a selection of constraints, but it is easy to add custom ones

.. autoclass:: constrainingorder.constraints.FixedValue
   :members:
   :special-members: __init__

.. autoclass:: constrainingorder.constraints.AllDifferent
   :members:
   :special-members: __init__

.. autoclass:: constrainingorder.constraints.Domain
   :members:
   :special-members: __init__

Binary relations are an important class of constraints. In Constraining Order
they are derived from a common baseclass. New binary relations only need to implement the relation function. These relations can be used on Variables with values that offer the corresponding relations in the python data model.

.. autoclass:: constrainingorder.constraints.BinaryRelation
   :members:
   :special-members: __init__

Constraining Order ships with the standard relations.

.. autoclass:: constrainingorder.constraints.Equal

.. autoclass:: constrainingorder.constraints.NonEqual

.. autoclass:: constrainingorder.constraints.Less

.. autoclass:: constrainingorder.constraints.LessEqual

.. autoclass:: constrainingorder.constraints.Greater

.. autoclass:: constrainingorder.constraints.GreaterEqual

For DiscreteVariables, another way to represent relations is by the set of
tuples that are fulfilling this relation. This is represented by the
DiscreteBinaryRelation constraint

.. autoclass:: constrainingorder.constraints.DiscreteBinaryRelation
   :members:
   :special-members: __init__


Space
-----

.. autoclass:: constrainingorder.Space
   :members:
   :special-members: __init__

Solvers
-------

To obtain one or all solutions to a CSP, one needs to use a solver. Solvers operate on a space. For good performance it might be good to reduce the problem space first.

.. autofunction:: constrainingorder.solver.ac3

.. autofunction:: constrainingorder.solver.solve

