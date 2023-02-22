import numpy as np
from env import *
from Graph import Graph

# bruteforce algorithm to find dominating set of size at most k or low_gamma

class BruteForce:
    def __init__(self, G, k=None):
        self.G = G
        self.k = k

    def bruteForce(self):
        G = self.G
        k = self.k

        n = G.n
        adj = G.adj

        # generate all subsets
        subsets = []
        if k is None:
            for i in range(2**n):
                subset = []
                for j in range(n):
                    if i & (1 << j):
                        subset.append(j)
                subsets.append(subset)
        else:
            # generate all subsets of size k
            for i in range(2**n):
                subset = []
                for j in range(n):
                    if i & (1 << j):
                        subset.append(j)
                if len(subset) == k:
                    subsets.append(subset)

        # find dominating set
        for subset in subsets:
            is_dominating = True
            for i in range(n):
                s = set(adj[i])
                s.add(i)
                if not s.intersection(set(subset)):
                    is_dominating = False
                    break
            if is_dominating:
                return subset

        return None

    def setK(self, k):
        self.k = k