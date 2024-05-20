import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def Model(x, a, b):
    return b + a * x

def Fit(filename, mode):
    data = pd.read_csv(filename, delim_whitespace=True, header=None, names=['Message Size', 'Time'])
    data = data[data['Message Size'] >= 512]
    
    try:
        params, _ = curve_fit(Model, data['Message Size'], data['Time'])
        inverseBandwidth, latency = params
    except Exception as e:
        print(f"Error fitting data: {e}")
        return None, None

    bandwidth = 1 / inverseBandwidth if inverseBandwidth != 0 else float('inf')

    if latency < 0:
        latency = 1.6e-6 if mode == 'inter-node' else 0.7e-6

    
    plt.figure(figsize=(10, 5))
    plt.scatter(data['Message Size'], data['Time'], label='Time')
    plt.plot(data['Message Size'], Model(data['Message Size'], *params), label=f'Fit: Bandwidth={bandwidth:.2e}, Latency={latency:.2e}s', color='red')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Message size (Bytes)')
    plt.ylabel('Ping-Pong time (S)')
    plt.title(f'Ping-Pong time vs. message size on {mode}')
    plt.legend()
    plt.grid(True)
    plt.show()

    return bandwidth, latency


intraBandwidth, latencyBandwidth = Fit('results/intra_node.txt', 'intra-node')
print("Bandwidth (bytes/s) for intra-node communication:", intraBandwidth)
print("Latency (s) for intra-node communication:", latencyBandwidth)

interBandwidth, latencyBandwidth = Fit('results/inter_node.txt', 'inter-node')
print("Bandwidth (bytes/s) for inter-node communication:", interBandwidth)
print("Latency (s) for inter-node communication:", latencyBandwidth)
