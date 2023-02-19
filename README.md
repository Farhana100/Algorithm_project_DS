# Order-based randomised local search (RLSo) for MDS

A Python implementation of the RLSo algorithm for MDS.

RLSo is described in the paper: [Order-based randomised local search for the multidimensional scaling problem](https://doi.org/10.1016/j.cor.2019.105100).

This paper converts the MDS problem into a permutation search problem and uses a randomised local search algorithm to find a permutation of the nodes of a graph which will generate the MDS of the graph. A greedy algorithm is used to find the minimal dominating set of a graph given a specific permutation of the nodes of the graph. The RLSo generates permutation until a dominating set of size k at maximum is found (or number of max iteration is exceeded).

## Installation
* Clone the repository
* Install the requirements: `pip install -r requirements.txt`

## Usage
* Create a file `graph.txt` with the graph in the following format:

    > number_of_nodes \
    > number_of_edges \
    > u v 

* Run the script `python rlso.py`
* enter the lower bound of gamma (maximum size of dominating set, k)

## Example
* The file `graph.txt` contains the graph of the example in the paper.
* Run the script `python rlso.py`
* enter the lower bound of gamma (maximum size of dominating set, k): 3
