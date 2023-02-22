import numpy  as np
from env import *
from Graph import Graph
from GraphGenerator import *
from rlso import *
from bruteForce import *
import time
import matplotlib.pyplot as plt

FILES_DIR_TIME = 'Order Based Greedy/time/'
TESTS = 10

if __name__ == "__main__":

    # range of n
    # n_range = np.arange(10, 30, 2)
    n_range = np.arange(10, 20, 2)

    n = 100
    max_e = int(n * (n - 1) / 2)
    e = np.array([int(n * (n - 1) / pow(2, i)) for i in np.arange(2, 3.5, 0.5)])
    e = np.concatenate((np.flip(e)[:-1], np.cumsum(e)))
    e[e > max_e] = max_e
    
    print(e)
    print()


    # creating n vs e matrix
    n_e_matrix = []

    for n in n_range:
        max_e = int(n * (n - 1) / 2)
        e = np.array([int(n * (n - 1) / pow(2, i)) for i in np.arange(2, 3.5, 0.5)])
        e = np.concatenate((np.flip(e)[:-1], np.cumsum(e)))
        e[e > max_e] = max_e
        n_e_matrix.append(e)
    n_e_matrix = np.array(n_e_matrix)

    print(n_e_matrix)

    # 2d array of dictionaries
    # each dictionary contains time taken by rls and bf for a particular n and e
    time_dict = np.array([{} for i in range(len(n_range)) for j in range(len(n_e_matrix[i]))])
    time_dict = time_dict.reshape(n_e_matrix.shape)
    print(time_dict)


    for i in range(len(n_range)):
        print("==================================================")
        print("starting experiment for n = ", n_range[i])
        for j in range(len(n_e_matrix[i])):

            n = n_range[i]
            e = n_e_matrix[i][j]

            print("e = ", e)

            time_dict[i][j]['n'] = n
            time_dict[i][j]['e'] = e
            time_dict[i][j]['bf_time'] = 0
            time_dict[i][j]['bf_solve'] = 0
            time_dict[i][j]['rlso_time'] = 0
            time_dict[i][j]['rlso_solve'] = 0


            for k in range(TESTS):
                # run TESTS times
                graph = generate_graph(n, e)


                # print("Brute Force")
                bf = BruteForce(graph)
                
                start_time = time.time()
                mds_bf = bf.bruteForce()
                end_time = time.time()
                # print("MDS = ", mds_bf)
                # print("bf time = ", end_time - start_time)
                time_dict[i][j]['bf_time'] += (end_time - start_time)*1000
                time_dict[i][j]['bf_solve'] += len(mds_bf)
                # print()

                # print("RLSO")
                rls = RLSo(graph, low_gamma=len(mds_bf))

                start_time = time.time()
                mds, p = rls.RLSoMDS()
                end_time = time.time()
                # print("MDS = ", mds)
                # print("p = ", p)
                # print("rlso time = ", end_time - start_time)
                time_dict[i][j]['rlso_time'] += (end_time - start_time)*1000
                time_dict[i][j]['rlso_solve'] += len(mds_bf)
                # time_dict[i][j]['rlso_perm'] = p

            time_dict[i][j]['bf_time'] = time_dict[i][j]['bf_time'] / TESTS
            time_dict[i][j]['bf_solve'] = time_dict[i][j]['bf_solve'] / TESTS
            time_dict[i][j]['rlso_time'] = time_dict[i][j]['rlso_time'] / TESTS
            time_dict[i][j]['rlso_solve'] = time_dict[i][j]['rlso_solve'] / TESTS
            print()

            print("bf time = ", time_dict[i][j]['bf_time'])
            print("bf solve = ", time_dict[i][j]['bf_solve'])
            print("rlso time = ", time_dict[i][j]['rlso_time'])
            print("rlso solve = ", time_dict[i][j]['rlso_solve'])

            print("--------------------------------------------------")
            print()

        print("==================================================")
        print()

    print('-------------- end exp --------------------')

    # save time_dict
    np.save(FILES_DIR_TIME + 'time_dict.npy', time_dict)

    # load time_dict
    # time_dict = np.load(FILES_DIR + 'time_dict.npy', allow_pickle=True)
    print(time_dict)


    # generate plot
    plt.figure(figsize=(10, 10))
    plt.title("time vs edges")
    plt.xlabel("edges")
    plt.ylabel("time")
    plt.grid()

    # for i in range(len(n_range)):
    #     plt.plot(n_e_matrix[i], [time_dict[i][j]['bf_time'] for j in range(len(n_e_matrix[i]))], label="bf n = " + str(n_range[i]))

    #     plt.grid()
    #     plt.title("time vs edges" + " n = " + str(n_range[i]))
    #     plt.legend()
    #     plt.savefig(FILES_DIR_TIME + "time_vs_edges_n_bf" + str(n_range[i]) + ".png")
    #     plt.clf()
            

    # for i in range(len(n_range)):
    #     plt.plot(n_e_matrix[i], [time_dict[i][j]['rlso_time'] for j in range(len(n_e_matrix[i]))], label="rlso n = " + str(n_range[i]))

    #     plt.grid()
    #     plt.title("time vs edges" + " n = " + str(n_range[i]))
    #     plt.legend()
    #     plt.savefig(FILES_DIR_TIME + "time_vs_edges_n_rlso" + str(n_range[i]) + ".png")
    #     plt.clf()
            


    # time vs nodes
    plt.figure(figsize=(10, 10))
    plt.title("time vs nodes")
    plt.xlabel("nodes")
    plt.ylabel("time")
    plt.grid()

    e_it = int(n_e_matrix.shape[1]/2)

    plt.plot(n_range, [time_dict[i][e_it]['bf_time'] for i in range(len(n_range))], label="bf")
    plt.plot(n_range, [time_dict[i][e_it]['rlso_time'] for i in range(len(n_range))], label="rlso")

    plt.title("time vs nodes")
    plt.legend()
    plt.savefig(FILES_DIR_TIME + "time_vs_nodes.png")
    # plt.show()   

    # time vs nodes
    plt.figure(figsize=(10, 10))
    plt.title("time vs nodes")
    plt.xlabel("nodes")
    plt.ylabel("time")
    plt.grid()

    e_it = int(n_e_matrix.shape[1]/2)

    plt.plot(n_range, [time_dict[i][e_it]['bf_time'] for i in range(len(n_range))], label="bf")

    plt.title("time vs nodes")
    plt.legend()
    plt.savefig(FILES_DIR_TIME + "time_vs_nodes_bf_time.png")
    # plt.show()   


    # time vs nodes
    plt.figure(figsize=(10, 10))
    plt.title("bruteforce time vs nodes")
    plt.xlabel("nodes")
    plt.ylabel("time")
    plt.grid()

    e_it = int(n_e_matrix.shape[1]/2)

    plt.plot(n_range, [time_dict[i][e_it]['rlso_time'] for i in range(len(n_range))], label="rlso")

    plt.title("RLSo time vs nodes")
    plt.legend()
    plt.savefig(FILES_DIR_TIME + "time_vs_nodes_rlso_time.png")
    # plt.show()   

