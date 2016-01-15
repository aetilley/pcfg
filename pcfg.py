
START_SYMBOL_CODE = "S"

"""Probabilistic Context-Free Grammar parser/scorer."""


def read_lines(training_file_path):
    """Read lines from a file a return an iterator of lists"""
    fi = open(training_file_path, 'r')
    for line in fi:
        fields = line.strip().split(' ')
        yield fields

class Symbol:
    
    # Could change this class to account for lexing (eg. "10" -> <decnumeral>
    
    def __init__(self, code = "",  from_string = "", terminal = False):
        
        
        self.terminal = terminal
        
        self.symbol_code = code #Eg. "NUMERAL"
        if from_string:
            self.symbol_code = string #Just for now
        
    def is_terminal(self):
        return self._terminal

    def to_str(self):
        return self.symbol_code
    
    def __eq__(self, other):
        return self.symbol_code == other.symbol_code


    def __hash__(self):
        return hash(str(self.symbol_code))

class Rule:
    """Any transformation (rewrite) rule for any CFG"""

    def __init__(self, source, targets):
        #Source and each of args should be Symbols
        # targets should be a tuple of Symbols
        self._source = source
        
        self._targets = targets

    def source(self):
        return self._source

    def arity(self):
        return len(self._targets)

    def targets(self):
        return self._targets

    def as_tuple(self):
        assert type(self._source) is Symbol
        assert type(self._targets) is tuple
        
        return (self._source,) + self._targets
    
    def __eq__(self, other):
        return self._source == other._source and self._targets == other._targets
    
    def __hash__(self):
        return hash((self._source, self._targets))

                 
    
class PCFG:
    """The PCFG Grammar object.

    """    
    def __init__(self, terminals = set(), nonterminals = set(), n_ary_rules = dict(), q = dict()):

        #Set of terminal Symbols
        self.terminals = terminals
        #Set of nonterminal Symbols
        self.nonterminals = nonterminals

        #A dict of items with keys aritys and as values sets of *tuples for rules* of the key's arity.
        self._n_ary_rules = n_ary_rules
        #A map from  *tuples for rules* to q values
        self._q = q

        self.CNF = False

    def get_rules_of_arity(self, n):
        """Return the set of rules of arity n"""
        return {Rule(x[0], x[1:]) for x in self._n_ary_rules[n]}

    def set_rule(self, rule):
        n = rule.arity()
        if n not in self._n_ary_rules.keys():
            self._n_ary_rules[n] = {rule.as_tuple()}
        else:
            self._n_ary_rules[n].add(rule.as_tuple())
            
    def set_q(self, rule, q):
        """Set the parameter value for a given rule."""
        self._q[rule.as_tuple()] = q
            
    def q(self, rule):
        return self._q[rule.as_tuple()]

    def unary_rules(self):
        return self.get_rules_of_arity(1)

    def binary_rules(self):
        return self.get_rules_of_arity(2)
        
    def train_from_file(self, file_path, file_type = "TYPED_COUNTS_FILE"):
        """
        Read counts from a counts file, then store counts for each type:
        nonterminal, binary rule and unary rule.


        file_type = "TYPED_COUNTS_FILE" means the file contains lines of the form <count> <type> <args> where 

        <type> is "NONTERMINAL", "UNARYRULE", or "BINARYRULE"
        <args> are the corresponding one, two, or three Symbols, respectively.
        <count> is some given empirical count for this Symbol (for NONTERMINAL) 
        or for this  transformation (for *ARYRULE)
        Assumes all "NONTERMINAL" come first.
        """

        if file_type == "TYPED_COUNTS_FILE":
            #We'll collect counts of 
            nonterminal_counts = dict()
            
            for l in read_lines(file_path):
                count = int(l[0])
                type = l[1]
                vals = l[2:]

                if type == 'NONTERMINAL':
                    nonterminal = Symbol(vals[0])
                    nonterminal_counts[nonterminal] = count
                    self.nonterminals.add(nonterminal)
                else:
                    source = Symbol(vals[0])
                    targets = ()
                    for val in vals[1:]:
                        targets = targets + (Symbol(val),)

                    rule = Rule(source, targets)
                    self.set_rule(rule)
                    #Record Conditional probability of the transition given the source
                    q = count / nonterminal_counts[rule.source()]
                    self.set_q(rule, q)
                    self.CNF = True
                
        elif c_file_style == 1:
            pass
        else:
            pass
    """
    def check_tokens(self, tokens):
        
        Checks whether each token is in the learned
        vocabulary (terminals) of the PCFG.
        
        
        good = True
        for token in tokens:
            if token not in self.terminals:
                good = False
                print("The token ", token, " is not a known terminal.")
        return good
    """
    def check_terminals(self, symbols):
        return True #Change this

            
    def get_symbols(self, sentence):

        """The lexer/tokenizer."""
        for token in  sentence.split():
            new_symbol = Symbol(token)
            yield new_symbol
    
    def score(self, sentence, algorithm = "inside"):
            """Score a sentence with respect to the trained grammar."""
            symbols = list(self.get_symbols(sentence))
            assert self.check_terminals(symbols)
            if algorithm == "inside":
                assert self.CNF, "This PCFG is not in Chomsky Normal Form.  Cannot apply inside algorithm."
                print("Applying Inside algorithm...")
                return self.inside(symbols)


    def parse(self, sentence, algorithm = "CKY"):
        """
        Returns a python dictionary giving the tree structure of the most likely parse.
        """
        symbols = list(self.get_symbols(sentence))
        assert self.check_terminals(symbols)
        if algorithm == "CKY":
            assert self.CNF, "This PCFG is not in Chomsky Normal Form.  Cannot apply inside algorithm."
            print("Applying CKY algorithm...")
            return self.CKY(symbols)

    def inside(self, symbols):

        N = len(symbols)
        pi = dict()
        
        #Initialization
        for i in range(N):
            terminal = symbols[i]
            for X in self.nonterminals:
                
                if (X, terminal) in self.unary_rules():
                    
                    pi[(i, i, X)] = self.q(Rule(X, (terminal,)))
                
                else:
                    pi[(i, i, X)] = 0
        #Recursive Step

        for l in range(N-1):
            for i in range(N-l-1):
                j = i + l + 1
                for X_0 in self.nonterminals:
                    sum = 0
                    for s in range(i, j):
                        for rule in self.binary_rules():
                            X = rule.source()
                            Y, Z = rule.targets()
                            if X == X_0:
                                sum += self.q(rule) *\
                                       pi[i, s, Y] * pi[s+1, j, Z]
                    pi[(i, j, X_0)] = sum
        
        result = pi[0,N-1, Symbol(START_SYMBOL_CODE)]
        print("Final Score:  ", result)
        return result



    def CKY(self, symbols):
        """
        Applies CYK algorithm to list tokens of tokens.  Returns parse tree as a dict.
        """
        N = len(symbols)
        pi = dict()
        bp = dict()
        
        #Initialization
        for i in range(N):
            terminal = symbols[i]
            for X in self.nonterminals:
                if Rule(X, (terminal,)) in self.unary_rules():
                    pi[(i, i, X)] = self.q(Rule(X, (terminal,)))
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
                        for rule in self.binary_rules():
                            X = rule.source()
                            Y, Z = rule.targets()
                            if X == X_0:
                                q_val = self.q(rule)
                                v1 = pi[i, s, Y]
                                v2 = pi[s+1, j, Z]
                                #print("q_val is ", q_val, " v1 is ", v1, " v2 is ", v2)
                                current_score = q_val * v1 * v2
                                #print(current_score)
                                if current_score > max_score:
                                    max_score = current_score
                                    best_rule = Rule(X, (Y, Z))
                                    #print("Best rule is now", best_rule)
                                    best_cut = s
                    pi[(i, j, X_0)] = max_score
                    bp[(i, j, X_0)] = (best_rule, best_cut)
        
        return self.recover_tree(bp, symbols, 0, N-1, Symbol(START_SYMBOL_CODE))

    def recover_tree(self, bp, tokens, i, j, X):
        """Recover a parse tree from a dictionary of back-pointers."""
        tree = dict()
        tree['tag'] = X
        if i == j:
            tree['terminal'] = tokens[i]
        else:
            rule, cut = bp[i, j, X]
            print("Rule is ", rule, " and cut is ", cut)
            left, right = rule.targets()
            tree['left_branch'] = self.recover_tree(bp, tokens, i, cut, left )
            tree['right_branch'] = self.recover_tree(bp, tokens, cut+1, j, right)
        return tree
