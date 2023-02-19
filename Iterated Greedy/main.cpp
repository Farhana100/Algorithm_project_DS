/**
 * N(v) = set of vertices adjacent to v
 * N[v] = N(v) U {v}
 * v is dominated by D if v is in N[D]
 * Support vertex is a vertex adjacent to a leaf vertex
 * L = set of leaf vertices
 * SV = set of support vertices
 */

#include <bits/stdc++.h>
using namespace std;


typedef vector<vector<int>> Graph;


/**
 * @brief Get the list representing how many times a vertex in G is dominated by D
 * 
 * @param D dominating set
 * @param G graph
 * @return vector<int> list representing how many times a vertex in G is dominated by D
 */
vector<int> getDominatedCount(const vector<int> &D, const Graph &G) {
    int n = G.size();
    vector<int> dominatedCount(n, 0);
    for(int u: D) {
        dominatedCount[u]++;
        for(int v: G[u])
            dominatedCount[v]++;
    }
    return dominatedCount;
}


/**
 * @brief Remove all redundant vertices from D.
 * A vertex u is redundant if N[u] is dominated by D-{u}
 * 
 * @param D input dominating set
 * @param G input graph
 * @return vector<int>: the new dominating set
 */
vector<int> checkP(const vector<int> &D, const Graph &G) {
    int n = G.size();
    vector<int> redundants, D_b;
    vector<int> dominatedCount = getDominatedCount(D, G);

    for(int u: D) {
        dominatedCount[u]--;
        int mn = dominatedCount[u];
        for(int v: G[u]) {
            dominatedCount[v]--;
            mn = min(mn, dominatedCount[v]);
        }

        if(mn>0) redundants.push_back(u);
    
        dominatedCount[u]++;
        for(int v: G[u]) 
            dominatedCount[v]++;
    }

    for(int i = 0, j = 0; i < D.size(); i++) {
        if(j < redundants.size() && D[i] == redundants[j]) j++;
        else D_b.push_back(D[i]);
    }

    return D_b;
}


/**
 * @brief Greedy Insert Procedure: #of newly dominated vertices by adding u to D
 * 
 * @param u Node to be inserted in D
 * @param D Dominating set
 * @param G Graph
 * @return int: GIP value of u
 */
int GIP(int u, const vector<int> &D, const Graph &G) {
    int n = G.size();
    vector<int> dominatedCount = getDominatedCount(D, G);   // O(|D|) = O(n/2) = O(n)
    int notDominatedCount = (dominatedCount[u] == 0);
    for(int v: G[u])             // O(|N[u]|) = O(n)
        notDominatedCount += (dominatedCount[v] == 0);

    return notDominatedCount;
}


bool isLeaf(int u, const Graph &G) {
    return G[u].size() == 1;
}


/**
 * @brief Performs a BFS to find all support vertices
 * 
 * @param G input Graph
 * @return vector<int>: list of support vertices
 */
vector<int> getSupportVertices(const Graph &G) {
    int n = G.size();
    vector<int> SV;
    vector<bool> visited(n, false);
    queue<int> q;
    q.push(0);
    visited[0] = true;
    while(!q.empty()) {
        int u = q.front();
        q.pop();
        for(int v: G[u]) {
            if(visited[v]) continue;
            if(isLeaf(v, G)) SV.push_back(u);
            q.push(v);
            visited[v] = true;
        }
    }
    return SV;
}


/**
 * @brief Get the initial solution for IG using Greedy Insertion Procedure
 * 
 * @param G input graph
 * @return vector<int>: initial dominating set
 */
vector<int> InitialSolution(const Graph &G) {
    int n = G.size();
    vector<int> D = getSupportVertices(G);      // O(n)
    while(true) {                               // O(|D|) = O(n/2) = O(n)
        int maxGIP = 0;
        int toPush = -1;
        for(int u = 0; u < n; u++) {            // O(n)
            int gip = GIP(u, D, G);             // O(n): Could be optimized
            if(gip > maxGIP) {
                maxGIP = gip;
                toPush = u;
            }
        }
        if(toPush != -1) D.push_back(toPush);
        else break;
    }
    vector<int> D_b = checkP(D, G);             // O(n)
    return D_b;
}


/**
 * @brief Definition of local improvement is given by 3 main components:
 * 1. the move operator
 * 2. the neighbourhood explored
 * 3. the strategy to explore the neighbourhood
 * 
 * The move operator is: 
 *  Exchange(u, v) = D-{u} U {v}
 *  where u is a vertex in D and v is a vertex not in D
 * 
 * The neighbourhood explored is:
 *  the next solution reached by performing the move operator on D
 * 
 * The strategy to explore the neighbourhood is:
 * the first solution that improves the objective function
 * Exchange(u,v) if the vertices dominated only by u are dominated by v
 * 
 * @param D 
 * @return vector<int> 
 */
vector<int> LocalImprovement(vector<int> D, const Graph &G) {
    int n = G.size();
    vector<int> D_b;
    vector<int> dominatedCount = getDominatedCount(D, G);
    vector<int> notD;
    
    for(int u = 0; u < n; u++) 
        if(find(D.begin(), D.end(), u) == D.end()) notD.push_back(u);
    
    for(int u: D) {
        dominatedCount[u]--;
        for(int w: G[u]) dominatedCount[w]--;
        
        for(int v: notD) {
            // inserting v in D
            dominatedCount[v]++;
            for(int w: G[v]) dominatedCount[w]++;
            
            int mn = *min_element(dominatedCount.begin(), dominatedCount.end());
            if(mn>0) {
                D_b = D;
                D_b.erase(find(D_b.begin(), D_b.end(), u));
                D_b.push_back(v);
                D_b = checkP(D_b, G);
                if(D_b.size() < D.size()) return D_b;
            } 

            // removing v from D
            dominatedCount[v]--;
            for(int w: G[v]) dominatedCount[w]--;
        }

        dominatedCount[u]++;
        for(int v: G[u]) dominatedCount[v]++;
    }

    // no local improvement
    return D;
}


/**
 * @brief Randomly remove beta percentage of vertices from D
 * 
 * @param D input Dominating Set
 * @param beta percentage of vertices to be removed
 * @return vector<int>: unfeasible dominating set
 */
vector<int> Destruction(vector<int> D, float beta) {
    vector<int> D_b = D; 

    // Seed the random number generator
    random_device rd;
    mt19937 g(rd());

    // Determine how many vertices to remove
    int num_vertices_to_remove = (int)((int)D_b.size()*beta);

    // Shuffle the vertices in D_b
    shuffle(D_b.begin(), D_b.end(), g);

    // Remove the first num_vertices_to_remove vertices from D_b
    D_b.erase(D_b.begin(), D_b.begin() + num_vertices_to_remove);

    return D_b;
}


/**
 * @brief Reconstruct a feasible solution from D using GIP
 * 
 * @param D unfeasible solution
 * @param G input graph
 * @return vector<int>: feasible solution
 */
vector<int> Reconstruction(vector<int> D, const Graph &G) {
    int n = G.size();
    while(true) {                               // O(|D|) = O(n/2) = O(n)
        int maxGIP = 0;
        int toPush = -1;
        for(int u = 0; u < n; u++) {            // O(n)
            int gip = GIP(u, D, G);             // O(n): Could be optimized
            if(gip > maxGIP) {
                maxGIP = gip;
                toPush = u;
            }
        }
        if(toPush != -1) D.push_back(toPush);
        else break;
    }
    D = checkP(D, G);                           // O(n)
    return D;
}


/**
 * @brief 
 * 
 * @param G input graph
 * @param beta percentage of vertices removed in destruction phase
 * @param delta maximum number of iterations without improvement that IG allows to perform (stopping criterion)
 */
vector<int> IteratedGreedy(vector<vector<int>> G, int beta, int delta) {
    vector<int> D = InitialSolution(G);
    vector<int> D_b = LocalImprovement(D, G);
    int currentIterations = 0;
    while(currentIterations < delta) {
        D_b = Destruction(D_b, beta);
        vector<int> D_r = Reconstruction(D_b, G);
        vector<int> D_i = LocalImprovement(D_r, G);
        if(D_i.size() < D_r.size()) {
            D_b = D_i;
            currentIterations = 0;
        } 
        else {
            currentIterations++;
        }
    }
    return D_b;
}


int main() {
    // TODO: Testing   
    return 0;
}
