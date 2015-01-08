import unittest
from constrainingorder.sets import *
from constrainingorder.variables import *
from constrainingorder.constraints import *

class TestFixedValue(unittest.TestCase):
    def setUp(self):
        self.x = DiscreteVariable('x',domain=DiscreteSet([1,2,3,5]))
        self.y = RealVariable('y',domain=IntervalSet([Interval.open(1,2)]))
        self.cnst_x = FixedValue(self.x,1)
        self.cnst_y = FixedValue(self.y,1.4)
    def test_init(self):
        self.assertRaises(ValueError,lambda: FixedValue(self.x,8))
        self.assertRaises(ValueError,lambda: FixedValue(self.y,2))
    def test_satisfied(self):
        self.assertTrue(self.cnst_x.satisfied(dict(d=2,x=1)))
        self.assertFalse(self.cnst_x.satisfied(dict(d=2,x=2)))

        self.assertTrue(self.cnst_y.satisfied(dict(d=2,y=1.4)))
        self.assertFalse(self.cnst_y.satisfied(dict(d=2,y=2)))

    def test_consistent(self):
        self.assertTrue(self.cnst_x.consistent({}))
        self.assertTrue(self.cnst_y.consistent({}))

        self.assertTrue(self.cnst_x.consistent(dict(y=3)))
        self.assertTrue(self.cnst_y.consistent(dict(x=0)))

class TestAllDifferent(unittest.TestCase):
    def setUp(self):
        self.x = DiscreteVariable('x',domain=DiscreteSet([1,2,3,5]))
        self.y = DiscreteVariable('y',domain=DiscreteSet([1,2,3,5]))
        self.cnst = AllDifferent([self.x, self.y])

    def test_satisfied(self):
        self.assertTrue(self.cnst.satisfied(dict(x=2,y=1)))
        self.assertFalse(self.cnst.satisfied(dict(x=2,y=2)))

    def test_consistent(self):
        self.assertTrue(self.cnst.consistent({}))
        self.assertTrue(self.cnst.consistent(dict(x=2)))
        self.assertTrue(self.cnst.consistent(dict(x=2,y=3)))

class TestDomain(unittest.TestCase):
    def setUp(self):
        self.x = DiscreteVariable('x',domain=DiscreteSet([1,2,3,5]))
        self.cnst = Domain(self.x, DiscreteSet([1,3,7]))

    def test_satisfied(self):
        self.assertTrue(self.cnst.satisfied(dict(x=1)))
        self.assertFalse(self.cnst.satisfied(dict(x=2)))

    def test_consistent(self):
        self.assertTrue(self.cnst.consistent({}))
        self.assertTrue(self.cnst.consistent(dict(x=1)))
        self.assertFalse(self.cnst.consistent(dict(x=2)))

class TestRelations(unittest.TestCase):
    def setUp(self):
        self.x = RealVariable('x',domain=IntervalSet([Interval.open(0,1)]))
        self.y = RealVariable('y',domain=IntervalSet([Interval.open(0,1)]))

    def test_equal(self):
        cnst = Equal(self.x,self.y)
        self.assertTrue(cnst.satisfied(dict(x=0.4,y=0.4)))
        self.assertFalse(cnst.satisfied(dict(x=0.4,y=0.5)))

        self.assertTrue(cnst.consistent({}))
        self.assertTrue(cnst.consistent(dict(x=0.5)))

    def test_non_equal(self):
        cnst = NonEqual(self.x,self.y)
        self.assertTrue(cnst.satisfied(dict(x=0.4,y=0.5)))
        self.assertFalse(cnst.satisfied(dict(x=0.4,y=0.4)))

        self.assertTrue(cnst.consistent({}))
        self.assertTrue(cnst.consistent(dict(x=0.5)))

    def test_less(self):
        cnst = Less(self.x,self.y)
        self.assertTrue(cnst.satisfied(dict(x=0.4,y=0.5)))
        self.assertFalse(cnst.satisfied(dict(x=0.4,y=0.4)))

        self.assertTrue(cnst.consistent({}))
        self.assertTrue(cnst.consistent(dict(x=0.5)))

    def test_less_equal(self):
        cnst = LessEqual(self.x,self.y)
        self.assertTrue(cnst.satisfied(dict(x=0.4,y=0.5)))
        self.assertTrue(cnst.satisfied(dict(x=0.4,y=0.4)))
        self.assertFalse(cnst.satisfied(dict(x=0.5,y=0.4)))

        self.assertTrue(cnst.consistent({}))
        self.assertTrue(cnst.consistent(dict(x=0.5)))

    def test_greater(self):
        cnst = Greater(self.x,self.y)
        self.assertTrue(cnst.satisfied(dict(x=0.5,y=0.4)))
        self.assertFalse(cnst.satisfied(dict(x=0.4,y=0.5)))
        self.assertFalse(cnst.satisfied(dict(x=0.4,y=0.4)))

        self.assertTrue(cnst.consistent({}))
        self.assertTrue(cnst.consistent(dict(x=0.5)))

    def test_greater_equal(self):
        cnst = GreaterEqual(self.x,self.y)
        self.assertTrue(cnst.satisfied(dict(x=0.5,y=0.4)))
        self.assertTrue(cnst.satisfied(dict(x=0.4,y=0.4)))
        self.assertFalse(cnst.satisfied(dict(x=0.4,y=0.5)))

        self.assertTrue(cnst.consistent({}))
        self.assertTrue(cnst.consistent(dict(x=0.5)))

class TestDiscreteRelations(unittest.TestCase):
    def setUp(self):
        self.x = DiscreteVariable('x',domain=DiscreteSet(['a','b','c']))
        self.y = DiscreteVariable('y',domain=DiscreteSet([1,2,3]))

    def test_discrete(self):
        cnst = DiscreteBinaryRelation(self.x,self.y,[('a',1),('b',1),('c',3)])

        self.assertTrue(cnst.satisfied(dict(x='a',y=1)))
        self.assertFalse(cnst.satisfied(dict(x='a',y=2)))

        self.assertTrue(cnst.consistent({}))
        self.assertTrue(cnst.consistent(dict(y=1)))
        self.assertFalse(cnst.consistent(dict(y=2)))

