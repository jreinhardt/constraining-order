import pint
from itertools import tee,izip,product
from csp import IntervalSet, Constraint, DiscreteSet, Interval, Patch

ureg = pint.UnitRegistry()

class Parameter(object):
    """
    Abstract baseclass for parameters
    """
    def __init__(self,name,**kwargs):
        self.name = name
        "name of the parameter"
        self.description = kwargs.get('description')
        "description of the parameter"
        self.unit = kwargs.get('unit')
        "description of the parameter"
        self.domain = None
        self.discrete = None

class ContinuousParameter(Parameter):
    """
    Continuous real parameter
    """
    def __init__(self,name,**kwargs):
        Parameter.__init__(
            self,
            name,
            unit=kwargs.get('unit',''),
            description=kwargs.get('description','')
        )

        self.domain = kwargs.get('domain',IntervalSet.everything())
        self.discrete = False

class DiscreteParameter(Parameter):
    """
    Discrete parameter over a set of more or less arbitrary elements
    """
    def __init__(self,name,**kwargs):
        Parameter.__init__(
            self,
            name,
            unit=kwargs.get('unit',''),
            description=kwargs.get('description','')
        )

        self.domain = kwargs.get('domain',IntervalSet.everything())

        self.discrete = True

class DerivatorConstraint(Constraint):
    """
    Abstract base class for constraints that allow to uniquely derive the
    value for a parameter from zero or more other parameter values.

    This is a useful mechanism for parametercollection if no constraint
    satisfaction is available (e.g. in OpenSCAD)
    """
    def __init__(self,name,required,parameter_domains):
        Constraint.__init__(self,parameter_domains)
        self.name = name
        "name of the derivable parameter"
        self.required = required
        "list of parameters required for derivation"
    def requirements_fulfilled(self,pt):
        """
        return whether all requirements are fulfilled and derivation is
        possible
        """
        for pname in self.required:
            if not pname in pt:
                return False
        return True
    def derive(self,pt):
        """
        return the value for the parameter name derived from the values of
        the requirements in pt
        """
        raise NotImplementedError

class Literal(DerivatorConstraint):
    """
    Fix a parameter to a specific value
    """
    def __init__(self,name,value):
        DerivatorConstraint.__init__(self,name,[],{name:set([value])})
        self.name = name
        self.value = value

    def satisfied(self,pt):
        if self.name in pt:
            return pt[self.name] == self.value
        return False

    def consistent(self,pt):
        if self.name in pt:
            return self.satisfied(pt)
        return True

    def derive(self,pt):
        return self.value

class Table(DerivatorConstraint):
    def __init__(self,name,idx,data):
        DerivatorConstraint.__init__(self,name,[idx],{
            name : set(data.values()),
            idx : set(data.keys())
        })
        self.idx = idx
        self.data = data
        self.name = name

    def satisfied(self,pt):
        if not self.name in pt:
            return False
        if not self.idx in pt:
            return False
        return pt[self.name] == self.data[pt[self.idx]]

    def consistent(self,pt):
        if self.idx in pt and self.name in pt:
            return self.satisfied(pt)
        elif self.idx in pt:
            return pt[self.idx] in self.domain[self.idx]
        elif self.name in pt:
            return pt[self.name] in self.domain[self.name]
        else:
            return True

    def derive(self,pt):
        return self.data[pt[self.idx]]

class Table2D(DerivatorConstraint):
    def __init__(self,name,idx1,idx2,data):
        domains = {idx1 : set([]), idx2 : set([]), name : set([])}
        for i1,v1 in data.iteritems():
            domains[idx1].add(i1)
            for i2,v2 in v1.iteritems():
                domains[idx2].add(i2)
                domains[name].add(v2)
        DerivatorConstraint.__init__(self,name,[idx1,idx2],domains)

        self.name = name
        self.idx1 = idx1
        self.idx2 = idx2
        self.data = data

    def satisfied(self,pt):
        if not self.name in pt:
            return False
        if not self.idx1 in pt:
            return False
        if not self.idx2 in pt:
            return False
        return pt[self.name] == self.data[pt[self.idx1]][pt[self.idx2]]
    def consistent(self,pt):
        #in total 8 cases to consider for the three relevant parameters: none
        #given, all given, 3 cases for one given, 3 cases for two given
        if self.idx1 in pt:
            if self.idx2 in pt:
                if self.name in pt:
                    #idx1,idx2,name
                    return self.satisfied(pt)
                else:
                    #idx1,idx2
                    return pt[self.idx2] in self.domain[self.idx2] and\
                           pt[self.idx1] in self.domain[self.idx1]
            elif self.name in pt:
                #idx1,name
                for idx2 in self.domain[self.idx2]:
                    if not idx2 in self.data[pt[self.idx1]].keys():
                        return False
                    if pt[self.name] == self.data[pt[self.idx1]][idx2]:
                        return True
                else:
                    return False
            else:
                #idx1
                return pt[self.idx1] in self.domain[self.idx1]
        elif self.idx2 in pt:
            if self.name in pt:
                #idx2,name
                for idx1 in self.domain[self.idx1]:
                    if pt[self.name] == self.data[idx1][pt[self.idx2]]:
                        return True
                else:
                    return False
            else:
                #idx2
                return pt[self.idx2] in self.domain[self.idx2]
        elif self.name in pt:
            #name
            return pt[self.name] in self.domain[self.name]
        else:
            #nothing
            return True

    def derive(self,pt):
        return self.data[pt[self.idx1]][pt[self.idx2]]

class Alias(Constraint):
    def __init__(self,aliases,constraint):
        self.aliases = aliases
        self.reverse = dict(zip(aliases.values(),aliases.keys()))
        self.constraint = constraint
        Constraint.__init__(self,self._forward(constraint.domain))

    def _translate(self,point,map):
        """
        return translation of parameternames in point according to map
        """
        res = {}
        for pname,value in point.iteritems():
            if pname in map.values():
                raise KeyError("Parameter name collision %s" % pname)
            if pname in map:
                if map[pname] in res:
                    raise KeyError("Parameter name collision %s" % map[pname])
                res[map[pname]] = value
            else:
                if pname in res:
                    raise KeyError("Parameter name collision %s" % pname)
                res[pname] = value
        return res

    def _forward(self,point):
        return self._translate(point,self.aliases)

    def _back(self,point):
        return self._translate(point,self.reverse)

    def satisfied(self,point):
        print self._back(point)
        return self.constraint.satisfied(self._back(point))

    def consistent(self,point):
        return self.constraint.consistent(self._back(point))

    def derive(self,pt):
        return self.data[pt[self.idx]]

