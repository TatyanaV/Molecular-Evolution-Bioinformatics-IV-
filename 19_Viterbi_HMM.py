'''

CODE CHALLENGE: Implement Viterbi learning for estimating the parameters of an HMM.
     Input: A number of iterations j, followed by a string x of symbols emitted by an HMM,
     followed by the HMM's alphabet , followed by the HMM's states, followed by initial transition
     and emission matrices for the HMM.
     Output: Emission and transition matrices resulting from applying Viterbi learning for j iterations.

Extra Dataset

Sample Input:
100
--------
zyzxzxxxzz
--------
x y z
--------
A B
--------
	A	B
A	0.599	0.401	
B	0.294	0.706	
--------
	x	y	z
A	0.424	0.367	0.209	
B	0.262	0.449	0.289
Sample Output:
	A	B
A	0.5	0.5	
B	0.0	1.0	
--------
	x	y	z
A	0.333	0.333	0.333	
B	0.4	0.1	0.5

'''
import numpy as np
def print_hmm_profile(transition,emission,alphabet,state_name):
    __emission = np.round(emission,3)
    __transition = np.round(transition,3)
    ret = ''
    #ret += '\t' + '\t'.join(state_name) + '\n'
    ret += '\t' + '\t'.join(state_name) + '\n'
    for i,s in enumerate(state_name) :
         l = s + '\t'
         l += '\t'.join([format("%.3g" % __transition[i,j]) if __transition[i,j] != 1 else '1.0' for j in range(len(state_name))])
         ret += l+ '\n'
    ret += '--------\n'
    ret += '\t' + '\t'.join(alphabet)
    for i,s in enumerate(state_name) :
         l = '\n'+ s + '\t'
         l += '\t'.join([format("%.3g" % __emission[i,j]) if __emission[i,j] != 1 else '1.0' for j in range(len(alphabet))])
         ret += l
    return ret
	
	
def parse_emission_symbols_states_transition_matrix_emission_matrix(lines):
    emission = lines[0]
    symbols = lines[2].split(' ')
    states = lines[4].split(' ')
    transition_matrix = np.zeros((len(states),len(states)), dtype = np.longfloat)
    for i in range(len(states)):
        transition_matrix[i,:] = map(np.longfloat,lines[i+7].split('\t')[1:len(states)+1])
    emission_matrix = np.zeros((len(states),len(symbols)), dtype = np.longfloat)
    for i in range(len(states)):
        emission_matrix[i,:] = map(np.longfloat,lines[i+9+len(states)].split('\t')[1:len(symbols)+1])
    return emission,symbols,states,transition_matrix,emission_matrix
	
	
def hmm_parameter_estimation(x,alphabet,path,states):

    assert len(x)==len(path)
    m = len(alphabet)
    n = len(states)
    p = len(path)
    transition = np.zeros((n,n))
    emission = np.zeros((n,m))
    rsymbols = {k: i for (i,k) in enumerate(alphabet)}
    rstates = {k: i for (i,k) in enumerate(states)}
        
    for i in range(p):
        sy_id = rsymbols[x[i]]
        st_id = rstates[path[i]]
        emission[st_id,sy_id] += 1.
    
    for i in range(1,p):
        curr_st_id = rstates[path[i]]
        prev_st_id = rstates[path[i-1]]
        transition[prev_st_id,curr_st_id] += 1

    def matrix_norm(mtx):
        a,b = mtx.shape
        for i in range(a):
            csum = mtx[i,:].sum()
            if csum == 0:
                mtx[i,:] = 1./b
            else:
                mtx[i,:] /=  1.*csum
        return

    matrix_norm(transition)
    matrix_norm(emission)

    return transition,emission

    
np.set_printoptions(precision=10)
x = 'yzzzyxzxxx'
alphabet = ['x','y','z']
path = 'BBABABABAB'
states = ['A','B','C']
(t,e) = hmm_parameter_estimation(x,alphabet,path,states)
t = np.round(t,3)
e = np.round(e,3)
ret = print_hmm_profile(t,e,alphabet,states)

	
def hmm_decoding(emission,symbols,states,transition_matrix,emission_matrix):

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

def parse_emission_symbols_states_transition_matrix_emission_matrix(lines):
    emission = lines[0]
    symbols = lines[2].split(' ')
    states = lines[4].split(' ')
    transition_matrix = np.zeros((len(states),len(states)), dtype = np.longfloat)
    for i in range(len(states)):
        transition_matrix[i,:] = map(np.longfloat,lines[i+7].split('\t')[1:len(states)+1])
    emission_matrix = np.zeros((len(states),len(symbols)), dtype = np.longfloat)
    for i in range(len(states)):
        emission_matrix[i,:] = map(np.longfloat,lines[i+9+len(states)].split('\t')[1:len(symbols)+1])
    return emission,symbols,states,transition_matrix,emission_matrix
	
def hmm_viterbi_learning(it,x,symbols,states,transition,emission):
    dsymbols = {s: i for (i,s) in enumerate(symbols)}
    dstates = {s: i for (i,s) in enumerate(states)}
    for j in range(it):
        path = hmm_decoding(x,dsymbols,dstates,transition,emission)
        (transition,emission) = hmm_parameter_estimation(x,symbols,path,states)
        print print_hmm_profile(transition,emission,symbols,states)
        print '**************************************'
    print 
    return transition,emission



with open('19_Viterbi_HMM.txt', "r") as f:
    text = f.read()
    lines = text.split('\n')
    it = int(lines[0])
    x,symbols,states,t,e = parse_emission_symbols_states_transition_matrix_emission_matrix(lines[2:])
    t,e = hmm_viterbi_learning(it,x,symbols,states,t,e)
    ret = print_hmm_profile(t,e,symbols,states)
with open('19_Viterbi_HMM_Answer.txt', "w") as f:
    text = f.write(ret)