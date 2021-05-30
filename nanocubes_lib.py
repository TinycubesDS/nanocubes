#===========================================
# Basic Definitions
#===========================================
PROPER = "Proper"
SHARED = "Shared"

CONTENT = "Content"
CHILD = "Child"

null = None

#===========================================
# Basic Class: Edge
#===========================================
class Edge:
    seq = 0
    def __init__(self, d, type, ownership, dst, value = None):
        Edge.seq += 1
        self.seq = Edge.seq
        self.index = 0
        self.type = type
        self.ownership = ownership
        self.src = None
        self.dst = dst
        self.value = value
        self.d = d
        self.id = str(self.seq)

#===========================================
# Basic Class: Node
#===========================================
class Node:
    seq = 0
    def __init__(self):
        Node.seq += 1
        self.seq = Node.seq
        self.index = 0
        self.children = []
        self.count = 0
        self.content = None
        self.terminal = False
        self.d = 1
        self.id = str(self.seq)

#===========================================
#  Dimensions, Chains, Values
#===========================================
def CreateS(lengths):
    height = 1
    for v in lengths:
        height += v + 1

    indexOfContent = [0] * (height + 1)
    dim = len(lengths)
    L= lengths
    index = 0
    acc = 0
    for d in range(dim):
        acc = acc + L[d] + 1
        for l in range(L[d] + 1):
            indexOfContent[index] = acc
            index += 1

    return dict(length=lengths, dim=dim, height = height, indexOfContent = indexOfContent)

def Dim(S):
    return S["dim"]

def Chains(S, d):
    def identity(x): return x
    return dict(S=S, d=d, ls=[ identity ] * S["length"][d-1])

def Values(chains, o):
    values = []

    d = chains["d"]
    S = chains["S"]
    ls = chains["ls"]

    offs = 0
    for x in range(d-1):
        offs += S["length"][x]

    for i in range(len(ls)):
        values.append(o[offs+ i])
    return values

#===========================================
# Set
#===========================================
def Set():
    return []

def BelongsToSet(x, set):
    return x in set

def InsertIntoSet(x, set):
    if BelongsToSet(x, set): return
    set.append(x)

#===========================================
# Stack
#===========================================
def IsEmpty(stack):
    return len(stack) == 0

def Pop(stack):
    return stack.pop()

def Push(stack, node):
    return stack.append(node)

def Stack():
    return []

#===========================================
# Time series emulator
#===========================================
def CreateTimeSeries():
    ts = Node()
    ts.terminal = True
    return ts

def ShallowCopyTimeSeries(ts):
    print("ShallowCopyTimeSeries: ", ts.id)
    new = Node()
    new.terminal = True
    new.count = ts.count
    return new


def InsertIntoTimeSeries(ts, info):
    ts.count += 1

