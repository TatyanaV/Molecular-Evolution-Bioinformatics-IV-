'''
CODE CHALLENGE: Solve the Multiple Approximate Pattern Matching Problem.
     Input: A string Text, followed by a collection of strings Patterns, and an integer d.
     Output: All positions where one of the strings in Patterns appears as a substring of Text with
     at most d mismatches.

Sample Input:

ACATGCTACTTT
ATT GCC GCTA TATT
1

Sample Output:

2 4 4 6 7 8 9

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
	
def multiple_approximate_pattern_matching(text,patterns,d):
    """
    CODE CHALLENGE: Solve the Multiple Approximate Pattern Matching Problem.
    Input: A string Text, followed by a collection of strings Patterns, and an integer d.
    Output: All positions where one of the strings in Patterns appears as a substring of Text with
    at most d mismatches.
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
    
    # move from patterns to seeds
    def pattern_to_seeds(p):
        l = len(p)
        assert l>d
        minsize = l/(d+1)
        cut = range(0,l-minsize+1,minsize)
        cut.append(l)
        seeds = [(p[cut[i-1]:cut[i]],cut[i-1]) for i in range(1,len(cut))]
        return seeds
    
    def seed_positions(seed):
        top = 0
        bottom = len(s) - 1
        while top <= bottom:
            if seed:
                symbol = seed[-1]
                seed = seed[:-1]
                if count_symbol[bottom+1].get(symbol,0) > count_symbol[top].get(symbol,0):   
                        top = first_occurence[symbol] + count_symbol[top].get(symbol,0)
                        bottom = first_occurence[symbol] + count_symbol[bottom+1].get(symbol,0) - 1
                else:
                    return []
            else:
                return [a[i] for i in range(top,bottom+1)]
        return []

    def is_approximately_matching(offset,p):
        mismatches = 0
        for i,c in enumerate(p):
            if (c!=text[offset+i]):
                mismatches += 1
                if mismatches > d:
                    return False
        return True
        
    
    def approximate_pattern_positions(p):
        pattern_positions = set()
        so = pattern_to_seeds(p)
        for (seed,offset) in so:
            candidate_positions = seed_positions(seed)
            for candidate_position in candidate_positions:
                pattern_position = candidate_position - offset
                if pattern_position < 0:
                    # candidate matching before text starts ....
                    continue
                if pattern_position + len(p) > len(text):
                    # candidate matching after text stops ....
                    continue
                if is_approximately_matching(pattern_position,p):
                    # candidate matching with at most d mismatches
                    pattern_positions.add(pattern_position)
        return list(pattern_positions)
       
    pos = []
    for pattern in patterns:
        pos += approximate_pattern_positions(pattern)
    pos.sort()
    return pos             
    
print multiple_approximate_pattern_matching('ACATGCTACTTT',['ATT', 'GCC', 'GCTA', 'TATT'],1)


with open('9_Multiple_Approximate_Pattern_Matching.txt', "r") as f:
    text = f.read().strip().split('\n')
    s = text[0]
    p = text[1].split(' ')
    d = int(text[2])
    print s,p,d
with open('9_Multiple_Approximate_Pattern_Matching_Answer.txt', "w") as f:
    f.write(' '.join(map(str,multiple_approximate_pattern_matching(s,p,d))))	
	
print("quiz")	

print suffix_array('cocoon$')	

print bwt('TCAGGGCTTG$')

def ibwt(s):
    """
    Inverse Burrows-Wheeler Transform Problem: 
    Reconstruct a string from its Burrows-Wheeler transform.
    Input: A string Transform (with a single "$" symbol).
    Output: The string Text such that BWT(Text) = Transform.
    """
    l = len(s)
    
    def char_rank(i):
        d[s[i]] = d.get(s[i],0) + 1
        return d[s[i]]
    d = {}
    # produce a list tuple (char,rank) for the last column
    last_char_rank = [(s[i],char_rank(i),i) for i in range(l)]
    d = {}
    # produce the list tuple (char,rank) for the first column
    first_char_rank = sorted(last_char_rank)
        
#    for i in range(l):
#        r = str(first_char_rank[i])+('*'*(l-2))+str(last_char_rank[i])
#        print r
    
    i = 0
    decoded = ''
    for j in range(l):
        i = first_char_rank[i][2]
        decoded += first_char_rank[i][0]
    return decoded

print ibwt('TTACA$AAGTC')
	