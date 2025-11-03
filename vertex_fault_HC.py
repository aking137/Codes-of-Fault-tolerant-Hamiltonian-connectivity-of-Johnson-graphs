import copy
import itertools
from edge_fault_HC import isHamiltonianConnected, generate_k_combinations

# Give the adjacency matrix of J(4,2), J(5,2), J(6,2) and J(6,3).
J_4_2 = [
    [0, 0, 1, 1, 1, 1,],  # 0: {0,1}
    [0, 0, 1, 1, 1, 1,],  # 1: {2,3}
    [1, 1, 0, 0, 1, 1,],  # 2: {0,2}
    [1, 1, 0, 0, 1, 1,],  # 3: {1,3}
    [1, 1, 1, 1, 0, 0,],  # 4: {0,3}
    [1, 1, 1, 1, 0, 0,]]  # 5: {1,2}

J_5_2 = [
    [0, 1, 1, 1, 1, 1, 1, 0, 0, 0],  # 0: {0,1}
    [1, 0, 1, 1, 1, 0, 0, 1, 1, 0],  # 1: {0,2}
    [1, 1, 0, 1, 0, 1, 0, 1, 0, 1],  # 2: {0,3}
    [1, 1, 1, 0, 0, 0, 1, 0, 1, 1],  # 3: {0,4}
    [1, 1, 0, 0, 0, 1, 1, 1, 1, 0],  # 4: {1,2}
    [1, 0, 1, 0, 1, 0, 1, 1, 0, 1],  # 5: {1,3}
    [1, 0, 0, 1, 1, 1, 0, 0, 1, 1],  # 6: {1,4}
    [0, 1, 1, 0, 1, 1, 0, 0, 1, 1],  # 7: {2,3}
    [0, 1, 0, 1, 1, 0, 1, 1, 0, 1],  # 8: {2,4}
    [0, 0, 1, 1, 0, 1, 1, 1, 1, 0]]  # 9: {3,4}

J_6_2 = [
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],  # {1,2}
    [1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0],  # {1,3}
    [1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0],  # {1,4}
    [1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1],  # {1,5}
    [1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1],  # {1,6}
    [1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0],  # {2,3}
    [1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0],  # {2,4}
    [1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],  # {2,5}
    [1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1],  # {2,6}
    [0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0],  # {3,4}
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],  # {3,5}
    [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1],  # {3,6}
    [0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1],  # {4,5}
    [0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1],  # {4,6}
    [0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0]]  # {5,6}

J_6_3 = [
    [0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],  # {1,2,3}
    [1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0],  # {1,2,4}
    [1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0],  # {1,2,5}
    [1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0],  # {1,2,6}
    [1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0],  # {1,3,4}
    [1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0],  # {1,3,5}
    [1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],  # {1,3,6}
    [0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0],  # {1,4,5}
    [0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0],  # {1,4,6}
    [0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],  # {1,5,6}
    [1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0],  # {2,3,4}
    [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0],  # {2,3,5}
    [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],  # {2,3,6}
    [0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0],  # {2,4,5}
    [0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1],  # {2,4,6}
    [0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1],  # {2,5,6}
    [0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1],  # {3,4,5}
    [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1],  # {3,4,6}
    [0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1],  # {3,5,6}
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0]]  # {4,5,6}

graphs = [J_4_2, J_5_2, J_6_2] # The computation time for J(6,3) is very long, so choose carefully

for order, matrix in enumerate(graphs):
    name = 'J(4,2)' if order == 0 else 'J(5,2)' if order == 1 else 'J(6,2)' if order == 2 else 'J(6,3)'
    n = len(matrix)
    d = sum(1 for j in range(n) if matrix[0][j] == 1)
    t = 0
    # get the family of all fault-vertex-sets
    allSetOfFaultyVertices = generate_k_combinations(range(n), d - 3)
    batchSize = len(allSetOfFaultyVertices)

    HamiltonianConnectedness = True

    # check the Hamiltonian connectedness for each fault-vertex-set
    for setOfFaultyVertices in allSetOfFaultyVertices:
        faultymatrix = [[element for j, element in enumerate(row) if j not in setOfFaultyVertices] 
                        for i, row in enumerate(matrix) if i not in setOfFaultyVertices
                        ]
        
        t += 1
        completed = (t * 100) // batchSize 
        print(f"\r{name} progress: {completed}%", end='', flush=True)
        
        # check the Hamiltonian connectedness for each pair of vertices
        for i in range(n-d+2):
            for j in range(i+1,n-d+3):
                if isHamiltonianConnected(i,j,faultymatrix) == -1:
                    HamiltonianConnectedness = False
                    print(setOfFaultyVertices, i, j)
    
    print(f"\n{name} completed")
    if HamiltonianConnectedness:
        print(name, 'is d-3 vertex-fault-tolerant Hamiltonian connected')
    else:
        print(name, 'is not d-3 vertex-fault-tolerant Hamiltonian connected')
            
