'''
CODE CHALLENGE: Solve the Limb Length Problem.
     Input: An integer n, followed by an integer j between 0 and n - 1, followed by a space-separated
     additive distance matrix D (whose elements are integers).
     Output: The limb length of the leaf in Tree(D) corresponding to row j of this distance
     matrix (use 0-based indexing).

Extra Dataset

Sample Input:
4
1
0	13	21	22
13	0	12	13
21	12	0	13
22	13	13	0
Sample Output:
2

https://github.com/boolker/coursera_tasks/blob/7d1f3fe6e79bd3eeb0e70973289a51bcbd3d81a2/bioinformatics/part2/bio06.py
'''
import sys, os
#input_file_name = os.getcwd() + "/bio02/data/04/input023.txt"
def get_limb_length(_distances,_limb_num):
    dim = len(_distances)
    limb_val = sys.maxint
    for i in xrange(dim):
        for k in xrange(dim):
            if i!=k and i!=_limb_num and k!=_limb_num:
                val = (_distances[i][_limb_num]+_distances[_limb_num][k]-_distances[i][k])/2.0
                if val < limb_val:
                    limb_val = val

    return limb_val
def task42():
    input_file_name = '2_Limb_Length.txt'
    with open (input_file_name, "r") as myfile:
        data=myfile.readlines()
    
    dim = int(data[0])
    limb_num = int(data[1])
    distances=[]
    for d in data[2:]:
        row_str = d.replace('\n','').replace('\t',' ')
        row_data = [int(i) for i in row_str.split(' ')]
        distances.append(row_data)
        
    print(distances)
    
    print(get_limb_length(distances,limb_num))
	
task42()	



