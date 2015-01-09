"""
This module contains functions for solving and reducing CSPs
"""
from itertools import product
from constrainingorder import Space
from constrainingorder.constraints import FixedValue
from constrainingorder.sets import DiscreteSet, IntervalSet

def ac3(space):
    """
    AC-3 algorithm. This reduces the domains of the variables by
    propagating constraints to ensure arc consistency.
    """
    #determine arcs
    arcs = {}
    for name in space.variables:
        arcs[name] = set([])
    for const in space.constraints:
        for vname1,vname2 in product(const.vnames,const.vnames):
            if vname1 != vname2:
                #this is pessimistic, we assume that each constraint
                #pairwisely couples all variables it affects
                arcs[vname1].add(vname2)

    #enforce node consistency
    for vname in space.variables:
        for const in space.constraints:
            _unary(space,const,vname)

    #assemble work list
    worklist = set([])
    for v1 in space.variables:
        for v2 in space.variables:
            for const in space.constraints:
                if _binary(space,const,v1,v2):
                    for name in arcs[v1]:
                        worklist.add((v1,name))

    #work through work list
    while worklist:
        v1,v2 = worklist.pop()
        for const in space.constraints:
            if _binary(space,const,v1,v2):
                for vname in arcs[v1]:
                    worklist.add((v1,vname))

def _unary(space,const,name):
    """
    Reduce the domain of variable name to be node-consistent with this
    constraint, i.e. remove those values for the variable that are not
    consistent with the constraint.

    returns True if the domain of name was modified
    """
    if not name in const.vnames:
        return False
    if space.variables[name].discrete:
        values = const.domains[name]
    else:
        values = const.domains[name]

    space.domains[name] = space.domains[name].intersection(values)
    return True

def _binary(space,const,name1,name2):
    """
    reduce the domain of variable name1 to be two-consistent (arc-consistent)
    with this constraint, i.e. remove those values for the variable name1,
    for which no values for name2 exist such that this pair is consistent
    with the constraint

    returns True if the domain of name1 was modified
    """
    if not (name1 in const.vnames and name2 in const.vnames):
        return False
    remove = set([])
    for v1 in space.domains[name1].iter_members():
        for v2 in space.domains[name2].iter_members():
            if const.consistent({name1 : v1, name2 : v2}):
                break
        else:
            remove.add(v1)

    if len(remove) > 0:
        if space.variables[name1].discrete:
            remove = DiscreteSet(remove)
        else:
            remove = IntervalSet.from_values(remove)

        space.domains[name1] = space.domains[name1].difference(remove)
        return True
    else:
        return False

def solve(space,method='backtrack',ordering=None):
    """
    generator for all solutions.

    Method can take the following values:
    backtrack: simple chronological backtracking
    ac-lookahead: full lookahead
    ffp: full lookahead with fail first variable ordering

    ordering is a list of all variable names in the order in which they will be considered
    """
    if ordering is None:
        ordering = space.variables.keys()

    if not space.is_discrete():
        raise ValueError("Can not backtrack on non-discrete space")
    if method=='backtrack':
        for label in _backtrack(space,{},ordering):
            yield label
    elif method=='ac-lookahead':
        for label in _lookahead(space,{},ordering):
            yield label
    else:
        raise ValueError("Unknown solution method: %s" % method)


def _backtrack(space,label,ordering):
    level = len(label)
    if level == len(space.variables):
        if space.satisfied(label):
            yield label
    elif space.consistent(label):
        vname = ordering[level]
        newlabel = label.copy()
        for val in space.domains[vname].iter_members():
            newlabel[vname] = val
            for sol in _backtrack(space,newlabel,ordering):
                yield sol

def _lookahead(space,label,ordering):
    level = len(label)
    if len(label) == len(space.variables):
        if space.satisfied(label):
            yield label
    elif space.consistent(label):
        vname = ordering[level]
        var = space.variables[vname]
        newlabel = label.copy()
        for val in space.domains[vname].iter_members():
            nspace = Space(space.variables.values(),
                           space.constraints + [FixedValue(var,val)])
            newlabel[vname] = val
            ac3(nspace)
            for sol in _lookahead(nspace,newlabel,ordering):
                yield sol
