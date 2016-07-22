'''
CODE CHALLENGE: Solve the HMM Parameter Estimation Problem.
     Input: A string x of symbols emitted from an HMM, followed by the HMM's alphabet ,
     followed by a path , followed by the collection of states of the HMM.
     Output: A transition matrix Transition followed by an emission matrix Emission that maximize
     Pr(x, ) over all possible transition and emission matrices.

Extra Dataset

Sample Input:
yzzzyxzxxx
--------
x y z
--------
BBABABABAB
--------
A B C
Sample Output:
	A	B	C
A	0.0	1.0	0.0
B	0.8	0.2	0.0
C	0.333	0.333	0.333
--------
	x	y	z
A	0.25	0.25	0.5
B	0.5	0.167	0.333
C	0.333	0.333	0.333


'''

import numpy as np

def hmm_profile(theta,alphabet,multalign,pseudocount = 0):

    a = np.array(map(list,multalign))
    (n,m) = a.shape
    # compute column id where insertion fraction is greater than theta
    col_is_m = np.apply_along_axis(lambda r:np.sum(r == '-')<n*theta,0,a)
    col_to_state = np.cumsum(col_is_m)
    # compute the symbols translation table
    symbols = {s: i for (i,s) in enumerate(alphabet)}        
    # compute the name_state translation table
    max_state_id = max(col_to_state)
    name_state = {}
    name_state['S'] = 0
    name_state['I0'] = 1
    for i in range(1,max(col_to_state)+1):
        name_state['M'+str(i)] = 3*i - 1
        name_state['D'+str(i)] = 3*i
        name_state['I'+str(i)] = 3*i + 1
    name_state['E'] = 3*max_state_id + 2
    state_name = [None] * len(name_state)
    for k,v in name_state.iteritems():
        state_name[v] = k
    
    # emission
    emission = np.zeros((len(name_state),len(symbols)))
    for i in range(n):
        for j in range(m):
            insert_flag = not col_is_m[j]
            state_id = col_to_state[j]
            e = a[i,j]
            if e in symbols:
                emission[name_state[('I' if insert_flag else 'M')+str(state_id)],symbols[e]] += 1       


    # transition
    transition = np.zeros((len(name_state),len(name_state)))
    for i in range(n):
        prev_state_name = 'S'
        for j in range(m):
            state_id = col_to_state[j]
            insert_flag = not (col_is_m[j])
            delete_flag = not (a[i,j] in symbols)
            if (insert_flag) and (delete_flag):
                if j == m-1:
                    transition[name_state[prev_state_name],name_state['E']] += 1
            else:
                if (not insert_flag) and (not delete_flag):
                    curr_state_name ='M' + str(state_id)
                elif insert_flag and (not delete_flag):
                    curr_state_name ='I' + str(state_id)
                elif (not insert_flag) and delete_flag:
                    curr_state_name ='D' + str(state_id)
                else:
                    print insert_flag,delete_flag
                    assert True == False #cannot happen anyway....
                transition[name_state[prev_state_name],name_state[curr_state_name]] += 1
                prev_state_name = curr_state_name
                # last column specific case
                if j == m-1:            
                    transition[name_state[prev_state_name],name_state['E']] += 1
 
    # normalize matrices probability
    for i in name_state.values():
        csum = emission[i,:].sum()
        if (csum > 0):
            emission[i,:] /= csum
    for i in name_state.values():
        csum = transition[i,:].sum()
        if (csum > 0):
            transition[i,:] /= csum
    
    # adding pseudocount if needed
    if pseudocount > 0:
        # emission :
        # add pseudocount only for 'I' and 'M' states
        m,n = emission.shape
        for i in range(1,m-1):
            if (i%3):
                emission[i,:] += pseudocount
        for i in name_state.values():
            csum = emission[i,:].sum()
            if (csum > 0):
                emission[i,:] /= csum
        # emission :
        # add transition only for allowed transition states
        m,n = transition.shape
        for i in range(0,m-1):
            a = min((i+1)/3*3+1,n)
            b = min((i+1)/3*3+4,n)
            transition[i,a:b] += pseudocount
        for i in name_state.values():
            csum = transition[i,:].sum()
            if (csum > 0):
                transition[i,:] /= csum
    
    return transition,emission,alphabet,state_name


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
def hmm_parameter_estimation(x,alphabet,path,states):
    """
    CODE CHALLENGE: Solve the HMM Parameter Estimation Problem.
    Input: A string x of symbols emitted from an HMM, followed by the HMM's alphabet ,
    followed by a path , followed by the collection of states of the HMM.
    Output: A transition matrix Transition followed by an emission matrix Emission that maximize
    Pr(x, ) over all possible transition and emission matrices.
    """
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



with open('18_ HMM_Parameter_Estimation.txt', "r") as f:
    text = f.read()
    lines = text.split('\n')
    x = lines[0]
    alphabet = lines[2].split(' ')
    path = lines[4]
    states = lines[6].split(' ')
(t,e) = hmm_parameter_estimation(x,alphabet,path,states)
ret = print_hmm_profile(t,e,alphabet,states)
with open('18_ HMM_Parameter_Estimation_Answer.txt', "w") as f:
    text = f.write(ret)