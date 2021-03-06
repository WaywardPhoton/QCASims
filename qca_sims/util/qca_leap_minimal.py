#!/usr/bin/env python3

'''
This sample code serves as a toy example for the use of D-Wave's Ocean SDK.
For more complete documentation, please visit:
https://docs.ocean.dwavesys.com/en/stable/getting_started.html
'''

def run_qca_minimal(E_k=1, qpu_arch='pegasus', use_classical=False, 
        num_reads=10, show_inspector=False, plot_emb_path=None, 
        h_array=[-1, 0], J_matrix=[[0, 1],[1, 0]]):
    '''
    Minimal 1 Driver 2 Cell QCA Problem (introduced in the Leap slide deck).

    Params:
        E_k : kink energy in eV.
        qpu_arch : QPU architecture to use. Either 'pegasus' (that is the newer
            architecture) or 'chimera' (the old one).
        use_classical : set to True to use D-Wave's classical Ising solver such 
            that you don't have to use up your D-Wave Leap minutes for testing.
        num_reads : count of samples to request from the D-Wave QPU or classical
            sampler. Don't use too high of a value on the QPU as that might 
            use up your Leap minutes very quickly.
        show_inspector : set to True to show problem inspector in the end.
        plot_emb_path : supply a string path to plot the embedding
    '''
    import matplotlib.pyplot as plt

    # general dwave dependencies
    import dwave
    import dwave.embedding
    import dwave.inspector
    from dwave.system import DWaveSampler, EmbeddingComposite
    from dwave.cloud import Client
    from dwave.cloud.exceptions import SolverNotFoundError
    import dimod
    from dimod.reference.samplers import ExactSolver
    from minorminer import find_embedding
    import neal

    # dependencies for plotting connectivity graph
    import networkx as nx
    import dwave_networkx as dnx

    # general math and Python dependencies
    import math
    import numpy as np
    import itertools

    # define self bias (h) and coupling strengths (J)
    h = - E_k * np.array(h_array)
    J = - E_k * np.array(J_matrix)
    N = len(h)

    # create edgelist (note that {} initializes Python dicts)
    linear = {}         # qubit self-bias
    quadratic = {}      # inter-qubit bias
    for i in range(N):
        linear[i] = h[i]
        for j in range(i+1, N):
            if J[i][j] != 0:
                quadratic[(i,j)] = J[i][j]

    # construct a bqm containing the provided self-biases (linear) and couplings
    # (quadratic). Specify the problem as SPIN (Ising).
    print('Constructing BQM...')
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, 0, dimod.SPIN)

    # get DWave sampler and target mapping edgelist
    print('Choosing solver...')
    client = Client.from_config()
    solver = None
    try:
        if qpu_arch == 'pegasus':
            solver = client.get_solver('Advantage_system1.1').id
        elif qpu_arch == 'chimera':
            solver = client.get_solver('DW_2000Q_6').id
        else:
            raise ValueError('Specified QPU architecture is not supported.')
    except SolverNotFoundError:
        print(f'The pre-programmed D-Wave solver name for architecture '
                '\'{qpu_arch}\' is not available. Find the latest available '
                'solvers by:\n'
                'from dwave.cloud import Client\nclient = Client.from_config()\n'
                'client.get_solvers()\nAnd update this script.')
        raise
    # get the specified QPU
    dwave_sampler = DWaveSampler(solver=solver)

    # run the problem
    sampler = None
    response = None
    if use_classical:
        print('Choosing classical sampler...')
        sampler = neal.SimulatedAnnealingSampler()
    else:
        print('Choosing D-Wave QPU as sampler...')
        sampler = EmbeddingComposite(dwave_sampler)
    response = sampler.sample(bqm, num_reads=num_reads)
    # print(response)
    print('Problem completed from selected sampler.')

    # plot the embedding if specified
    if not use_classical and plot_emb_path != None:
        print(f'Plotting embedding to {plot_emb_path}...')
        embedding = response.info['embedding_context']['embedding']
        plt.figure(figsize=(16,16))
        T_nodelist, T_edgelist, T_adjacency = dwave_sampler.structure
        if qpu_arch == 'pegasus':
            G = dnx.pegasus_graph(16,node_list=T_nodelist)
            dnx.draw_pegasus_embedding(G, embedding, node_size=8, cmap='rainbow')
        elif qpu_arch == 'chimera':
            G = dnx.chimera_graph(16,node_list=T_nodelist)
            dnx.draw_chimera_embedding(G, embedding, node_size=8, cmap='rainbow')
        plt.savefig(plot_emb_path)

    # take first result from response
    use_result = [*response.first.sample.values()]
    # NOTE that response.record contains all returned results and some 
    # statistics. You can inspect what's inside by using pdb or reading the 
    # dimod.SampleSet documentation.

    # show dwave web inspector if specified
    if show_inspector and not use_classical:
        print('\nOpening problem inspector on your browser.')
        dwave.inspector.show(response)
    return response
    # return use_result

if __name__ == '__main__':
    run_qca_minimal(show_inspector=True, plot_emb_path='embedding.pdf')
