'''
CODE CHALLENGE: Implement BETTERBWMATCHING.
     Input: A string BWT(Text) followed by a collection of strings Patterns.
     Output: A list of integers, where the i-th integer corresponds to the number of substring
     matches of the i-th member of Patterns in Text.

Sample Input:

GGCGCCGC$TAGTCACACACGCCGTA
ACC CCG CAG

Sample Output:

1 2 1
'''

def better_bw_matching(s,patterns):
    """
    CODE CHALLENGE: Implement BETTERBWMATCHING.
    Input: A string BWT(Text) followed by a collection of strings Patterns.
    Output: A list of integers, where the i-th integer corresponds to the number of substring
    matches of the i-th member of Patterns in Text.
    """
    # create count_symbol array : len = |s| * #symbol 
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

    def print_symbol_count():
        symbols = sorted(set(s))
        last_col = ' ' + s
        first_col = ' ' + ''.join(sorted(s))

        header = 'f l ##:'+' '.join(symbols)        
        
        delimiter = ''.join(['-']*len(header))
        print delimiter
        print header
        print delimiter
        for i,d in enumerate(count_symbol):
            l = first_col[i] + ' ' + last_col[i] + ' ' + format(i,'02') + ':'
            l += ' '.join(map(lambda symbol:str(d.get(symbol,0)),symbols))
            print l
        print delimiter

#    print_symbol_count()
    
    def pattern_count(pattern):
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
                    return 0
            else:
                return bottom - top + 1
        return 0
    
    return [pattern_count(pattern) for pattern in patterns]
    
print better_bw_matching('GGCGCCGC$TAGTCACACACGCCGTA',['ACC', 'CCG', 'CAG'])
with open('7_BETTERBWMATCHING.txt', "r") as f:
    text = f.read().strip().split('\n')
    s = text[0]
    p = text[1].split(' ')
with open('7_BETTERBWMATCHING_Answer.txt', "w") as f:
    f.write(' '.join(map(str,better_bw_matching(s,p))))