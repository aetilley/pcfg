
START_SYMBOL_CODE = "S"

"""Probabilistic Context-Free Grammar parser/scorer."""


def read_lines(training_file_path):
    """Read lines from a file a return an iterator of lists"""
    fi = open(training_file_path, 'r')
    for line in fi:
        fields = line.strip().split(' ')
        yield fields

class Symbol:
    
    def __init__(self, symbol_code = ""):
        
        self._symbol_code = symbol_code #Eg. "NUMERAL"

    def __str__(self):
        return self._symbol_code
    
    def __repr__(self):
        return self._symbol_code

    def __eq__(self, other):
        return self._symbol_code == other._symbol_code

    def __hash__(self):
        return hash(str(self._symbol_code))


class Variable(Symbol):
    """(The class of Nonterminal Symbols)"""
    def __init__(self, var_code = ""):
        
        self._symbol_code = var_code #For Now



class Terminal(Symbol):
        def __init__(self, term_code = "", from_string = ""):
            if from_string != "":
                self._symbol_code = from_string
            elif term_code != "":
                self._symbol_code = term_code #For now
            else:
                print('Valid form:  Terminal(term_code = "", from_string = "")')
    

class Rule:
    """A transformation (rewrite) rule for any CFG"""

    def __init__(self, source, targets):
        """
        Source should be a Variable
        targets should be a tuple of 0 or more Symbols
        """

        self._source = source
        self._targets = targets
        
        self.check_Rule()

    def check_Rule(self):
        
        assert type(self._source) is Variable, "The source must be of type Variable."
        for target in self._targets:
            assert isinstance(target,  Symbol),  "All targets must be of type Symbol."
            
    def source(self):
        """returns source symbol (Variable symbol being transformed by the grammar.)"""
        return self._source

    def arity(self):
        """Return number of target symbols."""
        return len(self._targets)

    def targets(self):
        """ Return tuple of target symbols """
        return self._targets

    def __str__(self):
        return self.source.__str__() + " " + self._targets.__str__()

    def __eq__(self, other):
        return self._source == other._source and self._targets == other._targets

    def __hash__(self):
        return hash((self._source, self._targets))
    
class CFG():

    def __init__(self, terminals = set(), variables = set(),
                 rules_of_arity = dict(), start_symbol = Variable(START_SYMBOL_CODE)):
        #Set of terminal Symbols
        self.terminals = terminals
        #Set of nonterminal Symbols
        self.variables = variables
        #A dict of items with keys aritys and as values sets of *rules* of the key's arity.
        self._n_ary_rules = rules_of_arity
        self.start_symbol = start_symbol
        self.check_CFG()
                 

    def check_CFG(self):
        """
        Check that self.terminals, self.variables, self._n_ary_rules, 
        and self.start_symbol define a valid PCFG
        """
        prop1a = type(self.terminals) is set
        assert prop1a, "self.terminals must be a set"
        prop2a = type(self.variables) is set
        assert prop2a, "self.variables must be a set"
        prop3a =  type(self._n_ary_rules) is dict
        assert prop3a, "self._nary_rules must be a dict"
        prop4a =  type(self.start_symbol) is Variable
        assert prop4a,"self.start_symbol must be a Variable"
        prop1b = len(self.terminals) > 0
        prop2b = len(self.variables) > 0
        prop3b = len(self._n_ary_rules) > 0
        prop4b = self.start_symbol in self.variables
        
        if not (prop1a and prop2a and prop3a and prop4a and prop1b and prop2b and prop3b and prop4b):
            self.Trained = False
            return False
                 
        term_check = True
        for symbol in self.terminals:
            p = (type(symbol) is Terminal)
            assert p, "self.terminals contains an object of type other than Terminal"
            if not p:
                 term_check = False
                 break

        var_check = True
        for symbol in self.variables:
            p = (type(symbol) is Variable)
            assert p, "self.variables contains an object of type other than Variable"
            if not p:
                 var_check = False
                 break

        n_ary_check = True

        for key in self._n_ary_rules.keys():
            p = type(key) is int and type(self._n_ary_rules[key]) is Rule
            if not p:
                 n_ary_check = False
                 break
                 
        if term_check and var_check and n_ary_check:
            """#Probably want to also include restriction that
            the Symbols in the Rules in self._n_ary_rules 
            all appear in self.terminals and self.variables.
            """
            self.Trained = True
            return True
        else:
            self.Trained = False
            return False

    def get_rules_of_arity(self, n):
        """Return the set of rules of arity n"""
        if n not in self._n_ary_rules.keys():
            return {}
        return self._n_ary_rules[n]

    def add_rule(self, rule):
        n = rule.arity()
        if n not in self._n_ary_rules.keys():
            self._n_ary_rules[n] = {rule}
        else:
            self._n_ary_rules[n].add(rule)

    def unary_rules(self):
        return self.get_rules_of_arity(1)

    def binary_rules(self):
        return self.get_rules_of_arity(2)

    def check_terminals(self, symbols):
        for symbol in symbols:
            if symbol not in self.terminals:
                 print("The symbol ", symbol, " is not a known terminal.")
                 return False
        return True
                 
    def get_terminals(self, sentence):
        """The lexer/tokenizer."""
        for token in sentence.split():
            new_symbol = Terminal(token)
            yield new_symbol

                 
class PCFG(CFG):

    def __init__(self, terminals = set(), variables = set(),
                 rules_of_arity = dict(), q = dict()):

        super().__init__(terminals = terminals, variables = variables,
                         rules_of_arity = rules_of_arity)

        self._q = q
                 
        self.check_PCFG()

    def check_PCFG(self):
        return self.check_CFG() and self.check_q()

    def check_q(self):
        for rule in self._q.keys():
            q = self._q[rule]
            prop = type(rule) is Rule and type(q) is float and 0 <= q <= 1
            if not prop:
                return False
        return True

    def set_q(self, rule, q):
        """Set the parameter value for a given rule."""
        self._q[rule] = q
            
    def q(self, rule):
        return self._q[rule]
            
    def train_from_file(self, file_path, file_type = "CNF_COUNTS"):
        """
        This function is meant to act on a variety of data file formats in order to

        1)  Learn the Terminals and Variables AND
        2)  Compute the transition rule set (for self.get_rules_of_arity(<arity>)) AND
        3)  Compute the q parameter for each transition rule (for self.q(<rule>)

        File Types:

        file_type = "CNF_COUNTS" means the grammar to be learned is in Chomsky Normal Form and
        that the file contains lines of the form <count> <type> <args> where 
        <type> is "NONTERMINAL", "UNARYRULE", or "BINARYRULE"
        <args> are the corresponding one, two, or three Symbols, respectively.
        <count> is some given empirical count for this Symbol (for NONTERMINAL) 
        or for this  transformation (for *ARYRULE)
        Assumes all "NONTERMINAL" come first.

        File types to support:  NCNF_COUNTS, CNF_PARAMS
        """

        if file_type == "CNF_COUNTS":

            variable_counts = dict()
            
            for l in read_lines(file_path):
                count = int(l[0])
                type = l[1]
                vals = l[2:]

                if type == 'NONTERMINAL':
                    new_var = Variable(vals[0])
                    variable_counts[new_var] = count
                    self.variables.add(new_var)
                else:
                    source = Variable(vals[0])
    
                    if len(vals) == 2:
                        new_term = Terminal(vals[1])
                        self.terminals.add(new_term)
                        targets = (new_term,)
                
                    else:
                        targets = ()
                        for val in vals[1:]:
                            targets = targets + (Variable(val),)

                    rule = Rule(source, targets)
                    self.add_rule(rule)
                    #Record Conditional probability of the transition given the source
                    q = count / variable_counts[source]
                    self.set_q(rule, q)
                    
            self.check_PCFG()
            self.CNF = True #make this the result of some check function
            
        elif c_file_style == "NCNF_COUNTS":
            pass
        elif c_file_style == "CNF_PARAMS":
            pass
        else:
            pass
                 
            
    def score(self, sentence, algorithm = "inside"):
        """Score a sentence with respect to the PCFG."""
        terminals = list(self.get_terminals(sentence))
        assert self.check_terminals(terminals)
        if algorithm == "inside":
            assert self.CNF, "This PCFG is not in Chomsky Normal Form.  Cannot apply inside algorithm."
            print("Applying Inside algorithm...")
            return self.inside(terminals)
        else:
            print("Algorithm not known")
            quit()


    def parse(self, sentence, algorithm = "CKY"):
        """
        Returns a python dictionary giving the tree structure of the most likely parse.
        """
        terminals = list(self.get_terminals(sentence))
        assert self.check_terminals(terminals)
        if algorithm == "CKY":
            assert self.CNF, "This PCFG is not in Chomsky Normal Form.  Cannot apply inside algorithm."
            print("Applying CKY algorithm...")
            return self.CKY(terminals)
        else:
            print("Algorithm not known")
            quit()
            
    def inside(self, symbols):

        N = len(symbols)
        pi = dict()
        
        #Initialization
        for i in range(N):
            terminal = symbols[i]
            for X in self.variables:
                
                if Rule(X, (terminal,)) in self.unary_rules():
                    pi[(i, i, X)] = self.q(Rule(X, (terminal,)))
                
                else:
                    pi[(i, i, X)] = 0
        #Recursive Step

        for l in range(N-1):
            for i in range(N-l-1):
                j = i + l + 1
                for X_0 in self.variables:
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
            for X in self.variables:
                if Rule(X, (terminal,)) in self.unary_rules():
                    pi[(i, i, X)] = self.q(Rule(X, (terminal,)))
                else:
                    pi[(i, i, X)] = 0

        #Recursive Step
        for l in range(N-1):
            for i in range(N-l-1):
                j = i + l + 1
                for X_0 in self.variables:
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
                                current_score = q_val * v1 * v2
                                if current_score > max_score:
                                    max_score = current_score
                                    best_rule = Rule(X, (Y, Z))
                                    best_cut = s
                    pi[(i, j, X_0)] = max_score
                    bp[(i, j, X_0)] = (best_rule, best_cut)
        
        return self.recover_tree(bp, symbols, 0, N-1, Symbol(START_SYMBOL_CODE))

    def recover_tree(self, bp, symbols, i, j, X):
        """Recover a parse tree from a dictionary of back-pointers."""
        tree = dict()
        tree['tag'] = X
        if i == j:
            tree['terminal'] = symbols[i]
        else:
            rule, cut = bp[i, j, X]
            left, right = rule.targets()
            tree['left_branch'] = self.recover_tree(bp, symbols, i, cut, left )
            tree['right_branch'] = self.recover_tree(bp, symbols, cut+1, j, right)
        return tree
    
