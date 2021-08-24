# Code for CS 171, Winter, 2021
import GrammarRule
from GrammarRule import grammarPeriodic
import Tree

verbose = False
def printV(*args):
    if verbose:
        print(*args)

# A Python implementation of the AIMA CYK-Parse algorithm in Fig. 23.5 (p. 837).
def CYKParse(words, grammar):
    T = {}
    P = {}
    # Instead of explicitly initializing all P[X, i, k] to 0, store
    # only non-0 keys, and use this helper function to return 0 as needed.
    def getP(X, i, k):
        key = str(X) + '/' + str(i) + '/' + str(k)
        if key in P:
            return P[key]
        else:
            return 0
    # Insert lexical categories for each word
    foundName = False
    for i in range(len(words)): # 1 potassium
        if words[i].lower() in ['name','are', 'am','group','column','period','row','hi','hello']:
            foundName = True
        X, p = getGrammarLexicalRules(grammar, words[i],foundName) 
        P[X + '/' + str(i) + '/' + str(i)] = p 
        T[X + '/' + str(i) + '/' + str(i)] = Tree.Tree(X, None, None,lexiconItem=words[i])

        #handle C1F
        for M,N,Q in getGrammarSyntaxRules(grammar,C1F = True):
            if N == X:
                P[M + '/' + str(i) + '/' + str(i)] = Q * p
                T[M + '/' + str(i) + '/' + str(i)] = Tree.Tree(M,T[X + '/' + str(i) + '/' + str(i)], None)
                #handle sentence that is only NP or VP.
                for A,B,C in getGrammarSyntaxRules(grammar,C1F = True):  
                    if B == M:
                        P[A + '/' + str(i) + '/' + str(i)] = Q * p * C
                        T[A + '/' + str(i) + '/' + str(i)] = Tree.Tree(A,T[M + '/' + str(i) + '/' + str(i)], None)
    
    #printV('P:', P)
    #printV('T:', [str(t)+':'+str(T[t]) for t in T])
    
    # Construct X_i:j from Y_i:j + Z_j+i:k, shortest spans first
    for i, j, k in subspans(len(words)):
        #print(i,j,k)
        for X,Y,Z,p in getGrammarSyntaxRules(grammar):
            PYZ = getP(Y, i, j) * getP(Z, j+1, k) * p
            if PYZ > getP(X, i, k):
                P[X + '/' + str(i) + '/' + str(k)] = PYZ
                T[X + '/' + str(i) + '/' + str(k)] = Tree.Tree(X, T[Y+'/'+str(i)+'/'+str(j)], T[Z+'/'+str(j+1)+'/'+str(k)])
                
        #handle C1F
        for X,Y,p in getGrammarSyntaxRules(grammar,C1F = True):
                PY = getP(Y,i,k) * p
                if PY > getP(X,i,k):
                    P[X + '/' + str(i) + '/' + str(k)] = PY
                    T[X + '/' + str(i) + '/' + str(k)] = Tree.Tree(X,T[Y + '/' + str(i) + '/' + str(k)], None)
                
    printV('T:', [str(t)+':'+str(T[t]) for t in T])
    return T, P

# Python uses 0-based indexing, requiring some changes from the book's
# 1-based indexing: i starts at 0 instead of 1
def subspans(N):
    for length in range(2, N+1):
        for i in range(N+1 - length):
            k = i + length - 1
            for j in range(i, k):
                yield i, j, k

# These two getXXX functions use yield instead of return so that a single pair can be sent back,
# and since that pair is a tuple, Python permits a friendly 'X, p' syntax
# in the calling routine.
def getGrammarLexicalRules(grammar, word,foundName):
    for rule in grammar['lexicon']:
        if rule[1] == word.lower():
            return rule[0], rule[2]
    
    if foundName:
        grammar['lexicon'].append(['Name',word.lower(), 0.01])
        return 'Name', 0.01
    elif word.isnumeric():
        grammar['lexicon'].append(['Number',word.lower(), 0.01])
        return 'Number', 0.01
    else:
        grammar['lexicon'].append(['Unknown',word.lower(), 0.01])
        return 'Unknown', 0.01
    
def getGrammarSyntaxRules(grammar,C1F = False):
    if C1F:
        for rule in grammar['syntax'][1]:
            yield rule[0], rule[1], rule[2]
    else:
        for rule in grammar['syntax'][0]:
            yield rule[0], rule[1], rule[2], rule[3]
            
# Unit testing code
if __name__ == '__main__':
    verbose = True
    #CYKParse(['How','many', 'elements', 'are', 'on','the','periodic', 'table'], grammarPeriodic)
    #CYKParse(['Hi','Loc','my', 'name', 'is', 'Peter'], grammarPeriodic)
    #CYKParse(['Hi'], grammarPeriodic)
    #CYKParse(['potassium'], grammarPeriodic)
    #CYKParse(['what', 'is', 'the', 'Potassium'], grammarPeriodic)
    
#comparison questions, yes/no questions, and properties of elements (mental or nonmetal, gas or solid at room temperature)


# R: Think about how the chatbot will respond to sentences it can’t parse/understand. DONE
#X: Recommend your chatbot should handle a wider variety of input questions and sentences, and ways it can respond. // randomize greeting and goodbye
# S: How will you handle nouns/names that aren’t in the lexicon? Done
# T: How will your parse function handle multiword names?

# Y: I don’t see that yourchatbot remembersany information from one sentence to the next(for example, so that it knows what “it” refers to). Consider adding that.