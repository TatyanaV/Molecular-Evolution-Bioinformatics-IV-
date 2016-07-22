"""
CODE CHALLENGE: Implement UPGMA.
     Input: An integer n followed by a space separated n x n distance matrix.
     Output: An adjacency list for the ultrametric tree returned by UPGMA. Edge weights
     should be accurate to two decimal places (answers in the sample dataset below are provided to three decimal places).

Note on formatting: The adjacency list must have consecutive integer node labels starting from 0. The n leaves must be labeled 0, 1, ..., n - 1 in order of their appearance in the distance matrix. Labels for internal nodes may be labeled in any order but must start from n and increase consecutively.

Sample Input:

4
0	20	17	11
20	0	20	13
17	20	0	10
11	13	10	0

Sample Output:

0->5:7.000
1->6:8.833
2->4:5.000
3->4:5.000
4->2:5.000
4->3:5.000
4->5:2.000
5->0:7.000
5->4:2.000
5->6:1.833
6->5:1.833
6->1:8.833
https://github.com/ngaude/sandbox/blob/f009d5a50260ce26a69cd7b354f6d37b48937ee5/bioinformatics-002/bioinformatics_chapter11.py
https://github.com/ahmdeen/Bioinformatic-Algorthims/tree/7cae61bb45535911f220da290f9ecf609b964058
"""

import numpy as np



def upgma(n,D):
    """
    CODE CHALLENGE: Implement UPGMA.
    Input: An integer n followed by a space separated n x n distance matrix.
    Output: An adjacency list for the ultrametric tree returned by UPGMA. Edge weights
    should be accurate to three decimal places.
    """

    def clusters_distance():
        n = len(clusters)
        dc = np.zeros( (n,n), dtype = float )
        for c1 in range(n):
            for c2 in range(c1+1,n):
                dc1c2 = 0.
                for i in clusters[c1]:
                    for j in clusters[c2]:
                        dc1c2 += D[i,j]
                dc1c2 = dc1c2 / (1.*len(clusters[c1])*len(clusters[c2]))
                dc[c1,c2] = dc1c2
                dc[c2,c1] = dc1c2
        return dc    
    
    def find_closest_clusters():
        (n,m) = dclusters.shape
        assert n == m
        assert n > 1
        dmin = dclusters[0,1] 
        pmin = (0,1)                
        for i in range(n):            
            for j in range(i+1,n):
                if dclusters[i,j] < dmin:
                    dmin = dclusters[i,j]
                    pmin = (i,j)
        return pmin

    def merge_clusters_brute_force(c1,c2):
        c = clusters[c1]+clusters[c2]
        clusters.pop(c1)
        clusters.pop(c2-1)
        clusters.append(c)
        nid = max(clusterid)+1
        clusterid.pop(c1)        
        clusterid.pop(c2-1)
        clusterid.append(nid)
        return clusters_distance()

    # init vars    
    dclusters = D
    T = {}
    clusters = []
    clusterid = []
    age = {}    
    for i in range(n):
        clusters.append([i])
        clusterid.append(i) 
        T[i] = []
        age[i] = 0
    
    # iterate
    while len(clusters)>1:
        # find two closest clusters C1 and C2 (break ties arbitrarily)
        (c1,c2) = find_closest_clusters()
        cid1 = clusterid[c1]
        cid2 = clusterid[c2]        
        dc1c2 = dclusters[c1,c2]
        # merge C1 and C2 into a new cluster C
        dclusters = merge_clusters_brute_force(c1,c2)
        cid = clusterid[-1]
        # add a new node C to T and connect it to nodes C1 and C2 by directed edges
        T[cid] = [cid1,cid2]
        T[cid1].append(cid)
        T[cid2].append(cid)        

        age[cid] = dc1c2/2.
#        print '--------------------------------'
#        print 'clusters',clusters
#        print 'clusterid',clusterid
#        print 'dclusters',dclusters
#        print 'clusters_distance',clusters_distance(clusters,D)
#        print 'age',age
#        print '--------------------------'        
    adj = {}
    for u,vs in T.iteritems():
        for v in vs:        
            w = abs(age[u] - age[v])
            adj.setdefault(u,[]).append((v,w))
    return adj
 
D = np.array([[0,20,17,11],[20,0,20,13],[17,20,0,10],[11,13,10,0]])
print D
T = upgma(4,D)
res = {0: [(5, 7.0)], 1: [(6, 8.8333333333333339)], 2: [(4, 5.0)], 3: [(4, 5.0)], 4: [(2, 5.0), (3, 5.0), (5, 2.0)], 5: [(0, 7.0), (4, 2.0), (6, 1.8333333333333339)], 6: [(1, 8.8333333333333339), (5, 1.8333333333333339)]}
assert T == res
print (T)


fname = '5_UPGM.txt'
with open(fname, "r") as f:
    lines = f.read().strip().split('\n')
    n = int(lines[0])
distances=[]
for d in lines[1:]:
    d.rstrip()
    row_str = d.replace('\n','').replace('\t',' ')
    row_data = [int(i) for i in row_str.split(' ')]
    distances.append(row_data)
		
    #d = map(lambda r: map(int, r.split(' ')), lines[1:])
distances = np.array(distances )
print distances
T = upgma(n,distances)
with open('5_UPGMA_Answer.txt', "w") as f:
   for u,vw in T.iteritems():
       for (v,w) in vw:
           f.write(str(u)+'->'+str(v)+':'+"{0:.3f}".format(w)+'\n')
