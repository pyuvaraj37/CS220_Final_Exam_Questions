from z3 import *
from graphreader import Data, WriteSat

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
#print(E)
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

# p3_c = [ Or( Not(xij[i][j], Not(xij[j][k], xij[i][k]))) for i in range(numVert) for j in range(i+1, numVert) for k in range(j+1, numVert) if i < j and j < k]

p3_c1 = [ Implies(And(xij[i][j], xij[j][k]),xij[i][k]) for i in range(numVert) for j in range(i+1, numVert) for k in range(j+1, numVert) if i < j and j < k]
p3_c2 = [ Implies(And(xij[i][k], xij[j][k]),xij[i][j]) for i in range(numVert) for j in range(i+1, numVert) for k in range(j+1, numVert) if i < j and j < k]
p3_c3 = [ Implies(And(xij[i][j], xij[i][k]),xij[j][k]) for i in range(numVert) for j in range(i+1, numVert) for k in range(j+1, numVert) if i < j and j < k]

# e_c  = [ If((i+1, j+1) in E, xij[i][j], Not(xij[i][j])) for i in range(numVert) for j in range(i, numVert) if i < j]


e_c = []
for i in range(numVert):
    for j in range(numVert):  
        if i < j:
            if (i+1, j+1) in E:
                # s.add(xij[i][j])
                e_c.append(xij[i][j])
            # else:
            #     # s.add(Not(xij[i][j]))
            #     e_c.append(Not(xij[i][j]))

s.add(p3_c1 + p3_c2 + p3_c3 + e_c)


if s.check() == sat:
    m = s.model()

    r = [ [ m.evaluate(xij[i][j]) for j in range(numVert)] for i in range(numVert)]
    
    mod = []
    for i in range(numVert):
        for j in range(numVert):  
            if i < j:
                if (i+1, j+1) in E and not r[i][j]:
                    mod.append((i+1,j+1))
                elif (i+1, j+1) not in E and r[i][j]:
                    mod.append((i+1,j+1))

    #print(mod)

    WriteSat('/Users/prith/Desktop/CS220/Final/benchmark_sat/exact{}.gr'.format(file),mod)
    #print(r)

else:
    print('unsat')