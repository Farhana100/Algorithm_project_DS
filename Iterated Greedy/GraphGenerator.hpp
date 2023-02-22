class GraphGenerator {
public:
    vector<vector<int>> RandomGraph(int n, int m) {
        vector<vector<int>> G(n);
        vector<pair<int, int>> edges;
        for(int i = 0; i < n; i++) {
            for(int j = i+1; j < n; j++) {
                edges.push_back({i, j});
            }
        }
        // Seed the random number generator
        srand(time(0));
        random_shuffle(edges.begin(), edges.end());
        for(int i = 0; i < m; i++) {
            int u = edges[i].first, v = edges[i].second;
            G[u].push_back(v);
            G[v].push_back(u);
        }
        return G;
    }

    vector<vector<int>> RandomGraph(int n) {
        int min_edges = n-1;
        int max_edges = n*(n-1)/2;
        int m = rand()%(max_edges-min_edges+1) + min_edges;
        return RandomGraph(n, m);
    }

    vector<vector<int>> RandomGraph() {
        int min_nodes = 1;
        int max_nodes = 20;
        int n = rand()%(max_nodes-min_nodes+1) + min_nodes;
        return RandomGraph(n);
    }
};