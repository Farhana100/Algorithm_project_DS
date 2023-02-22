import numpy as np
from env import *
from Graph import Graph
from GraphGenerator import *
from rlso import *
from bruteForce import *


if __name__ == "__main__":

    # # take console input -------------------------------------------------------->>>
    # n = int(input("Enter number of nodes: "))
    # e = int(input("Enter number of edges: "))
    # for i in range(e):
    #     u, v = map(int, input().split())
    #     adj[u].append(v)
    #     adj[v].append(u)


    # take graph input from file  -------------------------------------------------------->>>
    # with open(INPUT_FILE, "r") as f:
    #     n = int(f.readline())
    #     e = int(f.readline())

    #     adj = [[] for i in range(n)]

    #     for line in f:
    #         u, v = map(int, line.split())
    #         adj[u].append(v)
    #         adj[v].append(u)

    # G = Graph(n, e, adj)

    # generate random graph -------------------------------------------------------->>>
    n = int(input("Enter number of nodes: "))
    e = int(input("Enter number of edges: "))
    G = generate_graph(n, e)
    textDump(G, 'graph1.txt')


    print('--------RLSo experiment setup-------')
    G.printGraph()
    print()

    rlso = RLSo(G, 0)
    bf = BruteForce(G, 0)


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

        rlso.setLowGamma(low_gamma)
        MDS, p = rlso.RLSoMDS()

        print('MDS:', MDS)
        print('p:', p)

        print('---------------------------------')
        print('brute force experiment setup')
        bf.setK(low_gamma)
        MDS_brute = bf.bruteForce()
        print('MDS:', MDS_brute)


        print()


    print('experiment done')
