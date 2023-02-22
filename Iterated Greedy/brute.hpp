typedef vector<vector<int>> Graph;


/**
 * @brief Gets minimum dominating set of G using brute force
 * Time Complexity: O(n*2^n)
 * Works for n <= 20
 * 
 * @param G input graph
 * @return vector<int>: minimum dominating set of G
 */
vector<int> BruteMDSP(Graph G) {
    int n = G.size();
    vector<int> D;
    int cur_size = 1000;

    // iterate over all subset of vertices
    for(int mask = 0; mask < (1<<n); mask++) {
        vector<bool> is_dominated(n, false);
        vector<int> D_cur;

        for(int u = 0; u < n; u++) {
            if(mask & (1<<u)) {
                D_cur.push_back(u);
                is_dominated[u] = true;
                for(int v: G[u])
                    is_dominated[v] = true;
            }
        }
        
        // check if D_cur is a dominating set
        int dominated_count = 0;
        for(int u = 0; u < n; u++) dominated_count += is_dominated[u];
        if(dominated_count < n) continue;

        // check if D_cur is minimal
        if(D_cur.size() < cur_size) {
            D = D_cur;
            cur_size = D_cur.size();
        }
    }

    return D;
}
