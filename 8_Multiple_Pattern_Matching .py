'''
CODE CHALLENGE: Solve the Multiple Pattern Matching Problem.
     Input: A string Text followed by a collection of strings Patterns.
     Output: All starting positions in Text where a string from Patterns appears as a substring.

Sample Input:

AATCGGGTTCAATCGGGGT
ATCG
GGGT

https://github.com/ngaude/sandbox/tree/f009d5a50260ce26a69cd7b354f6d37b48937ee5/bioinformatics-002
Sample Output:

1 4 11 15

'''

def bwt(s):
    """
    Burrows-Wheeler Transform Construction Problem: 
    Construct the Burrows-Wheeler transform of a string.
    Input: A string Text.
    Output: BWT(Text).
    """
    return ''.join([s[(i-1) % len(s)] for i in suffix_array(s)])
	
	
def suffix_array(s):
    """
    Suffix Array Construction Problem: Construct the suffix array of a string.
    Input: A string Text.
    Output: SuffixArray(Text).
    """
    # elegant by uses too much memory 
    # return sorted(range(len(s)), key=lambda i: s[i:])
    
    # no memory issue, but still not time loglinear because of string copy
    # return sorted(range(len(s)), cmp=lambda i,j: cmp(s[i:],s[j:]))
    
    # no memory issue, no string copy issue, but python bytecode is still slow
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
    return sorted(range(len(s)), cmp=compare)	

def multiple_pattern_matching(text,patterns):
    """
    CODE CHALLENGE: Solve the Multiple Pattern Matching Problem.
    Input: A string Text followed by a collection of strings Patterns.
    Output: All starting positions in Text where a string from Patterns appears as a substring.
    """
    # to cope with not $-ending text
    if text[-1] != '$':
            text+='$'
    s = bwt(text)
    a = suffix_array(text)
    
    
    def scan_symbol_count(c):
        # update current dict
        current_dict[c] = current_dict.get(c,0)+1
        # copy current dict to the current symbol array
        return current_dict.copy()
    current_dict = {}
    count_symbol = [{}] + [scan_symbol_count(c) for c in s]
    
    # create first_occurence 
    def scan_first_occurence((i,c)):
        if c not in first_occurence:
            first_occurence[c] = i
    first_occurence = {}    
    map(scan_first_occurence,enumerate(sorted(s)))
    
    def pattern_positions(pattern):
        top = 0
        bottom = len(s) - 1
        while top <= bottom:
            if pattern:
                symbol = pattern[-1]
                pattern = pattern[:-1]
                if count_symbol[bottom+1].get(symbol,0) > count_symbol[top].get(symbol,0):   
                        top = first_occurence[symbol] + count_symbol[top].get(symbol,0)
                        bottom = first_occurence[symbol] + count_symbol[bottom+1].get(symbol,0) - 1
                else:
                    return []
            else:
                return [a[i] for i in range(top,bottom+1)]
        return []
    
    pos = []
    for pattern in patterns:
        pos += pattern_positions(pattern)
    pos.sort()
    return pos

print multiple_pattern_matching('AATCGGGTTCAATCGGGGT',('ATCG','GGGT'))



with open('8_Multiple_Pattern_Matching.txt', "r") as f:
    text = f.read().strip().split('\n')
    s = text[0]
    p = text[1:]
with open('8_Multiple_Pattern_Matching_Answer.txt', "w") as f:
    f.write(' '.join(map(str,multiple_pattern_matching(s,p))))