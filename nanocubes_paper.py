from nanocubes_functions import *

#==============================================
# Nanocubes functions as listed in paper
#==============================================

def Nanocube(objects, S, ltime):
    nano_cube = Node()
    for o in objects:
        update_nodes = Set()
        ADD(nano_cube, o, 1, S, ltime, update_nodes)
    return nano_cube


def TrailProperPath(root, values):
    stack = Stack()
    Push(stack, root)
    node = root
    k = len(values)
    for i in range(k):
        vi = values[i]
        child = Child(node, vi)
        if child is null:
            child = NewProperChild(node, vi, Node())
        elif IsSharedChild(node, child):
            child = ReplaceChild(node, child, ShallowCopy(child))
        Push(stack, child)
        node = child
    return stack


def ADD(root, o, d, S, ltime, updated_nodes):
    ls = Chains(S, d)
    stack = TrailProperPath(root, Values(ls, o))
    child = null

    while not IsEmpty(stack):
        node = Pop(stack)
        update = False

        if HasSingleChild(node):
            SetSharedContent(node, Content(child))

        elif Content(node) is null:
            if d == Dim(S):
                p_node = CreateTimeSeries()
            else:
                p_node = Node()
            SetProperContent(node, p_node)
            update = True

        elif ContentIsShared(node) \
                and not BelongsToSet(Content(node), updated_nodes):
            SetProperContent(node, ShallowCopy(Content(node)))
            update = True

        elif ContentIsProper(node):
            update = True

        if update:
            if d == Dim(S):
                InsertIntoTimeSeries(Content(node),ltime(o))
            else:
                ADD(Content(node), o, d+1, S, ltime, updated_nodes)
            InsertIntoSet(Content(node), updated_nodes)

        child = node
    return 0

def ShallowCopy(node):
    if node.terminal:
        node_sc = ShallowCopyTimeSeries(node)
    else:
        node_sc = Node()

    SetSharedContent(node_sc, Content(node))
    for c in node.children:
        NewSharedChild(node_sc, c.value, Child(node, c.value))
    return node_sc
