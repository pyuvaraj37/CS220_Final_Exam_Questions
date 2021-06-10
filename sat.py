from z3 import *
from graphreader import Data, Write

file = input("Input the 3-digits for a file in /exact/exactXXX.gr: ")
V, E, numVert, numEdges = Data('/Users/prith/Desktop/CS220/Final/exact/exact{}.gr'.format(file))

numVert = len(V)
# T = []

# solution = True
# k = 1


# 1 perm
# 1 forb

# C = []
# U = []

# for i in V:
#     T.append([])
#     for j in V:
#         common_neighbor = 0
#         uncommon_neighbor = 0
#         if i < j:
#             for z in V:
#                 if j < z:
#                     if (i, z) in E and (j, z) in E:
#                         common_neighbor+=1

#                     if z != i and z != j:
#                         if (i, z) in E or (j, z) in E:
#                             uncommon_neighbor+=1

#             C[i][j] = common_neighbor
#             U[i][j] = uncommon_neighbor    
            
s = Solver()

adjMatrix = []

xij = []

# for i in range(numVert):
#     adjMatrix.append([])
#     for j in range(numVert):
#         if i < j and (i+1 , j+1) in E:
#             adjMatrix[i].append(1)
#         else:
#             adjMatrix[i].append(0)


for i in range(numVert):
    xij.append([])
    for j in range(numVert):
        xij[i].append(Bool("x_%s_%s" % (i+1, j+1)))

#print(xij)

# for i in range(numVert):
#     for j in range(i+1, numVert):
#         for k in range(j+1, numVert):
#             if i < j and j < k:
#                 s.add(Or(Not(xij[i][j]), Not(xij[j][k]), xij[i][k]))

p3_c = [ Or( Not(xij[i][j], Not(xij[j][k], xij[i][k]))) for i in range(numVert) for j in range(i+1, numVert) for k in range(j+1, numVert) if i < j and j < k]
e_c  = [ If((i, j) in E, True, xij[i][j] == False) for i in range(numVert) for j in range(i+1, numVert) if i < j]
# for i in range(numVert):
#     for j in range(i+1, numVert):  
#         if i < j:
#             if (i+1, j+1) in E:
#                 s.add(xij[i][j])
#             else:
#                 s.add(Not(xij[i][j]))

s.add(p3_c + e_c)


if s.check() == sat:
    m = s.model()

    r = [ [ m.evaluate(xij[i][j]) for j in range(9) ] for i in range(9)]
    print(r)

else:
    print('unsat')