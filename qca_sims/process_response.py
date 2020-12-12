import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

def process_response(response, output_cell_index, expected_out):
    response = response.record
    # print(response.dtype)
    energy_levels = response['energy']
    bins = np.unique(energy_levels)
    counts = np.zeros(len(bins))
    for i in energy_levels:
        index = np.where(bins == i)
        counts[index[0]] = counts[index[0]] + 1 

    bins = [str(i) for i in bins]

    plt.bar(bins, counts, width=0.3)
    plt.show()

    # print(response.sample)

    for j in range(len(output_cell_index)):
        out = response.sample[:,output_cell_index[j]]
        # print(out)
        for i in range(len(out)):
            # print(np.where(out==expected_out[j]))
            perc = len(np.where(out==expected_out[j])[0])/len(out)
        print('percent of output', j, 'correct:', perc)