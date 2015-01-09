"""
This module defines classes describing constraints on variables
"""
from constrainingorder.sets import DiscreteSet, IntervalSet
from itertools import product

class Constraint(object):
    def __init__(self,domains):
        self.vnames = [v.name for v in domains.keys()]
        "Names of the variables affected by this constraint"
        self.domains = {}
        "Domains imposed by node consistency for this constraint"
        for var,dom in domains.iteritems():
            self.domains[var.name] = dom
    def satisfied(self,lab):
        """
        return whether the labeling satisfies this constraint
        """
        raise NotImplementedError
    def consistent(self,lab):
        """
        returns whether the labeling is consistent with this constraint
        """
        raise NotImplementedError

class FixedValue(Constraint):
    """
    Constraint that fixes a variable to a value
    """
    def __init__(self,variable,value):
        if not value in variable.domain:
            raise ValueError("Value %s is incompatible with domain of %s" % 
                             (str(value),variable.name))
        if variable.discrete:
            domain = {variable : DiscreteSet([value])}
        else:
            domain = {variable : IntervalSet.from_values([value])}
        Constraint.__init__(self,domain)

        self.name = variable.name
        self.value = value

    def satisfied(self,lab):
        if self.name in lab:
            return lab[self.name] == self.value
        return False

    def consistent(self,lab):
        if self.name in lab:
            return self.satisfied(lab)
        return True

class AllDifferent(Constraint):
    """
    Constraint enforcing different values between a list of variables
    """
    def __init__(self,variables):
        Constraint.__init__(self,dict((v,v.domain) for v in variables))
    def satisfied(self,lab):
        for v1,v2 in product(self.vnames,repeat=2):
            if v1 not in lab or v2 not in lab:
                return False
            if v1 == v2:
                continue
            if lab[v1] == lab[v2]:
                return False
        return True
    def consistent(self,lab):
        for v1,v2 in product(self.vnames,repeat=2):
            if v1 not in lab or v2 not in lab or v1 == v2:
                continue
            if lab[v1] == lab[v2]:
                return False
        return True

class Domain(Constraint):
    """
    Constraint that ensures that value of a variable falls into a given
    domain
    """
    def __init__(self,variable,domain):
        """
        domain: IntervalSet or DiscreteSet
        """
        Constraint.__init__(self,{variable:domain})
    def satisfied(self,lab):
        for v in self.vnames:
            if v not in lab:
                return False
            if not lab[v] in self.domains[v]:
                return False
        return True
    def consistent(self,lab):
        for v in self.vnames:
            if v not in lab:
                continue
            if not lab[v] in self.domains[v]:
                return False
        return True

class BinaryRelation(Constraint):
    """
    Abstract Base class for constraint the describe a binary relation between
    two variables.
    """
    def __init__(self,var1,var2):
        Constraint.__init__(self,{var1:var1.domain,var2:var2.domain})
        self.v1 = var1.name
        self.v2 = var2.name
    def satisfied(self,lab):
        for v in self.vnames:
            if v not in lab:
                return False
            elif not lab[v] in self.domains[v]:
                return False
        return self.relation(lab[self.v1],lab[self.v2])
    def consistent(self,lab):
        incomplete = False
        for v in self.vnames:
            if v not in lab:
                incomplete = True
                continue
            elif not lab[v] in self.domains[v]:
                return False
        if incomplete:
            return True
        return self.relation(lab[self.v1],lab[self.v2])

class Equal(BinaryRelation):
    def __init__(self,var1,var2):
        BinaryRelation.__init__(self,var1,var2)
        #for equality, something can be said about the domains
        domain = var1.domain.intersection(var2.domain)
        self.domains[var1.name] = domain
        self.domains[var2.name] = domain
    def relation(self,val1,val2):
        return val1 == val2

class NonEqual(BinaryRelation):
    def relation(self,val1,val2):
        return val1 != val2

class Less(BinaryRelation):
    def relation(self,val1,val2):
        return val1 < val2

class LessEqual(BinaryRelation):
    def relation(self,val1,val2):
        return val1 <= val2

class Greater(BinaryRelation):
    def relation(self,val1,val2):
        return val1 > val2

class GreaterEqual(BinaryRelation):
    def relation(self,val1,val2):
        return val1 >= val2

class DiscreteBinaryRelation(Constraint):
    """
    General binary relation between discrete variables represented by the
    tuples that are in this relation
    """
    def __init__(self,var1,var2,tuples):
        """
        tuples: list of tuples
        """
        dom1 = DiscreteSet([t[0] for t in tuples])
        dom2 = DiscreteSet([t[1] for t in tuples])
        Constraint.__init__(self,{var1:dom1,var2:dom2})
        self.v1 = var1.name
        self.v2 = var2.name
        self.tuples = tuples
    def satisfied(self,lab):
        for v in self.vnames:
            if v not in lab:
                return False
        return (lab[self.v1],lab[self.v2]) in self.tuples
    def consistent(self,lab):
        incomplete = False
        for v in self.vnames:
            if v not in lab:
                incomplete = True
                continue
            elif not lab[v] in self.domains[v]:
                return False
        if incomplete:
            return True
        return (lab[self.v1],lab[self.v2]) in self.tuples
