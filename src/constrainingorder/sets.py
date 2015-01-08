"""
This module defines datastructures to represent discrete and real sets in one
and more dimensions
"""

from itertools import tee,izip,product

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

class Interval(object):
    """
        Interval on real axis.
    """
    def __init__(self,bounds,included):
        """
            bounds: tuple with left and right bound
            included: whether the corresponding boundary value should be
            included in the interval
        """
        self.bounds = tuple(bounds)
        self.included = tuple(included)

    @classmethod
    def everything(cls):
        return cls((-float("inf"),float("inf")),(True,True))

    @classmethod
    def from_value(cls,value):
        return cls((value,value),(True,True))

    @classmethod
    def open(cls,a,b):
        return cls((a,b),(False,False))

    @classmethod
    def closed(cls,a,b):
        return cls((a,b),(True,True))

    @classmethod
    def leftopen(cls,a,b):
        return cls((a,b),(False,True))

    @classmethod
    def rightopen(cls,a,b):
        return cls((a,b),(True,False))

    def is_disjoint(self,other):
        if self.is_empty() or other.is_empty():
            return True

        if self.bounds[0] < other.bounds[0]:
            i1,i2 = self,other
        elif self.bounds[0] > other.bounds[0]:
            i2,i1 = self,other
        else:
            #coincident lower bounds
            if self.is_discrete() and not other.included[0]:
                return True
            elif other.is_discrete() and not self.included[0]:
                return True
            else:
                return False

        return not i2.bounds[0] in i1

    def _difference(self,other):
        #the set of intervals is not closed w.r.t the difference, as it might
        #yield 0,1 or two intervals as a result. Therefore only use this as a
        #utility function for IntervalSet, which doesn't suffer from this.

        if self.is_empty():
            return []

        if other.is_empty() or self.is_disjoint(other):
            return [self]

        b1 = (self.bounds[0],other.bounds[0])
        i1 = (self.included[0],not other.included[0])
        int1 = Interval(b1,i1)

        b2 = (other.bounds[1],self.bounds[1])
        i2 = (not other.included[1],self.included[1])
        int2 = Interval(b2,i2)

        if other.bounds[0] in self and other.bounds[1] in self:
            #-------
            # ***
            return [int1,int2]

        elif other.bounds[0] in self:
            bounds = (self.bounds[0],other.bounds[0])
            include = (self.included[0],not other.included[0])
            #-------
            # *********
            return [int1]
        elif other.bounds[1] in self:
            #    -------
            #*******
            return [int2]
        else:
            raise RuntimeError("This should not happen")

    def intersection(self,other):
        if self.bounds[0] < other.bounds[0]:
            i1,i2 = self,other
        else:
            i2,i1 = self,other

        if self.is_disjoint(other):
            return Interval((1,0),(True,True))

        bounds = [None,None]
        included = [None,None]
        #sets are not disjoint, so i2.bounds[0] in i1:
        bounds[0] = i2.bounds[0]
        included[0] = i2.included[0]

        if i2.bounds[1] in i1:
            bounds[1] = i2.bounds[1]
            included[1] = i2.included[1]
        else:
            bounds[1] = i1.bounds[1]
            included[1] = i1.included[1]

        return Interval(bounds,included)

    def is_empty(self):
        if self.bounds[1] < self.bounds[0]:
            return True
        if self.bounds[1] == self.bounds[0]:
            return not (self.included[0] and self.included[1])

    def is_discrete(self):
        return self.bounds[1] == self.bounds[0] and\
               self.included == (True,True)

    def get_point(self):
        if not self.is_discrete():
            raise ValueError("Interval doesn't contain exactly one value")
        return self.bounds[0]

    def __contains__(self,x):
        if self.is_empty():
            return False
        if self.included[0]:
            if not (x >= self.bounds[0]):
                return False
        else:
            if not (x > self.bounds[0]):
                return False
        if self.included[1]:
            if not (x <= self.bounds[1]):
                return False
        else:
            if not (x < self.bounds[1]):
                return False
        return True

    def __repr__(self):
        return str(self)

    def __str__(self):
        if self.is_empty():
            return "<empty set>"
        else:
            left = ["(","["]
            right = [")","]"]

            bnd = "%s,%s" % self.bounds
            brk = (left[self.included[0]],right[self.included[1]])

            return "%s%s%s" % (brk[0],bnd,brk[1])

class IntervalSet(object):
    """
    A set of intervals to represent quite general sets in R
    """
    def __init__(self,ints):
        self.ints = []
        for i in sorted(ints,key=lambda x: x.bounds[0]):
            if i.is_empty():
                continue
            self.ints.append(i)

        for i1,i2 in pairwise(self.ints):
            if not i1.is_disjoint(i2):
                raise ValueError('Intervals are not disjoint')

    @classmethod
    def everything(cls):
        return cls([Interval.everything()])

    @classmethod
    def from_values(cls,values):
        return cls([Interval.from_value(v) for v in values])

    def is_empty(self):
        return len(self.ints) == 0

    def is_discrete(self):
        for i in self.ints:
            if not i.is_discrete():
                return False
        return True

    def iter_members(self):
        if not self.is_discrete():
            raise ValueError("non-discrete IntervalSet can not be iterated")
        for i in self.ints:
            yield i.get_point()

    def intersection(self,other):
        res = []
        for i1 in self.ints:
            for i2 in other.ints:
                res.append(i1.intersection(i2))

        return IntervalSet(res)

    def difference(self,other):
        res = IntervalSet.everything()
        for j in other.ints:
            tmp = []
            for i in self.ints:
                tmp.extend(i._difference(j))
            res = res.intersection(IntervalSet(tmp))
        return res

    def __contains__(self,x):
        for interval in self.ints:
            if x in interval:
                return True
        return False

    def __str__(self):
        if self.is_empty():
            return "<empty interval set>"
        else:
            return " u ".join(str(i) for i in self.ints)

class DiscreteSet(object):
    """
    A set data structure for hashable elements

    This is a wrapper around pythons set type, which additionally provides the
    possibility to express the set of everything (which only makes sense
    sometimes).
    """
    def __init__(self,elements):
        self.everything = False
        self.elements = set(elements)

    @classmethod
    def everything(cls):
        res = cls([])
        res.everything = True
        return res

    def is_empty(self):
        if self.everything:
            return False
        return len(self.elements) == 0

    def is_discrete(self):
        return not self.everything

    def intersection(self,other):
        if self.everything:
            if other.everything:
                return DiscreteSet()
            else:
                return DiscreteSet(other.elements)
        else:
            if other.everything:
                return DiscreteSet(self.elements)
            else:
                return DiscreteSet(self.elements.intersection(other.elements))

    def difference(self,other):
        if self.everything:
            raise ValueError("Can not remove from everything")
        elif other.everything:
            return DiscreteSet([])
        else:
            return DiscreteSet(self.elements.difference(other.elements))

    def iter_members(self):
        if self.everything:
            raise ValueError("Can not iterate everything")
        for coord in self.elements:
            yield coord

    def __contains__(self,element):
        if self.everything:
            return True
        return element in self.elements

    def __str__(self):
        if self.is_empty():
            return "<empty discrete set>"
        else:
            return "{%s}" % ",".join(str(e) for e in self.elements)


class Patch(object):
    def __init__(self,sets):
        """
        A patch of multidimensional parameter space

        sets is a dict of names to DiscreteSet or IntervalSets of feasible values and
        represents the cartesion product of these
        """
        self.sets = sets
        self.discrete = True
        self.empty = False
        for s in sets.values():
            if isinstance(s,IntervalSet) and not s.is_discrete():
                self.discrete = False
            if s.is_empty():
                self.empty = True

    def is_empty(self):
        return self.empty

    def is_discrete(self):
        return self.discrete

    def intersection(self,other):
        "intersection with another patch"
        res = {}
        if set(self.sets.keys()) != set(other.sets.keys()):
            raise KeyError('Incompatible patches in intersection')
        for name,s1 in self.sets.iteritems():
            s2 = other.sets[name]
            res[name] = s1.intersection(s2)
        return Patch(res)

    def iter_points(self):
        "returns a list of tuples of names and values"
        if not self.is_discrete():
            raise ValueError("Patch is not discrete")
        names = sorted(self.sets.keys())
        icoords = [self.sets[name].iter_members() for name in names]
        for coordinates in product(*icoords):
            yield tuple(zip(names,coordinates))

    def __contains__(self,point):
        for name, coord in point.iteritems():
            if not coord in self.sets[name]:
                return False
        return True

    def __str__(self):
        if self.is_empty():
            return "<empty patch>"
        else:
            sets = ["%s:%s" % (n,str(i)) for n,i in self.sets.iteritems()]
            return " x ".join(sets)

class PatchSet(object):
    """
    A list of patches that represents quite general subsets of a
    multidimensional parameter space
    """
    def __init__(self,patches):
        self.discrete = True
        self.patches = []
        self.coords = None
        for patch in patches:
            if patch.is_empty():
                continue
            if not patch.is_discrete():
                self.discrete = False
            self.patches.append(patch)

    def is_empty(self):
        return len(self.patches) == 0

    def is_discrete(self):
        return self.discrete

    def intersection(self,other):
        res = []
        for p1 in self.patches:
            for p2 in other.patches:
                res.append(p1.intersection(p2))
        return PatchSet(res)

    def iter_points(self):
        if not self.discrete:
            raise ValueError('cannot iter points in non-discrete domain')
        if self.coords is None:
            self.coords = set([])
            for patch in self.patches:
                for point in patch.iter_points():
                    self.coords.add(point)
        for coord in self.coords:
            yield coord

    def __contains__(self,point):
        for patch in self.patches:
            if point in patch:
                return True
        return False

    def __str__(self):
        if self.is_empty():
            return "<empty interval set>"
        else:
            return "{ %s }" % " u ".join(str(i) for i in self.ints)

