

def Data(path_to_data):
    V = []
    E = []
    numEdges = 0
    numVert = 0
    file = open(path_to_data, 'r')
    for line in file:
        line = repr(line)
        line = line.strip('\'\\n')
        line = line.split()
        #print(line)
        if len(line) > 2:
            numVert = int(line[2])
            numEdges = int(line[3])
        else:
            E.append((int(line[0]), int(line[1])))

    V = [*range(1, numVert + 1)]

    return V, E, numVert, numEdges


def Write(path_to_write, numVert, edges, x):
    file = open(path_to_write, 'w')
    for i in range(numVert):
        for j in range(numVert):
            if i < j and x[i][j] != 1 and (i + 1, j + 1) not in edges:
                file.writelines("{} {}\n".format(i + 1, j + 1))
            elif i < j and x[i][j] == 1 and (i + 1, j + 1) in edges:
                file.writelines("{} {}\n".format(i + 1, j + 1))
    file.close()