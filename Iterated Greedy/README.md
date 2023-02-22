# Iterated Greedy Algorithm for Minimum Dominating Set Problem (MDSP)

## How to Run
`test.cpp` file contains code for generating the performance metrics of IG algorithm. For different number of nodes, it generates different graphs and performs both IG and Brute force to compare the result of IG.

The results are written to a text file `results.txt`. 

`run.py` file visualizes the performace metrics from `results.txt` in plots.

You can directly execute `run.py` and use an optional argument whether or not you want to run `test.cpp` too or not

1. **To only visualize the plots** (considering that `results.txt` contains the performance metrics)
    ```bash
    python run.py
    ```
2. **To re-run the experiment**, i.e perform IG and brute on some randomly generated graphs and use their results to visualize plots
    ```bash
    python run.py test
    ```
3. **To run IG on predefined input sets**, i.e on `input_1.txt`, `input_2.txt` or `input_3.txt`
    ```bash
    g++ main.cpp -o main.exe && main.exe
    ```

## Overview of the algorithm

The work is focused on designing a metaheuristic algorithm to approximate the minimum dominating set and therefore the domination number for arbitrary graphs, even for graph mining, that are large scale real-world graphs. Specifically, an *Iterated Greedy (IG)* algorithm is proposed to address this problem based on the idea of starting from an initial solution that will be destructed and reconstructed in an iterative way until a stopping criterion is met

- IG starts by creating an initial solution
- It then tries to locally improve that solution, by searching the *neighbour solutions* in the search space
- The algorithm then iteratively destructs the solution, reconstructs and locally improves the solution
- It keeps doing these until a certain number of iterations have passed without any improvement

```cpp
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
```

After `delta` iterations with no improvements, the algorithm stops

### Initial Solution
Starting from an empty solution, we iteratively select **the most promising** vertex to be included in the next iteration until reaching a feasible solution. (A feasible solution is just a set which is indeed dominatin set). This called *Greedy Insertion Procedure*

**The most promising** vertex is chosen in terms of *how much a vertex will contribute* if it is included in the current set? In mathematical terms, $g_{GIP}(v) = |N[v]$ \ $ N[D] |$, where $N[u]$ means the neighbour set of $u$ along with $u$ itself

So, we include the vertex that has the maximum $g_{GIP}$ value.

A better improvement: Instead of starting from an empty solution, we initialize D with the support vertices of $G$. The vertices which have atleast one leaf as its neighbour are support vertices.

It may happen the initial solution thus formed contains some redundant vertices. That is, if $D-u$ is also a dominating set, then we remove all such $u$ (`checkP` method does this)

```cpp
vector<int> InitialSolution(const Graph &G) {   // O(n^3)
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
```

## Local Improvement
Definition of local improvement is given by 3 main components:
1. The move operator
2. The neighbourhood explored
3. How is the neighbourhood explored (the stratedy)

**The move operator:** Say we have a feasible solution $D$. The move operator is exchanging a vertex $u$ from $D$ with a vertex $v$ not from $D$.

$Exchange(D,u,v)$ -> $(D$ \ $\{u\}) U \{v\}$

**The neighbourhood Explored:** It is fairly obvious. If the above exchange operation results in a feasible solution, only then we consider that as a neighbour, otherwise not

**The strategy to explore the neighbours:** There are two main strategys. 
    
    1. Best Improvement: Explore all neighbours and move to the neighbour that has the best improvement
    2. First Improvement: Whenever a neighbour has an improvement, move to that neighbour

This algorithm uses first improvement, as it ensures better performance with respect to time, although may not lead to a local optimul

## Destruction
Randomly remove `beta` percentage of vertices from current solution

## Reconstruction
Similar to that in initial solution. 
- Iteratively select **the most promising** vertex until the resulting set becomes a feasible solution.
- Remove all redundant vertices

## Structural Complexity
Consider p as the cardinality of the solution. Upper bound n/2

Summarizing, a single iteration of our IG algorithm performs a destruction phase, O(βp); a reconstruction phase,O(n − p); a checking, O(pn); and a local search method, O(p·p·n). Then, the complexity of an IG iteration is evaluated as the maximum complexity of the inner methods, which is the local search complexity, O(p·p·n)=O(n^3).

Notice that IG is executed a maximum number of iterations without improvement, which cannot be analyzed from a complexity point of view.


May 2023: [Paper Link](https://www.sciencedirect.com/science/article/pii/S0378475422005055#:~:text=A%20dominating%20set%20in%20a%20graph%20is%20a,that%20has%20been%20proved%20to%20be%20NP%20-hard)
