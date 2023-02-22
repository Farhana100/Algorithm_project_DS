#include <bits/stdc++.h>
using namespace std;

#include "IteratedGreedy.hpp"
#include "brute.hpp"
#include "GraphGenerator.hpp"


int main() {

    ofstream fout("results.txt");

    GraphGenerator G;
    double total_accuracy = 0;
    double total_avg_diff = 0;
    int iters, n1, n2;
    cout << "Enter number of iterations: ";
    cin >> iters;
    cout << "Enter range of n: ";
    cin >> n1 >> n2;

    fout << "n,accuracy,avg_diff\n";

    for(int n = n1; n <= n2; n++) {
        cout << "--------------------- n = " << n << "----------------------------\n";
        double accuracy = 0;
        double avg_diff = 0;
        for(int i = 0; i < iters; i++) {
            cout << "Iteration " << i << "/" << iters << " ... ";

            Graph G1 = G.RandomGraph(20);
            vector<int> D1, D2;
            D1 = IteratedGreedy(G1, 0.5, 10);
            D2 = BruteMDSP(G1);
            avg_diff += abs((int)D1.size() - (int)D2.size());
            accuracy += (D1.size() == D2.size());
            
            cout << " Done\n";
        }
    
        total_accuracy += accuracy;
        total_avg_diff += avg_diff;

        avg_diff /= iters;
        accuracy /= iters;
        fout << n << "," << fixed << setprecision(5) << accuracy << "," << avg_diff << "\n";
    }

    total_accuracy /= ((n2-n1+1)*iters);
    total_avg_diff /= ((n2-n1+1)*iters);

    cout << "Total Accuracy: " << fixed << setprecision(5) << total_accuracy << "\n";
    cout << "Total Avg Diff: " << fixed << setprecision(5) << total_avg_diff << "\n";

    return 0;
}

/**
Total Accuracy: 0.92727
Total Avg Diff: 0.07727  
*/