import copy
import itertools

def isHamiltonianConnected(i, j, matrix):
    """
    Check whether there exists a Hamiltonian path from i to j in the graph
    
    Parameters:
        i: Starting node
        j: target node
        matrix: The adjacency matrix representation of a graph
        
    Return:
        If a Hamiltonian path exists, return the list of paths; otherwise, return -1
    """
    n = len(matrix)
    # Check boundary conditions
    if i < 0 or i >= n or j < 0 or j >= n:
        return -1
    if n == 1:
        return [i] if i == j else -1
    
    # Record the nodes that have been visited
    visited = [False] * n
    # Record the path with starting vertex i
    path = [i]
    visited[i] = True
    
    # Backtracking function
    def backtrack(current):
        # If the path length is equal to the number of vertices and the current vertex is the target j, then a Hamiltonian path is found
        if len(path) == n:
            return current == j
        
        # Try to visit all unvisited vertices that are connected to the current vertex
        for next_node in range(n):
            if not visited[next_node] and matrix[current][next_node] == 1:
                visited[next_node] = True
                path.append(next_node)
                
                # Recursively explore the next node
                if backtrack(next_node):
                    return True
                
                # Backtrack
                path.pop()
                visited[next_node] = False
        
        return False
    
    # Start backtracking search
    if backtrack(i):
        return path
    else:
        return -1

def generate_k_combinations(lst, k):
    """
    Generate all k-combinations of elements in the list lst
    
    Parameters:
        lst: A list of elements
        k: The number of elements in each combination
        
    Return:
        A list of all k-combinations, where each combination is a sublist
    """
    # Check input validity
    if k < 0 or k > len(lst):
        return []
    
    # Use itertools.combinations to generate combinations, then convert them to list form
    combinations = itertools.combinations(lst, k)
    return [list(comb) for comb in combinations]

if __name__ == '__main__':
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

    graphs = [J_4_2, J_5_2]

    for order, matrix in enumerate(graphs):
        name = 'J(4,2)' if order == 0 else 'J(5,2)'
        n = len(matrix)
        d = sum(1 for j in range(n) if matrix[0][j] == 1)
        t = 0
        # Get the set of edges
        edges = []
        for i in range(n-1):
            for j in range(i+1,n):
                if matrix[i][j] == 1:
                    edges.append((i,j))
        # Get all possible sets of fault edges
        allSetOfFaultyEdeges = generate_k_combinations(edges, d - 3)
        batchSize = len(allSetOfFaultyEdeges)
        
        HamiltonianConnectedness = True

        for setOfFaultyEdges in allSetOfFaultyEdeges:
            faultymatrix = copy.deepcopy(matrix)
            t += 1
            completed = (t * 100) // batchSize 
            print(f"\r{name} progress: {completed}%", end='', flush=True)
            for k, l in setOfFaultyEdges:
                faultymatrix[k][l] = 0
                faultymatrix[l][k] = 0
            for i in range(n-1):
                for j in range(i+1,n):
                    if isHamiltonianConnected(i,j,faultymatrix) == -1:
                        HamiltonianConnectedness = False
                        print('Faulty edges:',setOfFaultyEdges,'Endpoints',i,j)
        print(f"\n{name} completed")
        if HamiltonianConnectedness:
            print(f'The graph {name} is d-3 edge-fault-tolerant Hamiltonian connected')
        else:
            print(f'The graph {name} is not d-3 edge-fault-tolerant Hamiltonian connected')
