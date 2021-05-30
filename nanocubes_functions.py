from nanocubes_lib import *

#===========================================
# Nanocubes called functions
#   in lexicographic order
#===========================================

def Child(node, value):
    for e in node.children:
        if e.value == value: return e.dst
    return None

def Content(node):
    if node.content is None: return None
    return node.content.dst

def ContentIsProper(node):
    return node.content.ownership == PROPER

def ContentIsShared(node):
    return node.content.ownership == SHARED

def HasSingleChild(node):
    return len(node.children) == 1

def IsSharedChild(node, child):
    for c in node.children:
        if c.dst == child:
            return c.ownership == SHARED

def NewProperChild(node, value, new_node):
    e = Edge(node.d, CHILD, PROPER, new_node, value)
    node.children.append(e)
    new_node.d = node.d
    return new_node

def NewSharedChild(node, value, new_node):
    e = Edge(node.d, CHILD, SHARED, new_node, value)
    node.children.append(e)
    return new_node

def ReplaceChild(node, child, new_child):
    for e in node.children:
        if e.dst == child:
            e.ownership = PROPER
            e.dst = new_child
            return new_child
    return None

def SetSharedContent(node, c_node):
    node.content = Edge(node.d, CONTENT, SHARED, c_node)
    if c_node is not None:  c_node.d = node.d + 1

def SetProperContent(node, c_node):
    node.content = Edge(node.d, CONTENT, PROPER, c_node)
    c_node.d = node.d + 1
