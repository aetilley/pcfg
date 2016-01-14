"""Probabilistic Context-Free Grammar parser/scorer."""


def read_counts(counts_file):
    """Read frequency counts from a file."""
    fi = open(counts_file, 'r')
    for line in fi:
        fields = line.strip().split(' ')
        yield fields


class PCFG:
    """The PCFG Grammar object."""    
    def __init__(self):
        self.nonterminal_counts = dict()
        self.unary_rule_counts = dict()
        self.binary_rule_counts = dict()
        self.nonterminals = set()
        self.unary_rules = set()
        self.binary_rules = set()
        self.terminals = set()


    def train(self, counts_file, c_file_style = 0):
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

        self.nonterminals = set(self.nonterminal_counts.keys())
        self.unary_rules = set(self.unary_rule_counts.keys())
        self.binary_rules = set(self.binary_rule_counts.keys())
        self.terminals = set(unary_rule[1] for unary_rule in self.unary_rules)

    def check_tokens(self, tokens):
        """
        Checks whether each token is in the learned
        vocabulary (terminals) of the PCFG.
        """
        
        good = True
        for token in tokens:
            if token not in self.terminals:
                good = False
                print("The token ", token, " is not a known terminal.")
        return good
        
    def q_unary(self, x, y):
        return self.unary_rule_counts[x, y] / self.nonterminal_counts[x]

    def q_binary(self, x, y, z):
        return self.binary_rule_counts[x, y, z] / self.nonterminal_counts[x]

    def tokenize(self, sentence):

        """The lexer/tokenizer."""
        return sentence.split()
    
    def score(self, sentence):
        """Score a sentence with respect to the trained grammar."""
        tokens = self.tokenize(sentence)
        self.check_tokens(tokens)
        print("Applying Inside algorithm...")
        return self.inside(tokens)

    def inside(self, tokens):

        N = len(tokens)
        pi = dict()
        
        #Initialization
        for i in range(N):
            terminal = tokens[i]
            for X in self.nonterminals:
                if (X, terminal) in self.unary_rules:
                    
                    pi[(i, i, X)] = self.q_unary(X, terminal)
                
                else:
                    pi[(i, i, X)] = 0
        #Recursive Step

        for l in range(N-1):
            for i in range(N-l-1):
                j = i + l + 1
                for X_0 in self.nonterminals:
                    sum = 0
                    for s in range(i, j):
                        for (X, Y, Z) in self.binary_rules:
                            if X == X_0:
                                sum += self.q_binary(X, Y, Z) \*
                                pi[i, s, Y] * pi[s+1, j, Z]
                    pi[(i, j, X_0)] = sum
        
        result = pi[0,N-1,'S']
        print("Final Score:  ", result)
        return result


    def parse(self, sentence):
        """
        Returns a python dictionary giving the tree structure of the most likely parse.
        """
        tokens = self.tokenize(sentence)
        self.check_tokens(tokens)
        print("Applying CKY algorithm...")
        return self.CKY(tokens)

    def CKY(self, tokens):
        """
        Applies CYK algorithm to list tokens of tokens.  Returns parse tree as a dict.
        """
        N = len(tokens)
        pi = dict()
        bp = dict()
        
        #Initialization
        for i in range(N):
            terminal = tokens[i]
            for X in self.nonterminals:
                if (X, terminal) in self.unary_rules:
                    pi[(i, i, X)] = self.q_unary(X, terminal)
                else:
                    pi[(i, i, X)] = 0

        #Recursive Step
        for l in range(N-1):
            for i in range(N-l-1):
                j = i + l + 1
                for X_0 in self.nonterminals:
                    max_score = 0
                    best_rule = None
                    best_cut = 0
                    for s in range(i, j):
                        for (X, Y, Z) in self.binary_rules:
                            if X == X_0:
                                current_score = self.q_binary(X, Y, Z) * \
                                pi[i, s, Y] * pi[s+1, j, Z]
                                if current_score > max_score:
                                    max_score = current_score
                                    best_rule = (X, Y, Z)
                                    best_cut = s
                    pi[(i, j, X_0)] = max_score
                    bp[(i, j, X_0)] = (best_rule, best_cut)
        
        return self.recover_tree(bp, tokens, 0, N-1, 'S')

    def recover_tree(self, bp, tokens, i, j, X):
        """Recover a parse tree from a dictionary of back-pointers."""
        tree = dict()
        tree['tag'] = X
        if i == j:
            tree['terminal'] = tokens[i]
        else:
            rule, cut = bp[i, j, X]
            tree['left_branch'] = self.recover_tree(bp, tokens, i, cut, rule[1])
            tree['right_branch'] = self.recover_tree(bp, tokens, cut+1, j, rule[2])
        return tree
