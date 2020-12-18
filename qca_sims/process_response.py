import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

def process_response(response, output_cell_index, expected_out, num_reads):
    response = response.record
    energy_levels = response['energy']
    num_occurrences = response['num_occurrences']
    sample = response['sample']
    
    ground = np.min(energy_levels)
    print('ground energy is ', ground)
    ground_indices = np.where(energy_levels == energy_levels.min())[0]
    ground_count = 0
    for index in ground_indices:
        ground_count += num_occurrences[index]

    aggr_count = {}   
    for i in range(len(energy_levels)):
        if aggr_count.get(energy_levels[i]) is not None:
            aggr_count[energy_levels[i]] =  aggr_count.get(energy_levels[i]) + num_occurrences[i]
        else:
            aggr_count[energy_levels[i]] =  num_occurrences[i]

    count_keys = list(aggr_count.keys())
    count_keys = np.sort(count_keys)
    bins = [str(round(key,3)) for key in count_keys]   
    plt.bar(bins, [i/num_reads for i in aggr_count.values()])
    plt.xticks(rotation=90)
    plt.xlabel("Energy levels")
    plt.ylabel("Proportion of occurences")
    plt. title("Number of occurences for each energy state")
    plt.show()

    for j in range(len(output_cell_index)):
        countg = 0
        count = 0
        for i in range(len(energy_levels)):        
            out = sample[i]

            if out[output_cell_index[j]] == expected_out[j]:
                count += num_occurrences[i]
                if energy_levels[i] == ground:
                    countg += num_occurrences[i]

        perc_max = countg/ground_count
        perc = count/num_reads
        

        print('percent of output', j, 'correct in ground state:', perc_max)
        print('percent of output', j, 'correct overall:', perc)
