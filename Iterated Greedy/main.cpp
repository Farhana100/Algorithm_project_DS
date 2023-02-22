#include <bits/stdc++.h>
using namespace std;

#include "IteratedGreedy.hpp"
#include "brute.hpp"


int main() {
    
    string filename, strategy;
    cout << "Enter filename: ";
    cin >> filename;

    freopen(filename.c_str(), "r", stdin);

    int n, m;
    cin >> n >> m;
    Graph G(n);
    for(int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        G[u].push_back(v);
        G[v].push_back(u);
    }

    vector<int> D1, D2;
    D1 = IteratedGreedy(G, 0.5, 10);
    D2 = BruteMDSP(G);
    
    cout << "Iterated Greedy: ";
    for(int u: D1) cout << u << " ";
    cout << endl;

    cout << "Brute Force: ";
    for(int u: D2) cout << u << " ";
    cout << endl;

    return 0;
}


/**
 * Outputs:
 * 1 -> 11 2 5 6
 * 2 -> 0 6 4
 * 3 -> 0 9 7 1
 * 
 */