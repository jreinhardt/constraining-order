import unittest
from constrainingorder.sets import *
from sys import float_info

class IntervalTest(unittest.TestCase):
    def test_init(self):
        i = Interval.from_value(2.4)
        self.assertTrue(i.is_discrete())
        self.assertFalse(i.is_empty())
    def test_membership(self):
        op = (False,False)
        cl = (True,True)
        ho = (False,True)
        self.assertTrue( 2 in Interval((0,3),op))
        self.assertFalse(3 in Interval((0,3),op))
        self.assertFalse(0 in Interval((0,3),op))

        self.assertTrue( 2 in Interval((0,3),cl))
        self.assertTrue( 3 in Interval((0,3),cl))
        self.assertTrue( 0 in Interval((0,3),cl))

        self.assertTrue( 2 in Interval((0,3),ho))
        self.assertFalse(0 in Interval((0,3),ho))
        self.assertTrue( 3 in Interval((0,3),ho))

    def test_emptyness(self):
        op = (False,False)
        cl = (True,True)
        ho = (False,True)

        self.assertFalse(Interval((0,1),op).is_empty())
        self.assertFalse(Interval((0,1),cl).is_empty())
        self.assertFalse(Interval((0,1),ho).is_empty())

        self.assertTrue(Interval((1,0),op).is_empty())
        self.assertTrue(Interval((1,0),cl).is_empty())
        self.assertTrue(Interval((1,0),ho).is_empty())

        self.assertTrue(Interval((1,1),op).is_empty())
        self.assertFalse(Interval((1,1),cl).is_empty())
        self.assertTrue(Interval((1,1),ho).is_empty())

    def test_discrete(self):
        op = (False,False)
        cl = (True,True)
        ho = (False,True)

        self.assertFalse(Interval((0,1),(op)).is_discrete())
        self.assertFalse(Interval((0,1),(cl)).is_discrete())

        self.assertTrue(Interval((0,0),(cl)).is_discrete())
        self.assertFalse(Interval((0,0),(op)).is_discrete())

        self.assertFalse(Interval((1,0),(op)).is_discrete())
        self.assertFalse(Interval((1,0),(cl)).is_discrete())

    def test_disjoint(self):
        op = (False,False)
        cl = (True,True)
        ho = (False,True)

        self.assertTrue(Interval((0,1),op).is_disjoint(Interval((1,2),op)))
        self.assertFalse(Interval((0,1),cl).is_disjoint(Interval((1,2),cl)))

        #empty sets
        self.assertTrue(Interval((0,3),op).is_disjoint(Interval((2,1),op)))

        self.assertFalse(Interval((0,3),op).is_disjoint(Interval((2,4),op)))

        #boundary boundary cases
        self.assertFalse(Interval((0,3),cl).is_disjoint(Interval((0,4),op)))

        #disjoint points
        i = Interval.from_value(2.1).is_disjoint(Interval.from_value(2.3))
        self.assertTrue(i)

    def test_intersection(self):
        op = (False,False)
        cl = (True,True)
        ho = (False,True)

        #completely contained
        i = Interval((0,5),op).intersection(Interval((1,3),ho))
        self.assertEqual(i.included,ho)
        self.assertEqual(i.bounds,(1,3))

        #disjoint
        i = Interval((0,2),op).intersection(Interval((3,3),ho))
        self.assertTrue(i.is_empty())

        #empty set
        i = Interval((0,0),op).intersection(Interval((3,3),ho))
        self.assertTrue(i.is_empty())

        #point result
        i = Interval((0,2),cl).intersection(Interval((2,4),cl))
        self.assertTrue(i.is_discrete())

        #some random cases
        i = Interval((0,2.3),ho).intersection(Interval((1.5,6),cl))
        self.assertEqual(i.included,(True,True))
        self.assertEqual(i.bounds,(1.5,2.3))

    def test_difference(self):
        op = (False,False)
        cl = (True,True)
        ho = (False,True)

        #disjoint
        i = Interval((0,5),op)._difference(Interval((8,19),ho))
        self.assertTrue(len(i) == 1)

        #empty set
        i = Interval((0,5),op)._difference(Interval((5,0),op))
        self.assertEqual(len(i),1)
        self.assertEqual(i[0].bounds,(0,5))

        i = Interval((5,0),op)._difference(Interval((0,5),op))
        self.assertFalse(i)

        #points
        i = Interval.from_value(2.1)._difference(Interval.from_value(2.1))
        self.assertTrue(i[0].is_empty())
        self.assertTrue(i[1].is_empty())

        i = Interval.from_value(2.3)._difference(Interval.from_value(2.1))
        self.assertEqual(len(i),1)
        self.assertTrue(i[0].is_discrete())
        self.assertEqual(i[0].bounds,(2.3,2.3))

        #point result
        i = Interval((0,5),cl)._difference(Interval((0,7),op))
        self.assertEqual(len(i),1)

        #some random cases
        i = Interval((0,2.3),ho)._difference(Interval((1.5,6),cl))
        self.assertEqual(len(i),1)
        self.assertEqual(i[0].included,(False,False))
        self.assertEqual(i[0].bounds,(0,1.5))

    def test_union(self):
        op = (False,False)
        cl = (True,True)
        ho = (False,True)

        #completely contained
        i = Interval((0,5),op)._union(Interval((1,3),ho))
        self.assertEqual(len(i),1)
        self.assertEqual(i[0].included,op)
        self.assertEqual(i[0].bounds,(0,5))

        #disjoint
        i = Interval((0,2),op)._union(Interval((3,4),ho))
        self.assertEqual(len(i),2)

        #empty set
        i = Interval((0,0),op)._union(Interval((3,3),ho))
        self.assertEqual(len(i),0)
        i = Interval((0,2),op)._union(Interval((3,3),ho))
        self.assertEqual(len(i),1)
        i = Interval((0,0),op)._union(Interval((3,4),ho))
        self.assertEqual(len(i),1)
        i = Interval((1,1),ho)._union(Interval((1,1),cl))
        self.assertEqual(len(i),1)

        #point result
        i = Interval((1,1),cl)._union(Interval((1,1),cl))
        self.assertEqual(len(i),1)
        self.assertTrue(i[0].is_discrete())

        #some random cases
        i = Interval((0,2.3),ho)._union(Interval((1.5,6),cl))
        self.assertEqual(len(i),1)
        self.assertEqual(i[0].included,ho)
        self.assertEqual(i[0].bounds,(0,6))

class DiscreteSetTest(unittest.TestCase):
    def setUp(self):
        self.a = DiscreteSet([1,2,3])
        self.b = DiscreteSet([1,3,'a'])
        self.c = DiscreteSet.everything()

    def test_membership(self):
        self.assertTrue(1 in self.a)
        self.assertFalse(4 in self.a)

        self.assertTrue(1 in self.c)
        self.assertTrue(4 in self.c)
        self.assertTrue("foobar" in self.c)

    def test_emptiness(self):
        self.assertFalse(self.a.is_empty())
        self.assertFalse(self.b.is_empty())
        self.assertFalse(self.c.is_empty())

    def test_intersection(self):
        d = self.a.intersection(self.b)
        self.assertTrue(1 in d)
        self.assertFalse(2 in d)

        d = self.a.intersection(self.c)
        self.assertTrue(1 in d)
        self.assertTrue(2 in d)
        self.assertFalse(4 in d)

    def test_difference(self):
        d = self.a.difference(self.b)
        self.assertEqual(len(d.elements),1)

    def test_union(self):
        d = self.a.union(self.b)
        self.assertEqual(len(d.elements),4)

class IntervalSetTest(unittest.TestCase):
    def setUp(self):
        op = (False,False)
        cl = (True,True)
        ho = (False,True)

        self.empty = Interval((3,0),(op))
        self.op = Interval((0,2),op)
        self.cl = Interval((1,4),cl)
        self.ho = Interval((3,6),ho)
        self.point = Interval((2.1,2.1),cl)
        self.point2 = Interval((2.3,2.3),cl)
        self.halfspace = Interval((0,float("inf")),cl)

    def test_init(self):
        iset = IntervalSet([self.op, self.ho])

        #Check merging of overlapping intervals
        iset = IntervalSet([self.op,self.cl,self.ho,self.point,self.point2])
        self.assertEqual(len(iset.ints),1)
        self.assertEqual(iset.ints[0].bounds,(0,6))

        #Check pruning of empty sets
        iset = IntervalSet([self.empty])
        self.assertTrue(iset.is_empty())
        self.assertTrue(iset.is_discrete())

        #Points
        iset = IntervalSet([self.point, self.point2])
        self.assertTrue(iset.is_discrete())
        self.assertTrue(2.1 in iset)
        #the same in better notation
        iset = IntervalSet.from_values([2.1,2.3])
        self.assertTrue(iset.is_discrete())
        self.assertTrue(2.1 in iset)

    def test_everything(self):
        iset = IntervalSet.everything()
        self.assertTrue(1 in iset)
        self.assertTrue(float("inf") in iset)

    def test_intersection(self):

        iset = IntervalSet([self.op,self.ho]).intersection(
               IntervalSet([self.cl]))
        self.assertTrue(1.5 in iset)
        self.assertTrue(1 in iset)
        self.assertEqual(len(iset.ints),2)

        iset = IntervalSet.everything().intersection(
               IntervalSet([self.op, self.point]))
        self.assertTrue(1.5 in iset)
        self.assertTrue(2.1 in iset)
        self.assertEqual(len(iset.ints),2)

        iset = IntervalSet([self.empty,self.point,self.ho]).intersection(
               IntervalSet([self.halfspace]))
        self.assertTrue(2.1 in iset)
        self.assertTrue(4 in iset)

    def test_difference(self):
        op = (False,False)
        cl = (True,True)
        ho = (False,True)

        #completely contained
        iset = IntervalSet([Interval((0,5),op)]).difference(IntervalSet([Interval((1,3),ho)]))
        self.assertEqual(len(iset.ints),2)

        #points
        iset = IntervalSet.from_values([1,1.2,2]).difference(IntervalSet.from_values([1.2,2]))
        self.assertTrue(iset.is_discrete())
        self.assertFalse(iset.is_empty())

    def test_union(self):
        op = (False,False)
        cl = (True,True)
        ho = (False,True)

        iset = IntervalSet([Interval((0,5),op)]).union(IntervalSet([Interval((1,3),ho)]))
        self.assertEqual(len(iset.ints),1)

        #points
        iset = IntervalSet.from_values([1,1.2,2]).union(IntervalSet.from_values([1.2,3]))
        self.assertTrue(iset.is_discrete())
        self.assertFalse(iset.is_empty())
        self.assertEqual(len(iset.ints),4)

class TestPatch(unittest.TestCase):
    def setUp(self):
        op = (False,False)
        cl = (True,True)
        ho = (False,True)

        self.ds1 = DiscreteSet(['M1',"M2","M3"])
        self.ds2 = DiscreteSet(['M1',"M2","M4"])
        self.fs1 = DiscreteSet(['foo',"bar","baz"])
        self.is1 = IntervalSet([Interval((0,4),ho),Interval((6,6),cl)])
        self.is2 = IntervalSet([Interval((4,5),op),Interval((6,6),cl)])
        self.is3 = IntervalSet([Interval((3,5),op)])

        self.p1 = Patch({'thread' : self.ds1, 'len' : self.is1})
        self.p2 = Patch({'thread' : self.ds2, 'len' : self.is2})
        self.p3 = Patch({'thread' : self.ds2, 'len' : self.is3})
        self.p4 = Patch({'thread' : self.fs1, 'len' : self.is3})
    def test_init(self):
        p = Patch({'thread' : self.ds1, 'len' : self.is1})
        self.assertFalse(p.discrete)

    def test_intersection(self):

        p = self.p1.intersection(self.p2)
        self.assertTrue(p.is_discrete())
        self.assertFalse(p.is_empty())

        p = self.p1.intersection(self.p3)
        self.assertFalse(p.is_discrete())
        self.assertFalse(p.is_empty())

        p = self.p1.intersection(self.p4)
        self.assertTrue(p.is_empty())

    def test_membership(self):
        self.assertTrue({'thread': 'M1', 'len' : 6} in self.p1)
        self.assertFalse({'thread': 'M1', 'len' : 7} in self.p1)
        self.assertFalse({'thread': 'M4', 'len' : 6} in self.p1)

        self.assertTrue({'thread': 'M1', 'len' : 4.5} in self.p2)
        self.assertFalse({'thread': 'M1', 'len' : 7} in self.p2)
        self.assertFalse({'thread': 'M3', 'len' : 6} in self.p2)

        self.assertFalse({'thread': 'M1', 'len' : 6} in self.p4)
        self.assertFalse({'thread': 'M1', 'len' : 7} in self.p4)
        self.assertFalse({'thread': 'M1', 'len' : 6} in self.p4)
        self.assertFalse({'thread': 'M3', 'len' : 6} in self.p4)

    def test_iteration(self):
        p = self.p1.intersection(self.p2)
        self.assertEqual(len(list(p.iter_points())),2)

        self.assertRaises(ValueError,lambda: list(self.p1.iter_points()))

class TestPatchSet(unittest.TestCase):
    def setUp(self):
        self.m1 = Patch({
            'x1' : DiscreteSet(['A','B','V']),
            'x2' : IntervalSet([Interval((0,4),(True,True)),
                                Interval((6,8),(False,True))])
        })
        self.m2 = Patch({
            'x1' : DiscreteSet(['C']),
            'x2' : IntervalSet([Interval((1,3),(True,True)),
                                Interval((10,21),(False,True))])
        })

        self.d1 = Patch({
            'x1' : DiscreteSet(['A','B','V']),
            'x2' : DiscreteSet(['1','2','3']),
        })
        self.d2 = Patch({
            'x1' : DiscreteSet(['C']),
            'x2' : DiscreteSet(['2','3']),
        })

        self.c1 = Patch({
            'x1' : IntervalSet([Interval((0,5),(True,True))]),
            'x2' : IntervalSet([Interval((0,4),(True,True)),
                                Interval((6,8),(False,True))])
        })

        self.c2 = Patch({
            'x1' : IntervalSet([Interval((9,15),(True,True))]),
            'x2' : IntervalSet([Interval((2,4),(True,True))])
        })

        self.m = PatchSet([self.m1,self.m2])
        self.d = PatchSet([self.d1,self.d2])
        self.c = PatchSet([self.c1,self.c2])

        self.m_sect = PatchSet([Patch({
            'x1' : DiscreteSet(['A','B','C']),
            'x2' : IntervalSet([Interval((2,5),(False,True))])
        })])

        self.d_sect = PatchSet([Patch({
            'x1' : DiscreteSet(['A','B','C']),
            'x2' : DiscreteSet(['1','2','3'])
        })])

        self.c_sect = PatchSet([Patch({
            'x1' : IntervalSet([Interval((2,6),(True,True))]),
            'x2' : IntervalSet([Interval((2,6),(True,True))])
        })])

    def test_init(self):
        empty = PatchSet([])
        self.assertTrue(empty.is_discrete())
        self.assertTrue(empty.is_empty())

        self.assertFalse(self.m.is_discrete())
        self.assertFalse(self.m.is_empty())

        self.assertTrue(self.d.is_discrete())
        self.assertFalse(self.d.is_empty())

        self.assertFalse(self.c.is_discrete())
        self.assertFalse(self.c.is_empty())

    def test_intersection(self):
        m = self.m.intersection(self.m_sect)
        self.assertFalse(m.is_empty())
        self.assertFalse(m.is_discrete())

        d = self.d.intersection(self.d_sect)
        self.assertFalse(d.is_empty())
        self.assertTrue(d.is_discrete())

        c = self.c.intersection(self.c_sect)
        self.assertFalse(c.is_empty())
        self.assertFalse(c.is_discrete())

    def test_membership(self):
        self.assertTrue({'x1' : 'A', 'x2' : 2.4} in self.m_sect)
        self.assertFalse({'x1' : 'A', 'x2' : 4} in self.d_sect)

    def test_iterate(self):
        self.assertEqual(len(list(self.d.iter_points())),11)

        self.assertRaises(ValueError,lambda: list(self.m.iter_points()))

        m_disc = PatchSet([Patch({
            'x1' : DiscreteSet.everything(),
            'x2' : IntervalSet([Interval((2.1,2.1),(True,True))])
        })])

        m = self.m.intersection(m_disc)
        self.assertTrue(m.is_discrete())
        self.assertEqual(len(list(m.iter_points())),4)

        c_disc = PatchSet([Patch({
            'x1' : IntervalSet([Interval((2.1,2.1),(True,True))]),
            'x2' : IntervalSet([Interval((3.1,3.1),(True,True)),
                                Interval((14.1,14.1),(True,True))])
        })])


        c = self.c.intersection(c_disc)
        self.assertTrue(c.is_discrete())
        self.assertFalse(c.is_empty())
        self.assertEqual(len(list(c.iter_points())),1)

