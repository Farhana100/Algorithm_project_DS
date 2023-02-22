# generate a random graph with n nodes and m edges
# the graph is represented by an adjacency list
# the graph is undirected
# the graph is unweighted
# the graph is simple
# the graph is may not be connected

import random
from Graph import Graph

def generate_graph(n, m):
    if m > n*(n-1)/2:
        print("m is too large")
        return
    
    adj = [[] for i in range(n)]
    
    for i in range(m):
        while True:
            u = random.randint(0, n-1)
            v = random.randint(0, n-1)
            if u != v and v not in adj[u]:
                adj[u].append(v)
                adj[v].append(u)
                break
    return Graph(n, m, adj)

def textDump(G, filename):
    with open(filename, 'w') as f:
        f.write(str(G.n) + '\n')
        f.write(str(G.e) + '\n')
        for i in range(G.n):
            for j in G.adj[i]:
                if i < j:
                    f.write(str(i) + ' ' + str(j) + '\n')