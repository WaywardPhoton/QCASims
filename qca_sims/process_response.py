import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

def process_response(response, output_cell_index, expected_out, num_reads):
    response = response.record
    # print(response)
    # print(response.dtype)
    energy_levels = response['energy']
    num_occurrences = response['num_occurrences']
    sample = response['sample']
    
    ground = np.min(energy_levels)
    print('ground energy is ', ground)
    ground_indices = np.where(energy_levels == energy_levels.min())[0]
    # print(ground_indices)
    ground_count = 0
    for index in ground_indices:
        ground_count += num_occurrences[index]

    # print(ground_count)

    # print(energy_levels)
    aggr_count = {}
        
    # for bin in bins:
    #     aggr_count[bin] = 0
    
    for i in range(len(energy_levels)):
        if aggr_count.get(energy_levels[i]) is not None:
            aggr_count[energy_levels[i]] =  aggr_count.get(energy_levels[i]) + num_occurrences[i]
        else:
            aggr_count[energy_levels[i]] =  num_occurrences[i]

    # print(aggr_count)

    # print(len(num_occurrences))
    # ground = np.min(energy_levels)
    # bins = np.unique(energy_levels)
    # print(len(bins))
    # counts = np.zeros(len(bins))
    # for i in energy_levels:
    #     index = np.where(bins == i)
    #     counts[index[0]] = counts[index[0]] + 1 
    # print(aggr_count.keys())
    # print(aggr_count.values())
    count_keys = list(aggr_count.keys())
    # print(count_keys)
    count_keys = np.sort(count_keys)
    bins = [str(round(key,3)) for key in count_keys]   
    # print(bins) 
    plt.bar(bins, aggr_count.values())
    plt.xticks(rotation=90)
    plt.xlabel("Energy levels")
    plt.ylabel("Number of occurences out of "+ str(num_reads))
    plt. title("Number of occurences for each energy state")
    plt.show()

    max_freq_energy_index = np.argmax(num_occurrences, axis=0)
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



    # print(response.sample)

    # for j in range(len(output_cell_index)):
    #     out = response.sample[:,output_cell_index[j]]
    #     # print(out)
    #     for i in range(len(out)):
    #         # print(np.where(out==expected_out[j]))
    #         perc = len(np.where(out==expected_out[j])[0])/len(out)
    #     
