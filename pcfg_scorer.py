"""
Probabilistic Context-Free Grammar Scorer
"""


def read_counts(counts_file):
    """
    Read frequency counts from a file
    """
    fi = open(counts_file, 'r')
    for line in fi:
        fields = line.strip().split(' ')
        yield fields


class PCFGScorer:
    
    def __init__(self):
        self.nonterminal_counts = dict()
        self.unary_rule_counts = dict()
        self.binary_rule_counts = dict()


    def train(self, counts_file):
        """
        Read counts from a counts file, then store counts for each type:
        nonterminal, binary rule and unary rule.
        """
        #Probably need to change this to address other countfile formats.
        
        for l in read_counts(counts_file):
            n, count_type, args = int(l[0]), l[1], l[2:]
            if count_type == 'NONTERMINAL':
                self.nonterminal_counts[args[0]] = n
            elif count_type == 'BINARYRULE':
                self.binary_rule_counts[tuple(args)] = n
            else: # UNARYRULE counts
                self.unary_rule_counts[tuple(args)] = n


    def q_unary(self, x, y):
        return self.unary_rule_counts[x, y] / self.nonterminal_counts[x]

    def q_binary(self, x, y, z):
        return self.binary_rule_counts[x, y, z] / self.nonterminal_counts[x]

    def tokenize(self, sentence):
        #Note:  This default tokenizer doesn't deal with punctuation
        """
        Should return list.
        """
        return sentence.split()
    
    def score(self, sentence):
        print("Tokenizing...")
        tokens = self.tokenize(sentence)
        print("Applying inside algorithm to tokens")
        return self.inside(tokens)

    def inside(self, tokens):

        N = len(tokens)
        print("Number of tokens is ", N)
        nonterminals = set(self.nonterminal_counts.keys())
        unary_rules = set(self.unary_rule_counts.keys())
        binary_rules = set(self.binary_rule_counts.keys())
        
        pi = dict()
        
        #Initialization
        print("Initializing atomic pi values...")
        for i in range(N):
            for X in nonterminals:
                if (X, tokens[i]) in unary_rules:
                    
                    pi[(i, i, X)] = self.q_unary(X, tokens[i])
                
                else:
                    pi[(i, i, X)] = 0
        #        print("pi(",i,",",i,",",X,") is ", pi[(i, i, X)])
        #Recursive Step

        for l in range(N-1):
            for i in range(N-l):
                j = i + l
                for X in nonterminals:
                    sum = 0
                    for (X, Y, Z) in binary_rules:
                        for s in range(i, j):
                            sum += self.q_binary(X, Y, Z) * pi[i, s, Y] * pi[s+1, j, Z]
                pi[(i, j, X)] = sum
        return pi[0,N-1,'S']

        

    
