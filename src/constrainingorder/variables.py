from sets import DiscreteSet, IntervalSet

class Variable(object):
    """
    Abstract baseclass for variables.

    Variables are immutable.
    """
    def __init__(self,name,**kwargs):
        self.name = name
        "name of the variable"
        self.description = kwargs.get('description')
        "description of the variable"
        self.unit = kwargs.get('unit')
        "unit of the variable"
        self.domain = None
        "domain of the variable"
        self.discrete = None
        "if the variable is discrete or continuous"

class RealVariable(Variable):
    """
    Continuous real variable with values from the real numbers.
    """
    def __init__(self,name,**kwargs):
        Variable.__init__(
            self,
            name,
            unit=kwargs.get('unit',''),
            description=kwargs.get('description','')
        )

        self.domain = kwargs.get('domain',IntervalSet.everything())
        self.discrete = False

class DiscreteVariable(Variable):
    """
    Discrete variable with values from a set of discrete elements.
    """
    def __init__(self,name,**kwargs):
        Variable.__init__(
            self,
            name,
            unit=kwargs.get('unit',''),
            description=kwargs.get('description','')
        )

        self.domain = kwargs.get('domain',DiscreteSet.everything())

        self.discrete = True
