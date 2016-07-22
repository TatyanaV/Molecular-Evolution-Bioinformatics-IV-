'''
CODE CHALLENGE: Solve the Probability of a Hidden Path Problem.
     Given: A hidden path followed by the states States and transition matrix Transition of an HMM
     (, States, Transition, Emission).
     Return: The probability of this path, Pr().

Note: You may assume that transitions from the initial state occur with equal probability.

Extra Dataset

Sample Input:

ABABBBAAAA
--------
A B
--------
	A	B
A	0.377	0.623
B	0.26	0.74

Sample Output:

0.000384928691755

'''

import numpy as np


def hmm_path_prob(path,states,transition_matrix):
    """
    CODE CHALLENGE: Solve the Probability of a Hidden Path Problem.
    Given: A hidden path  followed by the states States and transition matrix Transition of an HMM
    (, States, Transition, Emission).
    Return: The probability of this path, Pr().
    """
    return 1./len(states) * np.exp(sum([np.log(transition_matrix[states[path[i]],states[path[i+1]]]) for i in range(len(path)-1)]))

def parse_path_states_transition_matrix(text):
    lines = text.split('\n')
    path = lines[0]
    states = {s: i for (i,s) in enumerate(lines[2].split(' '))}
    transition_matrix = np.zeros((len(states),len(states)))
    for i in range(len(states)):
        transition_matrix[i,:] = map(float,lines[i+5].split('\t')[1:len(states)+1])
    return path,states,transition_matrix

text = 'ABABBBAAAA\n--------\nA B\n--------\n	A	B\nA	0.377	0.623\nB	0.26	0.74\n'
print np.abs(hmm_path_prob(*parse_path_states_transition_matrix(text)))


with open('11_Hidden_Path_Problem.txt', "r") as f:
    print hmm_path_prob(*parse_path_states_transition_matrix(f.read()))