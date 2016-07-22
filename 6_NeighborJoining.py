'''
CODE CHALLENGE: Implement NeighborJoining.
     Input: An integer n, followed by an n x n distance matrix.
     Output: An adjacency list for the tree resulting from applying the neighbor-joining algorithm. Edge-weights should be accurate to two decimal places (they are provided to three decimal places in the sample output below).

Note on formatting: The adjacency list must have consecutive integer node labels starting from 0. The n leaves must be labeled 0, 1, ..., n - 1 in order of their appearance in the distance matrix. Labels for internal nodes may be labeled in any order but must start from n and increase consecutively.

Sample Input:

4
0	23	27	20
23	0	30	28
27	30	0	30
20	28	30	0

Sample Output:

0->4:8.000
1->5:13.500
2->5:16.500
3->4:12.000
4->5:2.000
4->0:8.000
4->3:12.000
5->1:13.500
5->2:16.500
5->4:2.000

https://github.com/ngaude/sandbox/blob/f009d5a50260ce26a69cd7b354f6d37b48937ee5/bioinformatics-002/bioinformatics_chapter11.py
'''
import numpy as np
def neighbor_joining_matrix(D):
    n = len(D)
    tD = D.sum(axis=1)      
    tD.shape = (n,1)
    o = np.ones(n)
    o.shape = (1,n)
    tD = np.dot(tD,o)
    njD = (n-2.)*D - tD - tD.transpose()
    for i in range(n):
        njD[i,i] = 0
    return njD

def neighbor_joining(n,D):
    """
    CODE CHALLENGE: Implement NeighborJoining.
    Input: An integer n, followed by an n x n distance matrix.
    Output: An adjacency list for the tree resulting from applying 
    the neighbor-joining algorithm.
    """
    def total_distance():
        return D.sum(axis=1)
    
    def neighbor_joining_distance():
        n = len(D)
        tD = total_distance()        
        tD.shape = (n,1)
        o = np.ones(n)
        o.shape = (1,n)
        tD = np.dot(tD,o)
        njD = (n-2.)*D - tD - tD.transpose()
        for i in range(n):
            njD[i,i] = 0
        return njD

    def find_pair():
        n = len(D)
        assert n>2
        njD = neighbor_joining_distance()
        dmin = njD[0,1] 
        pmin = (0,1)                
        for i in range(n):            
            for j in range(i+1,n):
                if njD[i,j] < dmin:
                    dmin = njD[i,j]
                    pmin = (i,j)
        return pmin

    def delta_distance():
        n = len(D)
        tD = total_distance()        
        tD.shape = (n,1)
        o = np.ones(n)
        o.shape = (1,n)
        tD = np.dot(tD,o)
        return (tD-tD.transpose())/float(n-2)
    
    def limb_length(i,j):
        dD = delta_distance()
        lli = 0.5*(D[i,j]+dD[i,j])
        llj = 0.5*(D[i,j]-dD[i,j])
        return (lli,llj)

    def reduce_distance(c1,c2):
        n = len(D)
        r = range(n)
        # add a new row/column m to D 
        # so that Dk,m = Dm,k = (1/2)(Dk,i + Dk,j - Di,j) for any k
        aD = np.zeros( (n+1,n+1), dtype = float )
        for ii,i in enumerate(r):
            for jj,j in enumerate(r):
                aD[ii,jj] = D[i,j]
        # do not compute m row/colmun for c1 row/column as well as c2 
        r.remove(c1)
        r.remove(c2)
        for k in r:
            aDk = 0.5*(D[k,c1]+D[k,c2]-D[c1,c2])
            aD[k,n] = aDk
            aD[n,k] = aDk
        # remove c1 row/column as well as c2 row/column from D/aD
        rD = np.zeros( (n-1,n-1), dtype = float )
        # copy also the m row/column from aD
        r.append(n)
        for ii,i in enumerate(r):
            for jj,j in enumerate(r):
                rD[ii,jj] = aD[i,j]
        return rD
    T = {}
    nodeid = range(n) 
    while len(D)>2:
        (i,j) = find_pair()
        (ii,jj) = (nodeid[i],nodeid[j])
        (wi,wj) = limb_length(i,j)
        # insert a k node linked to i and j
        kk =  max(nodeid)+1
        T.setdefault(kk,[]).append((ii,wi))
        T.setdefault(ii,[]).append((kk,wi))
        T.setdefault(kk,[]).append((jj,wj))
        T.setdefault(jj,[]).append((kk,wj))

        # update the node id reference
        nodeid.append(kk)
        nodeid.remove(ii)
        nodeid.remove(jj)
#        print '------'
#        print 'D',D
#        print 'njD',neighbor_joining_distance()
#        print 'tD',total_distance()
#        print '(i,j)',(ii,jj),'(w,w)',wi,wj
#        print 'nodeid',nodeid
#        print tree_tostring(T)
#        print '------'
    
        # reduce the distance matrix
        D = reduce_distance(i,j)

        
    # insert the last edge from the D 2x2 matrix
    T.setdefault(nodeid[0],[]).append((nodeid[1],D[0,1]))
    T.setdefault(nodeid[1],[]).append((nodeid[0],D[1,0]))
    
    return T

def tree_tostring(T):
    s = ''
    for u,vw in T.iteritems():
        for (v,w) in vw:
            s += str(u)+'->'+str(v)+':'+"{0:.3f}".format(w)+'\n'
    return s



with open('6_NeighborJoining.txt', "r") as f:
    lines = f.read().strip().split('\n')
    n = int(lines[0])
    d = np.zeros(shape=(n,n),dtype = float)    
    for i,l in enumerate(lines[1:]):
        l = l.replace('\t',' ')
        valstr = l.split(' ')
        if valstr[-1]=='':
            valstr = valstr[:-1]
        for j,v in enumerate(map(int,valstr)):
            d[i,j] = v
T = neighbor_joining(n,d)
with open('6_NeighborJoining_Answer.txt', "w") as f:
    f.write(tree_tostring(T))