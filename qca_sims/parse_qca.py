import numpy as np

from util import QCACircuit

def parse_qca(qcafile):
    circuit = QCACircuit(fname=qcafile, verbose=True )
    print(type(circuit))

    print(circuit.nodes)

    drivers = []
    inputs = []
    cells = []
    output_cell_index = []

    for i in range(len(circuit.nodes)):
            node = circuit.nodes[i]
            if node["cf"] == 0:
                    cells.append(np.array((node["x"], node["y"], node["rot"])))
            elif node["cf"] == 3:
                    drivers.append(np.array((node["x"], node["y"], node["pol"], node["rot"])))
            elif node["cf"] == 1:
                    inputs.append(np.array((node["x"], node["y"], node["pol"], node["rot"])))
            elif node["cf"] == 2:
                    cells.append(np.array((node["x"], node["y"], node["rot"])))
                    output_cell_index.append(len(cells)-1)

    return drivers, inputs, cells, output_cell_index