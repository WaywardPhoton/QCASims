import numpy as np

from util import run_qca_minimal

def run_qca(drivers, inputs, cells, output_cell_index, input_vals, classical, num_reads):
        inputs =  np.array(inputs)
        drivers = np.array(drivers)
        cells = np.array(cells)
        output_cell_index = np.array(output_cell_index)
        Ek = 1

        def calc_Ek_reduc(i, j):
                dist = (((i[0] - j[0])/20)**2 + ((i[1] - j[1])/20)**2)**(1/2)
                return dist**5

        inputs[:,2] = input_vals
        if (len(drivers) == 0):
                drivers = inputs
        else:
                drivers = np.append(drivers, inputs, axis=0)

        h_array = []
        for i in range(cells.shape[0]):
                input_e = 0 
                for D in range(drivers.shape[0]):
                        reduc = calc_Ek_reduc(drivers[D], cells[i])
                        if reduc <= 2**5 and cells[i,2] == drivers[D,3]:
                                EkiD = -Ek/reduc
                                pD = drivers[D,2]
                                input_e = input_e + EkiD*pD
                h_array.append(input_e)
        h_array = np.array(h_array)

        J_matrix = np.zeros((cells.shape[0],cells.shape[0])) 
        for j in range(0, cells.shape[0]):
                for i in range(0,cells.shape[0]):
                        reduc = calc_Ek_reduc(cells[j],cells[i])
                        if i < j and reduc <= 2**5 and cells[i,2] == cells[j,2]:                
                                Ekij = -Ek/reduc
                                J_matrix[j][i] = Ekij
        J_matrix = np.array(J_matrix)

        response = run_qca_minimal(E_k=Ek, qpu_arch='pegasus', use_classical=classical, 
                                num_reads=num_reads, show_inspector=False, plot_emb_path=None, 
                                h_array = h_array, J_matrix = J_matrix)

        return response