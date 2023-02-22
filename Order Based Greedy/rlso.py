import numpy as np
from env import *
from Graph import Graph

# cant fix seed otherwise RLSoMDS will always choose the same j for purturbation in every iteration
# np.random.seed(11)
# low_gamma is k

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
            # if (it % 100 == 0):
            #     print('iteration:', it)
            #     print('MDS so far:', self.MDS)
            #     print()

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

    def setLowGamma(self, low_gamma):
        self.low_gamma = low_gamma