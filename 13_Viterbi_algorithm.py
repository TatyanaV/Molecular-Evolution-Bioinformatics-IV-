'''
CODE CHALLENGE: Implement the CODE CHALLENGE: Implement the Viterbi algorithm solving the Decoding Problem.
     Input: A string x, followed by the alphabet from which x was constructed,
     followed by the states States, transition matrix Transition, and emission matrix
     Emission of an HMM (, States, Transition, Emission).
     Output: A path that maximizes the (unconditional) probability Pr(x,) over all possible paths .
Note: You may assume that transitions from the initial state occur with equal probability.

Extra Dataset

Sample Input:

xyxzzxyxyy
--------
x y z
--------
A B
--------
	A	B
A	0.641	0.359
B	0.729	0.271
--------
	x	y	z
A	0.117	0.691	0.192	
B	0.097	0.42	0.483

Sample Output:

AAABBAAAAAsolving the Decoding Problem.
     Input: A string x, followed by the alphabet from which x was constructed,
     followed by the states States, transition matrix Transition, and emission matrix
     Emission of an HMM (, States, Transition, Emission).
     Output: A path that maximizes the (unconditional) probability Pr(x, ) over all possible paths .
Note: You may assume that transitions from the initial state occur with equal probability.

Extra Dataset

Sample Input:

xyxzzxyxyy
--------
x y z
--------
A B
--------
	A	B
A	0.641	0.359
B	0.729	0.271
--------
	x	y	z
A	0.117	0.691	0.192	
B	0.097	0.42	0.483

Sample Output:

AAABBAAAAA
'''
import numpy as np

def hmm_decoding(emission,symbols,states,transition_matrix,emission_matrix):
    """
    CODE CHALLENGE: Implement the Viterbi algorithm solving the Decoding Problem.
    Input: A string x, followed by the alphabet from which x was constructed,
    followed by the states States, transition matrix Transition, and emission matrix
    Emission of an HMM (, States, Transition, Emission).
    Output: A path that maximizes the (unconditional) probability Pr(x, ) over all possible paths .
    """
    assert transition_matrix.shape == (len(states),len(states))
    assert emission_matrix.shape == (len(states),len(symbols))
    rstates = {v: k for (k,v) in states.iteritems()}
    def __log_weight(l,k,i):
        si = symbols[emission[i]]
        return np.log(emission_matrix[k,si]*transition_matrix[l,k])
    score = np.empty(shape = (len(states),len(emission)), dtype = float)
    backt = np.zeros(shape = (len(states),len(emission)), dtype = int)
    
    score[:,0] = np.log(1./len(states)*emission_matrix[:,symbols[emission[0]]])
    for i in range(1,len(emission)):
        for k in range(len(states)):
            pscore = np.array(map(lambda l:score[l,i-1]+__log_weight(l,k,i), range(len(states))))
            score[k,i] = pscore.max()
            backt[k,i] = pscore.argmax()
    # backtracking max score from backt pointers
    rpath = []
    state = score[:,len(emission)-1].argmax()
    rpath.append(rstates[state])
    for i in range(1,len(emission))[::-1]:
        state  = backt[state,i]
        rpath.append(rstates[state])       
    return ''.join(rpath[::-1])


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


text = 'xyxzzxyxyy\n--------\nx y z\n--------\nA B\n--------\n	A	B\nA	0.641	0.359\nB	0.729	0.271\n--------\n	x	y	z\nA	0.117	0.691	0.192	\nB	0.097	0.42	0.483\n'
path = 'AAABBAAAAA'
assert  hmm_decoding(*parse_emission_symbols_states_transition_matrix_emission_matrix(text)) == path


text = 'zxxxxyzzxyxyxyzxzzxzzzyzzxxxzxxyyyzxyxzyxyxyzyyyyzzyyyyzzxzxzyzzzzyxzxxxyxxxxyyzyyzyyyxzzzzyzxyzzyyy\n--------\nx y z\n--------\nA B\n--------\n	A	B\nA	0.634	0.366	\nB	0.387	0.613	\n--------\n	x	y	z\nA	0.532	0.226	0.241\nB	0.457	0.192	0.351\n'
path = 'AAAAAAAAAAAAAABBBBBBBBBBBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBBBBBBBBBAAAAAAAAAAAAAAAAAAAAABBBBBBBBBBAAA'
assert hmm_decoding(*parse_emission_symbols_states_transition_matrix_emission_matrix(text)) == path


with open('13_Viterbi_algorithm.txt', "r") as f:
    variable = hmm_decoding(*parse_emission_symbols_states_transition_matrix_emission_matrix(f.read()))
	
	
with open('13_Viterbi_algorithm_Answer.txt', "w") as f:
    f.write(variable)



