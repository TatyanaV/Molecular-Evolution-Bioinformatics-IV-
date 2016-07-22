'''
CODE CHALLENGE: Solve the Outcome Likelihood Problem.
     Input: A string x, followed by the alphabet from which x was constructed,
     followed by the states States, transition matrix Transition, and emission matrix
     Emission of an HMM (, States, Transition, Emission).
     Output: The probability Pr(x) that the HMM emits x.
Note: You may assume that transitions from the initial state occur with equal probability.
https://github.com/ngaude/sandbox/blob/f009d5a50260ce26a69cd7b354f6d37b48937ee5/bioinformatics-002/bioinformatics_chapter15.py
Extra Dataset

Sample Input:

xzyyzzyzyy
--------
x y z
--------
A B
--------
	A	B
A	0.303	0.697 
B	0.831	0.169 
--------
	x	y	z
A	0.533	0.065	0.402 
B	0.342	0.334	0.324

Sample Output:

1.1005510319694847e-06

'''
import numpy as np


def parse_emission_symbols_states_transition_matrix_emission_matrix(text):
    lines = text.split('\n')
    emission = lines[0]
    symbols = {s: i for (i,s) in enumerate(lines[2].split(' '))}
    states = {s: i for (i,s) in enumerate(lines[4].split(' '))}
    transition_matrix = np.zeros((len(states),len(states)), dtype = np.longfloat)
    for i in range(len(states)):
        transition_matrix[i,:] = map(np.longfloat,lines[i+7].split('\t')[1:len(states)+1])
    emission_matrix = np.zeros((len(states),len(symbols)), dtype = np.longfloat)
    for i in range(len(states)):
        emission_matrix[i,:] = map(np.longfloat,lines[i+9+len(states)].split('\t')[1:len(symbols)+1])
    return emission,symbols,states,transition_matrix,emission_matrix
	
def hmm_emission_likelihood_prob(emission,symbols,states,transition_matrix,emission_matrix):
    """
    CODE CHALLENGE: Solve the Outcome Likelihood Problem.
    Input: A string x, followed by the alphabet from which x was constructed,
    followed by the states States, transition matrix Transition, and emission matrix
    Emission of an HMM (, States, Transition, Emission).
    Output: The probability Pr(x) that the HMM emits x.
    """
    assert transition_matrix.shape == (len(states),len(states))
    assert emission_matrix.shape == (len(states),len(symbols))
    forward = np.empty(shape = (len(states),len(emission)), dtype = np.longfloat)
    
    forward[:,0] = 1./len(states)*emission_matrix[:,symbols[emission[0]]]
    for i in range(1,len(emission)):
        for k in range(len(states)):
            si = symbols[emission[i]]
            pforward = np.array(map(lambda l:forward[l,i-1]*transition_matrix[l,k], range(len(states))))
            forward[k,i] = pforward.sum()*emission_matrix[k,si]
#    print forward
    return forward[:,-1].sum()
    

np.set_printoptions(precision =32)
   
text = 'xzyyzzyzyy\n--------\nx y z\n--------\nA B\n--------\n	A	B\nA	0.303	0.697 \nB	0.831	0.169\n--------\n	x	y	z\nA	0.533	0.065	0.402\nB	0.342	0.334	0.324\n'
#print np.abs(hmm_emission_likelihood_prob(*parse_emission_symbols_states_transition_matrix_emission_matrix(text)))
#
#s = hmm_emission_likelihood_prob(*parse_emission_symbols_states_transition_matrix_emission_matrix(text))
#print("challenge : %.10e" % s)

#text = 'zxxxzyyxyzyxyyxzzxzyyxzzxyxxzyzzyzyzzyxxyzxxzyxxzxxyzzzzzzzxyzyxzzyxzzyzxyyyyyxzzzyzxxyyyzxyyxyzyyxz\n--------\nx y z\n--------\nA B\n--------\n	A	B\nA	0.994	0.006	\nB	0.563	0.437	\n--------\n	x	y	z\nA	0.55	0.276	0.173	\nB	0.311	0.368	0.321\n'
#print np.abs(hmm_emission_likelihood_prob(*parse_emission_symbols_states_transition_matrix_emission_matrix(text))-3.3318672795e-55) < 0.000000000000001



with open('14_Outcome_Likelihood.txt', "r") as f:
    text = f.read()
    s = hmm_emission_likelihood_prob(*parse_emission_symbols_states_transition_matrix_emission_matrix(text))
print(">> %.10e" % s)
