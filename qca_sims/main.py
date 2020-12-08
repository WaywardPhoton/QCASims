from qcadtrans import QCACircuit

qcafile = 'XOR'
circuit = QCACircuit(fname=qcafile, verbose=True )
print(type(circuit))

print(circuit.nodes)

for i in range(len(circuit.nodes)):
        node = circuit.nodes[i]
        # Here, node is a dict containing multiple key--value pairs.
        # You can use pdb to inspect what kind of information is available 
        # within each node.
        print(f'x: {node["x"]}\ty: {node["y"]}\tpol: {node["pol"]}\trotated: {node["rot"]}')