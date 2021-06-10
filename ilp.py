import gurobipy as gp
from gurobipy import *
import numpy as np
import scipy.sparse as sp
from graphreader import Data, Write

file = input("Input the 3-digits for a file in /exact/exactXXX.gr: ")

V, E, numVert, numEdges = Data('/Users/prith/Desktop/CS220/Final/exact/exact{}.gr'.format(file))

try:
    print("Creating a new model")
    m = gp.Model("Cluster Editing")

    print("Creating variables")
    x = m.addMVar(shape=(numVert, numVert), vtype=GRB.BINARY, name="x")
    
    print("Setting objective")
    term_one = sum(x[i][j] for i in range(numVert) for j in range(numVert) if i < j and (i + 1, j + 1) in E)
    term_two = sum(1 - x[i][j] for i in range(numVert) for j in range(numVert) if i < j and (i + 1, j + 1) not in E)
    obj = term_one + term_two
    m.setObjective(obj, GRB.MINIMIZE)

    print("Building contraints...")
    for i in range(numVert):
        for j in range(i+1, numVert):
            for k in range(j+1,numVert):
                if i < j and j < k:
                    m.addConstr(x[i][k] <= x[i][j] + x[j][k])
                    m.addConstr(x[i][j] <= x[i][k] + x[j][k])
                    m.addConstr(x[j][k] <= x[i][j] + x[i][k])

    print("Optimizing model")
    m.optimize()

    #print(x.X)
    print('Obj: %g' % m.objVal)
    Write('/Users/prith/Desktop/CS220/Final/benchmark_ilp/exact{}.gr'.format(file), numVert, E, x.X)

except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ": " + str(e))

except AttributeError:
    print('Encountered an attribute error')


