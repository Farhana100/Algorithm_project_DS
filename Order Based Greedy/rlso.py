import numpy as np
from env import *

# cant fix seed otherwise RLSoMDS will always choose the same j for purturbation in every iteration
# np.random.seed(11)


class Graph:
    def __init__(self, n, e, adj):
        self.n = n
        self.e = e
        self.adj = adj

    def printGraph(self):
        print('Number of nodes:', self.n)
        print('Number of edges:', self.e)
        print('Adjacency list:')
        for i in range(self.n):
            print(i, end=" -> ")
            for j in self.adj[i]:
                print(j, end=" ")
            print()

        print()


class RLSo:
    def __init__(self, G, low_gamma, max_iter=MAX_ITER):
        self.G = G
        self.low_gamma = low_gamma
        self.max_iter = max_iter
        self.p = np.random.permutation(self.G.n)
        self.MDS = list(range(self.G.n))

    def greedyMDS(self, p):
        n = self.G.n
        adj = self.G.adj

        S = []
        D = np.ones(n)  # D[v] = 1 if v is non-dominated in S, 0 otherwise

        for i in p:
            if len(S) == n:
                # all nodes are dominated
                break

            if D[i] == 1 or D[adj[i]].any() == 1:
                S.append(i)
                D[i] = 0
                D[adj[i]] = 0
        return S

    def RLSoMDS(self):
        n = self.G.n

        for it in range(self.max_iter):
            if (it % 100 == 0):
                print('iteration:', it)
                print('MDS so far:', self.MDS)
                print()

            if len(self.MDS) <= self.low_gamma:
            # if len(self.MDS) <= self.low_gamma * n:
                break
            # random integer between 1 and n-1
            i = np.random.randint(1,n, 1)[0]

            # perturb p
            perturbed_p = np.concatenate((np.roll(self.p[:i], -1), self.p[i:]))

            # greedy MDS
            S = self.greedyMDS(perturbed_p)

            # update MDS
            if len(S) <= len(self.MDS):
                self.MDS = S
                self.p = perturbed_p

        return (self.MDS, self.p)




if __name__ == "__main__":

    # # take console input
    # n = int(input("Enter number of nodes: "))
    # e = int(input("Enter number of edges: "))
    # for i in range(e):
    #     u, v = map(int, input().split())
    #     adj[u].append(v)
    #     adj[v].append(u)


    # take graph input from file
    with open("graph.txt", "r") as f:
        n = int(f.readline())
        e = int(f.readline())

        adj = [[] for i in range(n)]

        for line in f:
            u, v = map(int, line.split())
            adj[u].append(v)
            adj[v].append(u)

    G = Graph(n, e, adj)



    print('--------RLSo experiment setup-------')
    G.printGraph()
    print()

    # run while loop until user enters a valid gamma
    while True:
        print('---------------------------------')
        
        
        # low_gamma = float(input("Enter low gamma: "))
        # if low_gamma < 0 or low_gamma > 1:
        #     break

        # print('looking for Dominating set of size at max', int(low_gamma * n), '...')
        # print()

        low_gamma = int(input("Enter low gamma: "))
        if low_gamma <= 0 or low_gamma > n:
            break
        
        print('looking for Dominating set of size at max', low_gamma, '...')
        print()

        rlso = RLSo(G, low_gamma)
        MDS, p = rlso.RLSoMDS()

        print('MDS:', MDS)
        print('p:', p)

        print()


    print('experiment done')
