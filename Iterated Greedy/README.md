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

May 2023: [Paper Link](https://www.sciencedirect.com/science/article/pii/S0378475422005055#:~:text=A%20dominating%20set%20in%20a%20graph%20is%20a,that%20has%20been%20proved%20to%20be%20NP%20-hard)
