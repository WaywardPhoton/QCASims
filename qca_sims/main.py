from qcadtrans import QCACircuit
from qca_leap_minimal import run_qca_minimal
import numpy as np

qcafile = 'XOR'
circuit = QCACircuit(fname=qcafile, verbose=True )
print(type(circuit))

print(circuit.nodes)

inputs = []
cells = []

for i in range(len(circuit.nodes)):
        node = circuit.nodes[i]
        # Here, node is a dict containing multiple key--value pairs.
        # You can use pdb to inspect what kind of information is available 
        # within each node.
        print(f'x: {node["x"]}\ty: {node["y"]}\tpol: {node["pol"]}\trotated: {node["rot"]}')
        if node["pol"] != 0:
                inputs.append(np.array((node["x"], node["y"], node["pol"])))
        else:
                cells.append(np.array((node["x"], node["y"])))

A = np.array((320, 300, node["pol"]))
B = np.array((320, 280, node["pol"]))
 # take parsable circuit and gnerate hamiltonian 
def calc_Ek_reduc(i, j):
    dist = ((i[0] - j[0])**2 + (i[1] - j[1])**2)**(1/2)
    return dist**5


# print(np.array(inputs))
# print(np.array(cells))
inputs = np.array(inputs)
cells = np.array(cells)
Ek = 1
    
input_e = 0 
h_array = []
for i in range(0, cells.shape[0]):
        for D in range(0, inputs.shape[0]):        
                EkiD = Ek/calc_Ek_reduc(inputs[D],cells[i])
                pD = inputs[D,2]
                input_e += EkiD*pD
        h_array.append(input_e)
h_array = np.array(h_array)

J_array = np.zeros((cells.shape[0],cells.shape[0])) 
for j in range(0, cells.shape[0]):
        for i in range(0,cells.shape[0]):
                if i < j:                
                        Ekij = Ek/calc_Ek_reduc(cells[j],cells[i])
                        J_array[i][j] = Ekij
J_array = np.array(J_array)
print(J_array)

run_qca_minimal(E_k=1, qpu_arch='pegasus', use_classical=False, 
        num_reads=10, show_inspector=True, plot_emb_path=None, 
        h_array = h_array, J_array= J_array)
       

