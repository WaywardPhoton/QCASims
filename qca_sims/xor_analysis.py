from qcadtrans import QCACircuit
from qca_leap_minimal import run_qca_minimal
import numpy as np

qcafile = 'XOR'
circuit = QCACircuit(fname=qcafile, verbose=True )
print(type(circuit))

print(circuit.nodes)

drivers = []
inputs = []
cells = []

for i in range(len(circuit.nodes)):
        node = circuit.nodes[i]
        # Here, node is a dict containing multiple key--value pairs.
        # You can use pdb to inspect what kind of information is available 
        # within each node.
        # print(f'x: {node["x"]}\ty: {node["y"]}\tpol: {node["pol"]}\trotated: {node["rot"]}\ttype: {node["cf"]}')
        if node["cf"] == 0:
                cells.append(np.array((node["x"], node["y"])))
        elif node["cf"] == 3:
                drivers.append(np.array((node["x"], node["y"], node["pol"])))
        elif node["cf"] == 1:
                inputs.append(np.array((node["x"], node["y"], node["pol"])))
        elif node["cf"] == 2:
                cells.append(np.array((node["x"], node["y"])))
                output_cell_index = len(cells)-1

# A = np.array((320, 300, node["pol"]))
# B = np.array((320, 280, node["pol"]))
# take parsable circuit and gnerate hamiltonian 

# print(np.array(inputs))
# print(np.array(drivers))
# print(np.array(cells))
# print(output_cell_index)
# print(len(cells))
inputs =  np.array(inputs)
drivers = np.array(drivers)
cells = np.array(cells)
Ek = 1

def calc_Ek_reduc(i, j):
        dist = (((i[0] - j[0])/20)**2 + ((i[1] - j[1])/20)**2)**(1/2)
        return dist**5

for a in [-1, 1]:
        for b in [-1, 1]:
                inputs[0][2] = a
                inputs[1][2] = b
                drivers = np.append(drivers, inputs, axis=0)

                h_array = []
                for i in range(0, cells.shape[0]):
                        input_e = 0 
                        for D in range(0, drivers.shape[0]):
                                reduc = calc_Ek_reduc(drivers[D], cells[i])
                                if reduc <= 2**5:
                                        EkiD = Ek/reduc
                                        pD = drivers[D,2]
                                        input_e = input_e + EkiD*pD
                        h_array.append(-input_e)
                h_array = np.array(h_array)

                J_matrix = np.zeros((cells.shape[0],cells.shape[0])) 
                for j in range(0, cells.shape[0]):
                        for i in range(0,cells.shape[0]):
                                reduc = calc_Ek_reduc(cells[j],cells[i])
                                if i < j and reduc <= 2**5:                
                                        Ekij = Ek/reduc
                                        J_matrix[j][i] = -Ekij
                J_matrix = np.array(J_matrix)
                # print(J_matrix)

                response = run_qca_minimal(E_k=1, qpu_arch='pegasus', use_classical=True, 
                                        num_reads=500, show_inspector=True, plot_emb_path=None, 
                                        h_array = h_array, J_array= J_matrix)

                print('inputs:', a, b)
                print('output:', response)
                print('output:', response[output_cell_index])

                drivers = drivers[:-2, :]

