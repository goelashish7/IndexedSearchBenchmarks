#!/usr/bin/env python

# sys.argv[1] is the input file name
# the first line of input file is the text on which we build suffix tree
# the rest lines are patterns

# global variable S stores the text

import sys

DEBUG = False

class Node:
        # node of suffix tree

        # we assign serial number to each node for debuging purpose
        SERIAL = 0

        # ingoing edge of this node is S[start:end], i.e., substring
        # of S that consists of S[start], S[start+1], ..., S[end-1]
        def __init__(self, start, end, depth, parent):

                assert start < end or (start == 0 and end == 0), \
                                (Node.SERIAL, start, end)
                assert depth >= end - start, \
                                (Node.SERIAL, start, end, depth)

                self.start = start
                self.end = end
                self.depth = depth
                self.parent = parent
                self.children = []
                self.suffix_link = None

                self.serial = Node.SERIAL
                Node.SERIAL = Node.SERIAL + 1

        def is_root(self):
                return self.depth == 0

        def edge_len(self):
                return self.end - self.start

        def path_len(self):
                return self.depth

        def edge_label(self):
                return S[self.start:self.end]

        def path_label(self):
                if self.depth == 0:
                        return ''
                else:
                        return self.parent.path_label() + S[self.start:self.end]

        def match_children(self, i, S):
                for child in self.children:
                        if S[child.start] == S[i]:
                                return child
                return None

        def branch_parent(self, edge_offset):

                assert edge_offset <= self.edge_len(), \
                                (self.serial, edge_offset)

                if edge_offset == self.edge_len():
                        return self

                p = self.parent
                # in case p == root, use self.start instead
                v = Node(self.start, self.start + edge_offset, \
                                p.depth + edge_offset, p)
                v.children.append(self)

                p.children.remove(self)
                p.children.append(v)

                self.parent = v
                self.start = self.start + edge_offset

                return v

        def dump(self):
                print '%3d' % self.serial,
                if self.edge_len() < 20:
                        s = repr(S[self.start:self.end])
                else:
                        s = '%4d %4d' % (self.start, self.end)
                print s.ljust(25),
                if self.suffix_link:
                        print self.suffix_link.serial,
                else:
                        print 'X',
                print map(lambda n: n.serial, self.children)

###

# T_-1 is the tree with only root node
# T_0 is the tree with S[0:] inserted
def make_T0(S):
        root    = Node(0, 0, 0, None)
        node_0  = Node(0, len(S), len(S), root)
        root.children.append(node_0)
        return root

def BFS(root, method):
        queue = [ root ]
        while len(queue) > 0:
                v = queue.pop(0)
                queue.extend(v.children)
                method(v)

def DFS(root, method):
        stack = [ root ]
        while len(stack) > 0:
                v = stack.pop()
                stack.extend(v.children)
                method(v)

# assert constraints/properties of each node
def assertion(v):
        # each edge represent any non-empty substring of S
        assert v.edge_len() > 0 or v == root, v.serial
        assert v.path_len() > 0 or v == root, v.serial
        if v.children == []:
                # leaf nodes have no suffix link
                assert v.suffix_link == None, v.serial
        else:
                # each internal node has a suffix link, possibly except
                # the node we've just visited in last iteration
                assert v.suffix_link != None or v == lo_head_0, v.serial
                # each internal node has at least two children, except root
                assert len(v.children) >= 2 or v == root, v.serial
                # sibling edges represent substrings with no common prefix
                for r, rest in map(lambda i: (v.children[i], v.children[i+1:]),
                                xrange(0, len(v.children) - 1)):
                        for s in rest:
                                for i in xrange(0, min(r.edge_len(), s.edge_len())):
                                        if S[r.start+i] != S[s.start+i]:
                                                break
                                else:
                                        assert False, (r.serial, s.serial)

#P = ""
#S = ""
#root = ""
###
#def buildTree(s = ""):
def buildTree(s = ""):
    #global P, S, root
    # f = open('test', 'r')

    # # to satisfy the premise of MCC's algorithm, keep the
    # # trailing '\n' character which is unique in S
    # S = f.readline()

    # # whereas trailing '\n' character of each pattern is removed
    # P = map(lambda s: s[:-1], f.readlines())

    # f.close()
    S = s + '\r'
    #print S
    ### build suffix tree ###

    # S[i:] = head_i + tail_i
    root = make_T0(S)
    lo_head_0 = root        # locus(head_i-1) in T_i-1
    cl_head_0 = root        # contracted_locus(head_i-1) in T_i-2

    for i in xrange(1, len(S)):

            if DEBUG:
                    BFS(root, Node.dump)
                    print 'iter', i, repr(lo_head_0.path_label()), \
                                    cl_head_0.serial, lo_head_0.serial

                    # computes head_i directly (for debug)
                    head_1 = ''
                    for k in xrange(i, len(S) + 1):
                            s = S[i:k]
                            j = S.find(s)
                            if j != -1 and j < i and len(s) > len(head_1):
                                    head_1 = s
                    # tail_i != ''
                    assert len(head_1) < len(S) - i, (i, head_1)

                    BFS(root, assertion)

            ###

            next_cl_head_0 = root

            ### step A: Jumpping (to locus of string u)

            if cl_head_0 == root:
                    # u = empty string
                    lo_u = root
            else:
                    lo_u = cl_head_0.suffix_link

            if DEBUG:
                    assert lo_u.path_label() == cl_head_0.path_label()[1:], \
                            (lo_u.serial, cl_head_0.serial)

            ### step B: Rescanning (for locus of string uw)

            # |u| = 0 only if cl_head_0 == root
            # |x| = 0 only if |head_0| = 0, |x| = 1 otherwise
            # |xu| = cl_head_0.path_len() for cl_head_0 != root

            if cl_head_0 == root: # u is empty
                    if lo_head_0.path_len() == 0: # xuw is empty
                            w_len = 0
                    else: # u is empty, but x is not
                            w_len = lo_head_0.path_len() - 1
            else: # xu is not empty and cl_head_0 is locus of xu
                    w_len = lo_head_0.path_len() - cl_head_0.path_len()

            if DEBUG:
                    assert w_len >= 0, (cl_head_0.serial, lo_head_0.serial, w_len)

            lo_uw = lo_u
            if w_len > 0:
                    while True:
                            w_off = (i-1) + lo_head_0.path_len() - w_len
                            lo_uw_next = lo_uw.match_children(w_off, S)

                            if DEBUG:
                                    # we are sure that locus of string uw exists
                                    assert lo_uw_next != None, \
                                                    (lo_u.serial, w_off, w_len)

                            if w_len > lo_uw_next.edge_len():
                                    lo_uw = lo_uw_next
                                    w_len = w_len - lo_uw_next.edge_len()
                            else:
                                    lo_uw = lo_uw_next.branch_parent(w_len)
                                    if lo_uw != lo_uw_next:
                                            # lo_uw is newly created
                                            # so, lo_uw is not in T_i-1
                                            next_cl_head_0 = lo_uw.parent
                                    break

            lo_head_0.suffix_link = lo_uw

            if DEBUG:
                    assert lo_uw.path_label() == lo_head_0.path_label()[1:], \
                                    (lo_uw.serial, lo_head_0.serial, \
                                    repr(lo_uw.path_label()), \
                                    repr(lo_head_0.path_label()[1:]))

            # step C: Scanning (for locus of string uwv = head_i)

            lo_uwv  = lo_uw
            v_base  = i + lo_uw.path_len()
            v_len   = 0
            while True:
                    lo_uwv_next = lo_uwv.match_children(v_base + v_len, S)
                    if lo_uwv_next == None: # we fall out
                            lo_head_1 = lo_uwv
                            break

                    for off in xrange(0, lo_uwv_next.edge_len()):
                            if S[lo_uwv_next.start + off] == S[v_base + v_len]:
                                    v_len = v_len + 1
                            else:
                                    break
                    else:
                            off = -1
                    if off == -1:
                            lo_uwv = lo_uwv_next
                    else:
                            lo_head_1 = lo_uwv = lo_uwv_next.branch_parent(off)
                            if lo_head_1 != lo_uwv_next:
                                    # lo_head_1 is newly created
                                    # so, lo_head_1 is not in T_i-1
                                    # btw, lo_head_1 == lo_uwv
                                    next_cl_head_0 = lo_head_1.parent
                            break

            if DEBUG:
                    assert lo_uw.path_len() + v_len == len(head_1)
                    assert lo_head_1.path_label() == head_1, \
                                    (lo_head_1.serial, head_1)

            # step D: Inserting (tail_i)
            t = Node(i + lo_head_1.path_len(), len(S), len(S) - i, lo_head_1)
            lo_head_1.children.append(t)

            # step E
            cl_head_0 = next_cl_head_0
            lo_head_0 = lo_head_1

    if DEBUG:
            BFS(root, Node.dump)
    return [root, S]


        
### search in suffix tree

def find_deepest(r):
        deepest = r
        for child in r.children:
                s = find_deepest(child)
                if s.path_len() > deepest.path_len():
                        deepest = s
        return deepest
        
def find_all(r, loc, S):
        deepest = r
        for child in r.children:
                s = find_all(child, loc, S)
                loc.add(len(S) - s.path_len())
                if s.path_len() > deepest.path_len():
                        deepest = s
        return deepest

def searchTree(struct, p):
    # for p in P:
            loc = set()
            v = struct[0]
            S = struct[1]
            #v = root
            i = 0
            while i < len(p) and v != None:
                    for w in v.children:
                            if S[w.start] == p[i]:
                                    k = min(w.edge_len(), len(p) - i)
                                    if S[w.start:w.start+k] == p[i:i+k]:
                                            i = i + w.edge_len()
                                            v = w
                                    else:
                                            v = None
                                    break
                    else:
                            v = None

            if v == None:
                    return []
            else:
                    loc.add(len(S) - find_all(v, loc, S).path_len())
                    return list(loc)

# buildTree()                    
# searchTree()