import numpy as np
import os
import matplotlib.pyplot as plt


def main():
    """
    generation list should be containing how many generations when converged
    active_node_length_list about how long each active nodes contain
    fitness_score is about rms_error
    """
    generation_list = []
    active_node_length_list = []
    fitness_score = []
    for universe_seed in range(10, 70):
        fn = 'outputs/seedlist%i.npy' % (universe_seed)
        seedlist = np.load(fn)
        generation = seedlist.item().get("generation")
        generation_list.append(generation)
        fn = 'outputs/seed%i/seed%i_gen%i.npy' % (universe_seed, universe_seed, generation)
        generation_analysis = np.load(fn)
        sample_best = generation_analysis.item().get("sample_best")
        active_nodes = sample_best.skeleton[1]["block_object"].active_nodes
        active_node_length_list.append(len(active_nodes))
        fitness_score.append(sample_best.fitness.values[0])
    """
    some sample
    generation  163 score: (0.07334205656756161, 0.47864814828582836)
    [-2, -1, 0, 1, 2, 3, 4, 5, 6, 8, 9, 11, 15, 18, 20]
    number of active nodes 15
    <function sub_fa2a at 0x1a20420ae8>    [-1, 0]    []
    <function add_fa2a at 0x1a20420950>    [1, -1]    []
    <function add_ff2f at 0x1118e2268>    [-1, -1]    []
    <function sub_fa2a at 0x1a20420ae8>    [-1, -2]    []
    <function mul_aa2a at 0x1a20420d08>    [4, 4]    []
    <function mul_fa2a at 0x1a20420c80>    [3, 5]    []
    <function mul_aa2a at 0x1a20420d08>    [6, 6]    []
    <function add_ff2f at 0x1118e2268>    [8, -1]    []
    <function mul_aa2a at 0x1a20420d08>    [9, 2]    []
    <function mul_aa2a at 0x1a20420d08>    [11, 4]    []
    <function add_fa2a at 0x1a20420950>    [15, -1]    []

    generation  17 score: (0.08224362068125281, 0.47864787023901256)
    [-2, -1, 0, 1, 2, 3, 4, 5, 7, 8, 11, 12, 18, 20]
    number of active nodes 14
    <function sub_fa2a at 0x1a20420ae8>    [-1, -2]    []
    <function mul_aa2a at 0x1a20420d08>    [0, 1]    []
    <function add_ff2f at 0x1118e2268>    [-1, 2]    []
    <function mul_fa2a at 0x1a20420c80>    [3, 2]    []
    <function add_aa2a at 0x1a204209d8>    [2, 0]    []
    <function mul_aa2a at 0x1a20420d08>    [5, 4]    []
    <function mul_fa2a at 0x1a20420c80>    [3, 7]    []
    <function add_aa2a at 0x1a204209d8>    [8, -2]    []
    <function add_fa2a at 0x1a20420950>    [5, 11]    []
    <function add_aa2a at 0x1a204209d8>    [0, 12]    []
    """

    plt.subplot(3, 1, 1)
    plt.plot(range(10, 70), fitness_score, linestyle='--', marker='o', color = 'black')
    plt.legend(['rms_error'])
    plt.subplot(3, 1, 2)
    plt.plot(range(10, 70), generation_list, linestyle='--', marker='o')
    plt.legend(['generation'])
    plt.gca().invert_yaxis()
    plt.subplot(3, 1, 3)
    plt.plot(range(10, 70), active_node_length_list, linestyle='--', marker='o', color = 'r')
    plt.legend(['active_nodes length'])
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
