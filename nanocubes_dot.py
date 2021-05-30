import sys
import os
from nanocubes_lib import *

""" *****************************************************************************
                             dot Tests
**************************************************************************** """
Colors = None
ranks = [ ]

def dotVertix(id, label, level):
    color = Colors[level]
    lines = 'penwidth=1.000000 style="filled" fontsize=8 '
    shape = 'shape="ellipse" margin=0 width=0.25 height=0.25'
    colors = 'color="%s", fillcolor="%s" fontcolor="#303030"'%(color, color)
    return 'v_%s [label="%s" %s %s %s];' %(id, label, lines, shape, colors)

def dotVirtualVertix(id, id_child, level):
    color = Colors[level]
    lines = 'penwidth=1.000000 style="filled" fontsize=8 '
    shape = 'shape="ellipse" margin=0 width=0.25 height=0.25'
    colors = 'color="%s", fillcolor="none" fontcolor="#303030"'%(color)
    return 'v_%s [label="%s" %s %s %s];' %(id, id_child, lines, shape, colors)

def dotEdge(id1, id2, label, type):
    if type == "PCHILD":
        head = "none"
        color = "black"
        line="filled"
        weight="weight=100"
    elif type == "SCHILD":
        head = "none" # normal
        color = "red"
        line="dashed" # filled
        weight="weight=1"
    elif type == "PCONTENT":
        head = "normal"
        color = "#4080ff"
        line="filled" #dashed
        weight="weight=50"
    elif type == "SCONTENT":
        head = "normal"
        color = "#c0c0c0"
        line="dashed"
        weight="weight=1"

    lines = 'fontsize=8 style=%s %s'%(line, weight)
    shape = 'arrowhead="%s"' % head
    colors = 'color="%s"'%color
    return 'v_%s -> v_%s [label=" %s " %s %s %s];' %(id1, id2, label, lines, shape, colors)



def dotNode(node, level):
    global next_level
    if node == None: return
    id = node.id
    if node.terminal:
        label = str(id) + ":" + str(node.count)
    else:
        label = id
    print("  ",dotVertix(id, label, level))

    ranks[level].append(node)

    for edge in node.children:
        child = edge.dst
        v = edge.value
        if edge.ownership == PROPER:
            print("  ",dotEdge(id, child.id, v, "PCHILD"))
            dotNode(child, level+1)
        else:
            id2 = "" + str(id) + "_" + str(child.id)
            print("  ", dotVirtualVertix(id2, child.id, level+1))
            print("  ", dotEdge(id, id2, v, "SCHILD"))

    content = node.content
    if content != None:
        cnode = content.dst
        if cnode!=None:
            if content.ownership == PROPER:
                print("  ",dotEdge(id, cnode.id, "*", "PCONTENT"))
                dotNode(cnode, next_level[level])
            else:
                print("  ",dotEdge(id, cnode.id, "*", "SCONTENT"))


def dotRankSame(queue):
    for i in range(len(queue)):
        q = queue[i]
        if q is None: return
        print("  ","{ rank = same;", end='')
        sep = ''
        for j in range(len(q)):
            node = q[j]
            print("%s v_%s" % (sep, node.id ), end='' )
            sep = ","
        print("}")

""" *****************************************************************************
                       Tests Functions
**************************************************************************** """

queue = None

dimColors = [ "#f0f0c0" , "#c0c0f0", "#f0c0c0", "#c0f0f0", "#c0f0c0", "#f0c0f0" ]
terminalColor = "#e0e0e0"

def prepare_colors(schema):
    global Colors
    Colors = []
    L = schema["length"]
    for d in range(schema["dim"]):
        for i in range(L[d]):
            Colors.append(dimColors[d % 6])
        Colors.append(dimColors[d % 6])
    Colors.append(terminalColor)


def createDot(S, node, filename=None, title=None):
    global ranks
    global next_level

    prepare_colors(S)
    ranks = [ None ] * (S["height"]+ S["dim"])
    for i in range(len(ranks)):
        ranks[i] = []

    next_level = S["indexOfContent"]
    print("Next_level", next_level)

    if title is None: title = "dot test"
    if filename is None:
        print("-----------------------[ DOT FILE BEGIN ]--------------------------------------")
    else:
        print("Filename:", filename)
        orig_stdout = sys.stdout
        f = open(filename, 'w')
        sys.stdout = f
    print('digraph { rankdir=TB; fontsize="6"; labelloc="t1"; label="%s";' % title)
    dotNode(node, 0)
    dotRankSame(ranks)
    print('}')
    if filename is not  None:
        sys.stdout = orig_stdout
        f.close()
        #os.system("dot -Tpng %s -o %s.png -Gsize=1024,768 -Gdpi=144"%(filename, filename))
        os.system("dot -Tpdf %s -o %s.pdf -Gsize=1024,2048 -Gdpi=144"%(filename, filename))
        os.system("%s.pdf"%(filename))

    else:
        print("----------------------------[ DOT FILE END ]---------------------------------------")
        print("Usage:")
        print("1) copy the subcube above to a file called 'file.dot'")
        print("2) run: dot -Tpng file.dot -o file.png -Gsize=1024,768 -Gdpi=144 ")
        print("3) open the file 'file.png'")


