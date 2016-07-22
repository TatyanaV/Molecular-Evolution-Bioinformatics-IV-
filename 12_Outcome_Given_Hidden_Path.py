'''
CODE CHALLENGE: Solve the Probability of an Outcome Given a Hidden Path Problem.
     Input: A string x, followed by the alphabet from which x was constructed, followed by
     a hidden path , followed by the states States and emission matrix Emission of an HMM
     (, States, Transition, Emission).
     Output: The conditional probability Pr(x) that x will be emitted given that the HMM
     follows the hidden path .
Note: You may assume that transitions from the initial state occur with equal probability.

Extra Dataset

Sample Input:

zzzyxyyzzx
--------
x y z
--------
BAAAAAAAAA
--------
A B
--------
	x	y	z
A	0.176	0.596	0.228
B	0.225	0.572	0.203

Sample Output:

3.59748954746e-06


'''
import numpy as np
def hmm_emission_prob(emission,symbols,path,states,emission_matrix):
    """
    CODE CHALLENGE: Solve the Probability of an Outcome Given a Hidden Path Problem.
    Input: A string x, followed by the alphabet from which x was constructed, followed by
    a hidden path , followed by the states States and emission matrix Emission of an HMM
    (, States, Transition, Emission).
    Output: The conditional probability Pr(x) that x will be emitted given that the HMM
    follows the hidden path .
    """
    assert len(emission) == len(path)
    return np.exp(sum([np.log(emission_matrix[states[path[i]],symbols[emission[i]]]) for i in range(len(path))]))

def parse_emission_symbols_path_states_emission_matrix(text):
    lines = text.split('\n')
    emission = lines[0]
    symbols = {s: i for (i,s) in enumerate(lines[2].split(' '))}
    path = lines[4]
    states = {s: i for (i,s) in enumerate(lines[6].split(' '))}
    emission_matrix = np.zeros((len(states),len(symbols)))
    for i in range(len(states)):
        emission_matrix[i,:] = map(float,lines[i+9].split('\t')[1:len(symbols)+1])
    return emission,symbols,path,states,emission_matrix

text = 'zzzyxyyzzx\n--------\nx y z\n--------\nBAAAAAAAAA\n--------\nA B\n--------\n	x	y	z\nA	0.176	0.596	0.228\nB	0.225	0.572	0.203\n'
print np.abs(hmm_emission_prob(*parse_emission_symbols_path_states_emission_matrix(text)))

text = 'zyyyxzxzyyzxyxxyyzyzzxyxyxxxxzxzxzxxzyzzzzyyxzxxxy\n--------\nx y z\n--------\nBAABBAABAABAAABAABBABBAAABBBABBAAAABAAAABBAAABABAA\n--------\nA B\n--------\n	x	y	z\nA	0.093	0.581	0.325	\nB	0.77	0.21	0.02\n'
assert np.abs(hmm_emission_prob(*parse_emission_symbols_path_states_emission_matrix(text)) - 3.42316482177e-35) < 0.000000000000001 


with open('12_Outcome_Given_Hidden_Path.txt', "r") as f:
    print hmm_emission_prob(*parse_emission_symbols_path_states_emission_matrix(f.read()))