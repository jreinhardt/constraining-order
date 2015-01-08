"""
This module defines common stuff for constraint satisfaction probleme
"""

class Space(object):
    """
    A space is a description of all the computation space for a specific csp
    """
    def __init__(self,variables, constraints):
        """
        variables is a list of Variables
        constraints is a list of Constraints
        """
        self.constraints = constraints
        "list of constraints"
        self.variables = {}
        "dictionary of variable names to variable instances"
        self.domains = {}
        "dictionary of variable names to DiscreteSet/IntervalSet"
        for var in variables:
            self.variables[var.name] = var
            self.domains[var.name] = var.domain

    def is_discrete(self):
        """
        Return whether this space is discrete
        """
        for domain in self.domains.values():
            if not domain.is_discrete():
                return False
        return True
    def consistent(self,lab):
        """
        Check whether the labeling is consistent with all constraints
        """
        for const in self.constraints:
            if not const.consistent(lab):
                return False
        return True
    def satisfied(self,lab):
        """
        Check whether the labeling satisfies all constraints
        """
        for const in self.constraints:
            if not const.satisfied(lab):
                return False
        return True
