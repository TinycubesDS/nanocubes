from nanocubes_paper import *
from nanocubes_dot import *

#===========================================
#
#===========================================

def Dump(node, spaces = ''):
    if node == None: return

    if spaces == '':
        print("-----------------------------")

    print("%sN%d " % (spaces, node.seq), end="")

    content = node.content
    if (node.content.dst is None):
        # if content.dst.count > 0: print(" Content %d " % (content.dst.count))
        return
    else:
        print()

    n = len(node.children)
    for edge in node.children:
        print("%sE%d %s %s Value:%d Node: N%d" % (
        spaces, edge.seq, edge.ownership, edge.type, edge.value, edge.dst.seq))
        if edge.ownership == PROPER:
            Dump(edge.dst, spaces + '   ')
        else:
            print("%s ++N%d " % (spaces, edge.dst.seq))

    if content == None:
        print("%s%s" % (spaces, "No Content"))
    else:
        if content.dst == None: return
        # seq = content.dst.seq
        if content.dst.count > 0 and n == 0:
            print("%sN%d Content %d " % (spaces, content.dst.seq, content.dst.count))
        else:
            print("%sE%d %s %s Node:N%d " % (spaces, content.seq, content.ownership, content.type, content.dst.seq))
            if content.ownership == PROPER: Dump(content.dst, spaces + '   ')

#===========================================
#
#===========================================

objects = []
ltime = lambda x: 1

test = 2
if test == 1:
    S = CreateS([1, 2])

    o = [ 1, 2, 3 ]
    objects.append(o)
    o = [ 6, 7, 8 ]
    objects.append(o)
    o = [ 1, 2, 3 ]
    objects.append(o)
else:
    S = CreateS([1, 2, 2])

    o = [ 1, 2, 3, 1, 2 ]
    objects.append(o)

    o = [ 6, 7, 8, 3, 4 ]
    objects.append(o)

    o = [ 1, 2, 3, 1, 2 ]
    objects.append(o)

    o = [6, 7, 9, 4, 5]
    objects.append(o)

nano_cube = Nanocube(objects, S, ltime)
Dump(nano_cube)

createDot(S, nano_cube, "nc_01.dot", "Dimensões: [1,2,2] - Inserção: [1,2,3,1,2] + [6,7,8,3,4] + [1,2,3,1,2] + [6,7,9,3,5]")
