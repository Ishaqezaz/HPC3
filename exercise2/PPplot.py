import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def format_bytes(size):
    power = 1024
    n = 0
    powers = {0: 'B', 1: 'KiB', 2: 'MiB', 3: 'GiB'}
    while size > power:
        size /= power
        n += 1
    return f"{size:.2f} {powers[n]}"

def plot_data(filename, mode):
    data = pd.read_csv(filename, delim_whitespace=True, header=None, names=['Message Size', 'Time'])

    # Plot
    plt.figure(figsize=(10, 5))
    plt.plot(data['Message Size'], data['Time'], marker='o', linestyle='-', color='blue')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Message size')
    plt.ylabel('Ping-Pong time (S)')
    plt.title('Ping-Pong times vs. size on ' + mode)
    plt.grid(True)

    ticks = [2**n for n in range(3, 31)]
    plt.xticks(ticks, [format_bytes(t) for t in ticks], rotation=45)

    plt.tight_layout()
    plt.show()


plot_data('results/inter_node.txt', 'Inter-node')
plot_data('results/intra_node.txt', 'Intra-node')
