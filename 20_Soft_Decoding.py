'''
CODE CHALLENGE: Solve the Soft Decoding Problem.
     Input: A string x, followed by the alphabet  from which x was constructed,
     followed by the states States, transition matrix Transition, and emission matrix
     Emission of an HMM (, States, Transition, Emission).
     Output: An |x| x |States| matrix whose (i, k)-th element holds the conditional probability Pr(i = k|x).

Extra Dataset

Sample Input:
zyxxxxyxzz
--------
x y z
--------
A B
--------
	A	B
A	0.911	0.089
B	0.228	0.772
--------
	x	y	z
A	0.356	0.191	0.453 
B	0.040	0.467	0.493
Sample Output:
A	B 
0.5438	0.4562 
0.6492	0.3508 
0.9647	0.0353 
0.9936	0.0064 
0.9957	0.0043 
0.9891	0.0109 
0.9154	0.0846 
0.964	0.036 
0.8737	0.1263 
0.8167	0.1833
https://github.com/johnmerm/bioinfo/blob/e6a255a461ca83c58e56c83d4717bc13f8880c5d/src/main/java/bioinfo/hiv/softDecoding.py
https://github.com/johnmerm/bioinfo/blob/e6a255a461ca83c58e56c83d4717bc13f8880c5d/src/main/java/bioinfo/hiv/markov.py
'''
def viterbi(x,transitions,emissions,alphabet=['x','y','z'],symbols=['A','B'],func=sum):
    trail = []
    
    scores = {s:{e:ev/len(symbols) for (e,ev) in emissions.items() if e[0]==s and e[1]==x[0]} for s in symbols}
    scores = {s:func(v.values()) for (s,v) in scores.items()}
    trail.append(scores)
    
    for i in range (1,len(x)):
        em = x[i]
        new_scores = {s:{t[0]:(scores[t[0]],tv,ev) for (t,tv) in transitions.items() for (e,ev) in emissions.items() 
                         if e[1] == em and t[1]==s and e[0] == s
                         } for s in symbols }
        
        new_scores = {s:{tk:prod(tv) for (tk,tv) in v.items()}  for (s,v) in new_scores.items()}
        
        new_scores = {s:func(v.values()) for (s,v) in new_scores.items()}
        scores = new_scores
        trail.append(scores)
    
        
    return func(new_scores.values()),trail
	
def prod(itera):
    return reduce(lambda x,y:x*y,itera,1)

	
def forward(x,transitions,emissions,alphabet=['x','y','z'],symbols=['A','B']):
    return viterbi(x, transitions, emissions, alphabet, symbols, sum)


def softDecoding(x,alphabet,symbols,trans,ems):
    sink,forward = viterbi(x, trans, ems, alphabet, symbols)
        
    bw ={s:1. for s in symbols}
    bws = [bw]
    for i in range(len(x)):
        _bw = {k:sum({l:bw[l]*trans[(k,l)]*ems[(l,x[-i-1])] for l in symbols}.values()) for k in symbols}
        bw = _bw
        bws = [bw]+bws
    
    bwsp = bws[1:]
    
    return [{s:bwsp[i][s]*forward[i][s]/sink for s in symbols} for i in range(len(x))]


def softDecoding_crack(x,alphabet,symbols,trans,ems,crack):
    cks = [{symbols[i]:c[i] for i in range(len(symbols)) }for c in crack]
    sink,forward = viterbi(x, trans, ems, alphabet, symbols)
    
    backward = [{s:cks[i][s]*sink/forward[i][s] for s in symbols} for i in range(len(x))]

    
    bw ={s:1. for s in symbols}
    bws = [bw]
    for i in range(len(x)):
        _bw = {k:sum({l:bw[l]*trans[(k,l)]*ems[(l,x[-i-1])] for l in symbols}.values()) for k in symbols}
        bw = _bw
        bws = [bw]+bws
    
    bwsp = bws[1:]
    for i in range(len(x)):
        print backward[i],bwsp[i]
def parseLines(lines):
    x = lines[0].strip()
    alphabet = lines[2].strip().split()
    symbols = lines[4].strip().split()
    trans_mat = [ [float(l) for l in li.strip().split()[1:]] for li in lines[7:7+len(symbols)] ]
    ems_mat = [[float(l) for l in li.strip().split()[1:]] for li in lines[9+len(symbols):9+len(symbols)+len(symbols)]]
    
    trans = {(symbols[i],symbols[j]):trans_mat[i][j] for j in range(len(symbols)) for i in range(len(symbols))}
    ems = {(symbols[i],alphabet[j]):ems_mat[i][j] for j in range(len(alphabet)) for i in range(len(symbols))}
    
    return x,alphabet,symbols,trans,ems
def test_softDecoding():
    lines = [
            "zyxxxxyxzz",
            "--------",
            "x y z",
            "--------",
            "A B",
            "--------",
            "A    B",
            "A    0.911    0.089",
            "B    0.228    0.772",
            "--------",
            "x    y    z",
            "A    0.356    0.191    0.453 ",
            "B    0.040    0.467    0.493",
            ]
    x, alphabet, symbols, trans, ems = parseLines(lines)
    
    
    crack = [   [0.5438,    0.4562],
                [0.6492  ,  0.3508 ],
                [0.9647  ,  0.0353 ],
                [0.9936  ,  0.0064 ],
                [0.9957  , 0.0043 ],
                [0.9891  ,  0.0109 ],
                [0.9154  ,  0.0846 ],
                [0.964   , 0.036 ],
                [0.8737  ,  0.1263 ],
                [0.8167  ,  0.1833]]
    #softDecoding_crack(x, alphabet, symbols, trans, ems,crack)
    
    sf =  softDecoding(x, alphabet, symbols, trans, ems)
    print '\t'.join(symbols)
    for s in sf:
        print '\t'.join([str(s[b]) for b in symbols ])
    
    print crack
def exam_softDecoding():
    lines = list(open('20_Soft_Decoding.txt'))
    x, alphabet, symbols, trans, ems = parseLines(lines)
    sf =  softDecoding(x, alphabet, symbols, trans, ems)
    print '\t'.join(symbols)
    for s in sf:
        print '\t'.join([str(s[b]) for b in symbols ])

if __name__ == '__main__':
    print exam_softDecoding()
	
with open('20_Soft_Decoding_Answer.txt', "w") as f:
    text = f.write(exam_softDecoding())	