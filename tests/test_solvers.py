import unittest
from sys import float_info
from constrainingorder import Space
from constrainingorder.solver import solve, _unary, _binary
from constrainingorder.sets import *
from constrainingorder.variables import *
from constrainingorder.constraints import *

class TestSolvers(unittest.TestCase):
    def setUp(self):
        self.x = DiscreteVariable('x',domain=DiscreteSet([1,2,3,5]))
        self.y = DiscreteVariable('y',domain=DiscreteSet(['a','b','c']))
        self.z = DiscreteVariable('z',domain=DiscreteSet([1,2,3,5]))
    def test_empty(self):
        space = Space([self.x,self.y],[])
        self.assertEqual(len(list(solve(space,method='backtrack'))),12)
        self.assertEqual(len(list(solve(space,method='ac-lookahead'))),12)

    def test_all_different(self):
        space = Space([self.x,self.z],[AllDifferent([self.x,self.z])])
        self.assertEqual(len(list(solve(space,method='backtrack'))),12)
        self.assertEqual(len(list(solve(space,method='ac-lookahead'))),12)

    def test_equal(self):
        space = Space([self.x,self.z],[Equal(self.x,self.z)])
        self.assertEqual(len(list(solve(space,method='backtrack'))),4)
        self.assertEqual(len(list(solve(space,method='ac-lookahead'))),4)

    def test_less(self):
        space = Space([self.x,self.z],[Less(self.x,self.z)])
        self.assertEqual(len(list(solve(space,method='backtrack'))),6)
        self.assertEqual(len(list(solve(space,method='ac-lookahead'))),6)

    def test_equal_domain(self):
        space = Space([self.x,self.z],[
            Equal(self.x,self.z),
            Domain(self.x,DiscreteSet([1,3,6]))
        ])
        self.assertEqual(len(list(solve(space,method='backtrack'))),2)
        self.assertEqual(len(list(solve(space,method='ac-lookahead'))),2)

class TestNodeConsistencyReduction(unittest.TestCase):
    def setUp(self):
        self.x = DiscreteVariable('x',domain=DiscreteSet([1,2,3,5]))
        self.y = DiscreteVariable('y',domain=DiscreteSet(['a','b','c']))
        self.z = RealVariable('z',domain=IntervalSet([Interval.closed(0,10)]))
        self.x2 = DiscreteVariable('x2',domain=DiscreteSet([1,2,3,6]))
        self.variables = [self.x,self.y,self.z,self.x2]

    def test_fixed_value(self):
        cnst = FixedValue(self.x,3)
        space = Space(self.variables,[cnst])
        _unary(space,cnst,'x')
        self.assertEqual(len(space.domains['x'].elements),1)

    def test_domain(self):
        cnst = Domain(self.z,IntervalSet([Interval.closed(3,5)]))
        space = Space(self.variables,[cnst])
        _unary(space,cnst,'z')
        self.assertEqual(len(space.domains['z'].ints),1)
        self.assertEqual(space.domains['z'].ints[0].bounds,(3,5))

    def test_discrete_binary_relation(self):
        cnst = DiscreteBinaryRelation(self.x,self.y,[(1,'a'),(3,'b'),(2,'b')])
        space = Space(self.variables,[cnst])
        _unary(space,cnst,'x')
        self.assertEqual(len(space.domains['x'].elements),3)
        _unary(space,cnst,'y')
        self.assertEqual(len(space.domains['y'].elements),2)

    def test_equality(self):
        cnst = Equal(self.x,self.x2)
        space = Space(self.variables,[cnst])
        _unary(space,cnst,'x')
        self.assertEqual(len(space.domains['x'].elements),3)
        _unary(space,cnst,'x2')
        self.assertEqual(len(space.domains['x2'].elements),3)

class TestArcConsistencyReduction(unittest.TestCase):
    def setUp(self):
        self.x = DiscreteVariable('x',domain=DiscreteSet([1,2,3,5]))
        self.y = DiscreteVariable('y',domain=DiscreteSet(['a','b','c']))
        self.z = DiscreteVariable('z',domain=DiscreteSet([1,2,3,5,6]))
        self.variables = [self.x,self.y,self.z]

    def test_all_different(self):
        cnst = AllDifferent([self.x,self.y])
        space = Space(self.variables,[cnst])
        _unary(space,cnst,'x')
        _unary(space,cnst,'y')
        #Nothing can be reduced here
        self.assertFalse(_binary(space,cnst,'x','y'))
        self.assertFalse(_binary(space,cnst,'y','x'))

    def test_greater(self):
        cnst = Greater(self.x,self.z)
        space = Space(self.variables,[cnst])
        _unary(space,cnst,'x')
        _unary(space,cnst,'z')
        self.assertTrue(_binary(space,cnst,'x','z'))
        self.assertEqual(len(space.domains['x'].elements),3)
        self.assertTrue(_binary(space,cnst,'z','x'))
        self.assertEqual(len(space.domains['z'].elements),3)

    def test_discrete_relation(self):
        cnst = DiscreteBinaryRelation(self.x,self.y,[(1,'a'),(1,'b'),(2,'c')])
        cnst2 = FixedValue(self.x,1)
        space = Space(self.variables,[cnst])
        _unary(space,cnst,'x')
        _unary(space,cnst,'y')
        _unary(space,cnst2,'x')
        self.assertFalse(_binary(space,cnst,'x','y'))
        self.assertTrue(_binary(space,cnst,'y','x'))
        self.assertEqual(len(space.domains['y'].elements),2)
