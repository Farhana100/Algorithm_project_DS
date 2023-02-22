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
