'''
CODE CHALLENGE: Solve the Profile HMM with Pseudocounts Problem.
     Input: A threshold and a pseudocount , followed by an alphabet , followed by a
     multiple alignment Alignment whose strings are formed from .
     Output: The transition and emission matrices of HMM(Alignment, , ).

Note: Your matrices can be either space-separated or tab-separated.

Extra Dataset

Sample Input:
0.358 0.01
--------
A B C D E
--------
A-A
ADA
ACA
A-C
-EA
D-A
Sample Output:
	S	I0	M1	D1	I1	M2	D2	I2	E
S	0	0.01	0.819	0.172	0	0	0	0	0
I0	0	0.333	0.333	0.333	0	0	0	0	0
M1	0	0	0	0	0.398	0.592	0.01	0	0
D1	0	0	0	0	0.981	0.01	0.01	0	0
I1	0	0	0	0	0.01	0.981	0.01	0	0
M2	0	0	0	0	0	0	0	0.01	0.99
D2	0	0	0	0	0	0	0	0.5	0.5
I2	0	0	0	0	0	0	0	0.5	0.5
E	0	0	0	0	0	0	0	0	0
--------
	A	B	C	D	E
S	0	0	0	0	0
I0	0.2	0.2	0.2	0.2	0.2
M1	0.771	0.01	0.01	0.2	0.01
D1	0	0	0	0	0
I1	0.01	0.01	0.327	0.327	0.327
M2	0.803	0.01	0.168	0.01	0.01
D2	0	0	0	0	0
I2	0.2	0.2	0.2	0.2	0.2
E	0	0	0	0	0


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


with open('16_HMM_Pseudocounts.txt', "r") as f:
    text = f.read()
    lines = text.split('\n')
    theta = float(lines[0].split(' ')[0])
    pseudocount = float(lines[0].split(' ')[1])
    alphabet = lines[2].split(' ')
    multalign = [l for l in lines[4:] if len(l)==len(lines[4])]
(t,e,a,s) = hmm_profile(theta,alphabet,multalign,pseudocount = pseudocount)
sol = print_hmm_profile(t,e,a,s)
with open('16_HMM_Pseudocounts_Answer.txt', "w") as f:
    text = f.write(sol)