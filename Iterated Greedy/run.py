import matplotlib.pyplot as plt
import csv
import os, sys


def plot_chart(x, y, title, xlabel, ylabel, color, filename, ylim=None):
    plt.plot(x, y, color=color)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.ylim(ylim)
    plt.savefig(filename)
    plt.clf()


def read_file(filename):
    with open(filename) as f:
        reader = csv.reader(f)
        # skip header
        next(reader)
        data = list(reader)
    return data


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        """
        Run test.cpp and regenerate results.txt
        """
        if os.system('g++ test.cpp -o test.exe && test.exe') == 0:
            print('Compiled and ran test.cpp successfully.')
        else:
            print('Failed to compile and run test.cpp.')
            exit(1)

    data = read_file('results.txt')
    n = [int(row[0]) for row in data]
    accuracy = [float(row[1]) for row in data]
    avg_diff = [float(row[2]) for row in data]
    ig_time = [float(row[3]) for row in data]
    brute_time = [float(row[4]) for row in data]
    
    plot_chart(n, accuracy, 'IG Performance: Accuracy', 'n', 'accuracy', 'tab:blue','accuracy.png', [0,1.1])
    plot_chart(n, avg_diff, 'IG Performance: Average Difference', 'n', 'avg_diff', 'tab:orange','avg_diff.png')

    plt.plot(n, ig_time, color='tab:blue', label='IG')
    plt.plot(n, brute_time, color='tab:orange', label='Brute Force')
    plt.legend()
    plt.title('Performance Comparison: Time')
    plt.yscale('log')
    plt.xlabel('n')
    plt.ylabel('time (log scaled micro-second)')
    plt.savefig("Time.png")
    plt.clf()