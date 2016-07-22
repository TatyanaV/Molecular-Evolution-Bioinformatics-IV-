'''
CODE CHALLENGE: Construct a partial suffix array.
     Input: A string Text and a positive integer K.
     Output: SuffixArrayK(Text), in the form of a list of ordered pairs (i, SuffixArray(i)) for all
     nonempty entries in the partial suffix array.

Sample Input:

PANAMABANANAS$
5

Sample Output:

1,5
11,10
12,0
'''


def partial_suffix_array(s,k):
    """
    CODE CHALLENGE: Construct a partial suffix array.
    Input: A string Text and a positive integer K.
    Output: SuffixArrayK(Text), in the form of a list of ordered pairs (i, SuffixArray(i)) for all
    nonempty entries in the partial suffix array.
    """
    l = len(s)
    def compare(i,j):        
        while i<l and j<l:
            if s[i]>s[j]:
                return 1
            elif s[i]<s[j]:
                return -1
            i +=1
            j +=1
        return 0
    sa = sorted(range(len(s)), cmp=compare)
    psa = [(i,c) for (i,c) in enumerate(sa) if c % k == 0]
    return psa
    
print partial_suffix_array('panamabananas$',5)


with open('10_partial_suffix_array.txt', "r") as f:
    text = f.read().strip().split('\n')
    s = text[0]
    k = int(text[1])
with open('10_partial_suffix_array_Answer.txt', "w") as f:
    f.write('\n'.join(map(lambda (i,j): str(i)+','+str(j),partial_suffix_array(s,k))))