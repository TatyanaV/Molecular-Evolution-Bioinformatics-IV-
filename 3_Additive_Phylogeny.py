'''
CODE CHALLENGE: Implement AdditivePhylogeny to solve the Distance-Based Phylogeny Problem.
     Input: An integer n followed by a space-separated n x n distance matrix.
     Output: A weighted adjacency list for the simple tree fitting this matrix.

Note on formatting: The adjacency list must have consecutive integer node labels starting from 0. The n leaves must be labeled 0, 1, ..., n - 1 in order of their appearance in the distance matrix. Labels for internal nodes may be labeled in any order but must start from n and increase consecutively.

Extra Dataset

Sample Input:
4
0	13	21	22
13	0	12	13
21	12	0	13
22	13	13	0
Sample Output:
0->4:11
1->4:2
2->5:6
3->5:7
4->0:11
4->1:2
4->5:4
5->4:4
5->3:7
5->2:6

https://github.com/ilap/Bioinformatics_Part2/blob/8c4fcec1df79e45b80818a281683578876060a6b/CH2_Which_Animal_Gave_Us_SARS/4_4_AdditivePhylogeny.py
https://github.com/search?q=phylogeny+0%0913%0921%0922language%3APython&ref=searchresults&type=Code&utf8=%E2%9C%93
https://github.com/boolker/coursera_tasks/blob/7d1f3fe6e79bd3eeb0e70973289a51bcbd3d81a2/bioinformatics/part2/bio05.py
https://github.com/ngaude/sandbox/blob/f009d5a50260ce26a69cd7b354f6d37b48937ee5/bioinformatics-002/bioinformatics_chapter10.py
instuctions how to donload numpy
http://stackoverflow.com/questions/31967617/no-module-named-numpy-windows-7-python-3-4-3-numpy-1-9-2

'''
import numpy as np

def limb_length_linear(n, j, d):
    """
    CODE CHALLENGE: Solve the Limb Length Problem in linear time.
    Input: An integer n, followed by an integer j between 0 and n, followed by a space-separated
    additive distance matrix D (whose elements are integers).
    Output: The limb length of the leaf in Tree(D) corresponding to the j-th row of this distance
    matrix (use 0-based indexing).
    """
    assert n > 2
    assert d.shape == (n,n)
    i = (j+1) % n
    k = (j+2) %n
    minlen = (d[i,j] + d[j,k] - d[i,k])/2
    for k in range(n):
        if i==j or k==j:
            continue
        currlen = (d[i,j] + d[j,k] - d[i,k])/2
        minlen = min(minlen,currlen)
    return minlen
def additive_phylogeny(n,d):
    """
    CODE CHALLENGE: Implement AdditivePhylogeny to solve the Distance-Based Phylogeny Problem.
    Input: An integer n followed by a space-separated n x n distance matrix.
    Output: A weighted adjacency list for the simple tree fitting this matrix.
    """
    def find_path(i,j):
        visited = [None] * (max(adj.keys())+1)
        def dfs(path):
            for (v,w) in adj[path[-1][0]]:
                if visited[v] == True:
                    continue
                visited[v] = True
                pathlen = path[-1][1] + w
                npath = path[:]                
                npath.append((v,pathlen))
                if (v == j):
                    # found the node that ends path.
                    return npath
                result = dfs(npath)
                if result is not None:
                    return result
            return
        return dfs([(i,0)])
        
    def add_leaf(leaf,i,j,x,w):
        # add leaf on the path from i to j,
        # attached at x distance from i
        # with weigth w
        path = find_path(i,j)
        # check if an x distant parent node already exists in path p
        parent = None
        for k in range(len(path)-1):
            if path[k][1] == x:
                # parent node already exists
                parent = path[k][0]
                break
            if path[k][1] < x and x < path[k+1][1]:
                # cut the u->v:w0 edge into
                # u->parent:w1 , parent->v:w2
                u = path[k][0]
                v = path[k+1][0]
                w0 = path[k+1][1] - path[k][1]
                w1 = x - path[k][1]
                w2 = w0 - w1
                # find a new node slot
                parent = max(adj.keys()+[n-1])+1 

                adj[u].remove((v,w0))
                adj[v].remove((u,w0))
                adj[parent] = []
                
                adj[u].append((parent,w1))
                adj[parent].append((u,w1))

                adj[v].append((parent,w2))
                adj[parent].append((v,w2))                

                break
        assert parent is not None

        adj.setdefault(leaf,[]).append((parent,w))
        adj[parent].append((leaf,w))        
        return
    
    def find_condition(d,l):

        for i in range(l):
            for k in range(i+1,l):
                if d[i,k] == d[i,l]+d[l,k]:
                    return (i,k)
        assert 0
        return
    
    def recursive(nn):
        if nn==2:
            return
        limb = limb_length_linear(nn,nn-1,d[:nn,:nn])
        for j in range(nn-1):
            d[nn-1, j] -= limb
            d[j, nn-1] -= limb
        (i, k) = find_condition(d,nn-1)
        x = d[i,nn-1]
        recursive(nn-1)
        add_leaf(nn-1,i,k,x,limb)
        return
        
    adj = {0: [(1,d[0,1]),],1: [(0,d[1,0]),]}
    recursive(n)
    return adj
	
fname = '3_Additive_Phylogeny.txt'
with open(fname, "r") as f:
    lines = f.read().strip().split('\n')
    n = int(lines[0])
distances=[]
for d in lines[1:]:
    row_str = d.replace('\n','').replace('\t',' ')
    row_data = [int(i) for i in row_str.split(' ')]
    distances.append(row_data)
		
    #d = map(lambda r: map(int, r.split(' ')), lines[1:])
distances = np.array(distances )
print distances
T = additive_phylogeny(n,distances)
with open('3_Additive_Phylogeny_Answer.txt', "w") as f:
   for u,vw in T.iteritems():
       for (v,w) in vw:
           f.write(str(u)+'->'+str(v)+':'+str(w)+'\n')	
'''	
def task43():
    input_file_name = '3_Additive_Phylogeny.txt'
    with open (input_file_name, "r") as myfile:
        data=myfile.readlines()
    
    limb_num = int(data[0])
    #limb_num = int(data[1])
    distances=[]
    for d in data[1:]:
        row_str = d.replace('\n','').replace('\t',' ')
        row_data = [int(i) for i in row_str.split(' ')]
        distances.append(row_data)
        
    print(distances)
    
    print(additive_phylogeny(distances,limb_num))
	
task43()	
'''