from digraph import Digraph


TOLERANCE = .00000000000001
START_SYMBOL_CODE = "S"

"""Probabilistic Context-Free Grammar parser/scorer."""

def read_lines(training_file_path):
    """Read lines from a file a return an iterator of lists"""
    fi = open(training_file_path, 'r')
    for line in fi:
        fields = line.strip().split(' ')
        yield fields

class Symbol:
    
    def __init__(self):
        self._symbol_code = None

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
        self.var_code = var_code
        self._symbol_code = self.var_code #For Now



class Terminal(Symbol):
        def __init__(self, term_code = "", from_string = None):
            if from_string:
                self.term_code = from_string
            else:
                self.term_code = term_code
            self._symbol_code = self.term_code #For Now

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
            assert isinstance(target,  Symbol),  "All targets must be instances of type Symbol."
            
    def source(self):
        """returns source symbol (Variable symbol being transformed by the grammar.)"""
        return self._source

    def arity(self):
        """Return number of target symbols."""
        return len(self._targets)

    def targets(self):
        return self._targets
    
    def target(self, i):
        """ Return tuple of target symbols """
        return self._targets[i]

    def set_target(self, i, new_target):
        self._targets[i]= new_target
    

    def substitute(self, sub_dict):
        source = self.source()
        if source in sub_dict.keys():
            new_source = sub_dict[source]
        else:
            new_source = source
        new_targets = ()
        for target in self.targets():
            if target in sub_dict.keys():
                new_target = sub_dict[target]
            else:
                new_target = target
            new_targets = new_targets + (new_target,)
        new_rule = Rule(new_source, new_targets)
        return new_rule
        


    def __str__(self):
        return self._source.__str__() + " " + self._targets.__str__()

    def __eq__(self, other):
        return self._source == other._source and self._targets == other._targets

    def __hash__(self):
        return hash((self._source, self._targets))
    
class CFG:

    def __init__(self, terminals = None, variables = None,
                 rules_of_arity = None, start_symbol = None):
        self._CFG = False
        self._CNF = False
        self.start_symbol = start_symbol or Variable(START_SYMBOL_CODE)
        #Set of the grammar's Terminals
        self.terminals = terminals or set()
        #Set of the grammar's Variables
        self.variables = variables or set()
        """A dict of items with keys aritys and as values *sets* of *rules* of the key's arity."""
        self._n_ary_rules = rules_of_arity or dict()
        """ another dict where the indices are source Variables, 
        and again, values are corresponding *sets* of *rules*"""
        self._rules_by_var = self.compute_rules_by_var()

        self._CFG = self.check_CFG()
        if self._CFG:
            self._CNF = self.check_CNF()

    def compute_rules_by_var(self):
        result = dict()
        # var in self.variables:
        for n in self._n_ary_rules.keys():
            for rule in self.get_rules_of_arity(n):
                var = rule.source()
                if var not in result.keys():
                    result[var] = {rule}
                else:
                    result[var].add(rule)
        return result

            
    def check_CFG(self):
        """
        Check that self.terminals, self.variables, self._n_ary_rules, 
        and self.start_symbol define a valid CFG
        """
        result = True
        
        prop1a = type(self.terminals) is set
        prop2a = type(self.variables) is set
        prop3a1 =  type(self._n_ary_rules) is dict
        prop3a2 = type(self._rules_by_var) is dict
        prop4a =  type(self.start_symbol) is Variable
        prop4b = self.start_symbol in self.variables
        
        if not (prop1a and prop2a and prop3a1 and prop3a2 and prop4a and prop4b):
            print("Input data has wrong signature")
            result = False

        #Check that every element in self.terminal is a Terminal
        for symbol in self.terminals:
            p = (type(symbol) is Terminal)
            if not p:
                 print("Not every element in self.terminal is a Terminal")
                 result = False


        #Check that every element in self.variable is a Variable
        for symbol in self.variables:
            p = (type(symbol) is Variable)
            if not p:
                print("Not every element of self.variable is a Variable.")
                result = False


        #Check the rule index is indexed by an int and has value a Rule
        for key in self._n_ary_rules.keys():
            p = type(key) is int
            if not p:
                print("keys to _n_ary_rules should all be integers")
                result = False
            else:
                if type(self._n_ary_rules[key]) is not set:
                    print("Values of self._n_ary_rules should be sets")
                    result = False
                else:
                    for rule in self._n_ary_rules[key]:
                        if type(rule) is not Rule:
                            print("Something in the set _n_ary_rules[",key,"] is not a rule.")
                            result =  False
        print("Valid CFG?:  ", result)
        return result
        
    def get_rules_of_arity(self, n):
        """Return the set of rules of arity n"""
        if n not in self._n_ary_rules.keys():
            return {}
        return self._n_ary_rules[n]

    def get_rules_from_source(self, var):
        return self._rules_by_var[var]

    
    def add_rule(self, rule):
        n = rule.arity()
        if n not in self._n_ary_rules.keys():
            self._n_ary_rules[n] = {rule}
        else:
            self._n_ary_rules[n].add(rule)
        var = rule.source()
        if var not in self._rules_by_var.keys():
            self._rules_by_var[var] = {rule}
        else:
            self._rules_by_var[var].add(rule)

    def remove_rule(self, rule):
        self._n_ary_rules[rule.arity()].remove(rule)
        self._rules_by_var[rule.source()].remove(rule)
    def unary_rules(self):
        return self.get_rules_of_arity(1)

    def binary_rules(self):
        return self.get_rules_of_arity(2)

    def check_terminals(self, symbols):
        """
        Check that input list consists of known Terminals 
        """
        for symbol in symbols:
            if symbol not in self.terminals:
                 print("The symbol ", symbol, " is not a known terminal.")
                 return False
        return True
                 
    def get_terminals(self, sentence):
        """The lexer/tokenizer."""
        for token in sentence.split():
            new_terminal = Terminal(token)
            yield new_terminal

    def check_CNF(self):
        result = True
        #Only rules of arity 1 and 2:
        for key in self._n_ary_rules.keys():
            if key not in {1, 2}:
                if len(self._n_ary_rules[key]) != 0:
                    result = False
                    print("Not CNF: the arity ", key, "is non-empty")
                
        for unary_rule in self.unary_rules():
            unary_check = type(unary_rule.target(0)) is Terminal
            if not unary_check:
                print("Not CNF:  The unary rule", unary_rule," has as target", unary_rule.target(0))
                result = False
                break
        for binary_rule in self.binary_rules():
            binary_check = type(binary_rule.target(0)) is Variable and\
                           type(binary_rule.target(1)) is Variable
            if not binary_check:
                print("Not CNF:  There are binary rules with targets that are not Variables")
                result = False
                break
        print("CNF?:  ", result)
        return result
    
                 
class PCFG(CFG):

    def __init__(self, terminals = None, variables = None,
                 rules_of_arity = None, start_symbol = Variable(START_SYMBOL_CODE),
                 q = None):
        super().__init__(terminals, variables, rules_of_arity, start_symbol)
        self._q = q or dict()
        self.TOLERANCE = TOLERANCE
        if self._CFG:
            self.check_q()
    # def __init__(self, cfg, q = dict())
    
    def check_PCFG(self):
        #Sets self.trained
        cfg = self.check_CFG()
        if not cfg:
            return False
        else:
            valid_q = self.check_q()
            return valid_q
        print("Valid PCFG?:  ", valid_q)
        return valid_q
        

        
    def check_q(self):
        #This will be the source of KeyErrors if self.variables
        #and .self._rules_by_var.keys() are not synced.
        """Verifies that the q parameter data on record actually makes sense."""
        result = True
        for var in self.variables:
            sum = 0
            for rule in self.get_rules_from_source(var):
                prop1 = type(rule) is Rule
                if not prop1:
                    print(rule, "is not a Rule.")
                    result = False
                        
                q = self.q(rule)
                prop2 = type(q) is float and 0 <= q <= 1
                if not prop2:
                    print(q, "is not a float between 0 and 1 inclusive.")
                    result = False
                        
                sum += q
                        
            if abs(1 - sum) > self.TOLERANCE:
                print("The rules with source equal to the Variable ", var)
                print("do not have parameters summing to within self.TOLERANCE of 1.")
                print("The sum is ", sum)
                result = False
                    
        print("Valid Parameters?:  ", result)
        return result
    def remove_rule(self, rule):
        super().remove_rule(rule)
        self._q.pop(rule)
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

        file_type = "UNIV_PCFG" uses the assumptions that, in any description of a PCFG:
        1)  All variables should be the source of some rule and,
        2)  The sources of all rules should be known variables, thus
        in particular we find that we can  determine a PCFG
        just by listing rules and their corresponding parameters
        For example the following file gives a complete description of a PCFG:

        S .2
        S S .2
        S NP VP .6
        NP DET NN .8
        NP thomas .1
        NP sally .1
        DET the 1.
        NN milkman 1.
        VP VT NP .6
        VP VI .4
        VI runs 1.
        VT greets 1.
                
        For any given line, that the first element (whitespace delimited element) is always the source of the rule in question.  
        The last element is always the probability of the transition from this source to the targets
        The aforementioned targests are exactly the zero or more elements between
        the first element and the last element of the line.
        So for example the line S .2 would mean a 0-ary rule with source S and targets (), 
        and that the conditional probability of this transition to () given S is .2.
        Note also that every symbol that appears in the middle but never on the left is assumed to be a Terminal


        file_type = "CNF_COUNTS" means the grammar to be learned is in Chomsky Normal Form and
        that the file contains lines of the form <count> <type> <args> where 
        <type> is "NONTERMINAL", "UNARYRULE", or "BINARYRULE"
        <args> are the corresponding one, two, or three Symbols, respectively.
        <count> is some given empirical count for this Symbol (for NONTERMINAL) 
        or for this  transformation (for *ARYRULE)
        Assumes all "NONTERMINAL" come first.

        """

        
        #file_type: UNIV_PCFG
        if file_type == "UNIV_PCFG":
        # Double Read
            for l in read_lines(file_path):
                var = Variable(l[0])
                self.variables.add(var)

            for l in read_lines(file_path):
                source_code = l[0]
                target_codes = l[1:-1]
                
                q = float(l[-1])

                source = Variable(var_code = source_code)
                targets = ()
                for code in target_codes:
                    if Variable(code) in self.variables:
                        target = Variable(var_code = code)
                    else:
                        target = Terminal(term_code = code)
                        self.terminals.add(target)
                    targets = targets + (target,)
                rule = Rule(source, targets)
                self.add_rule(rule)
                self.set_q(rule, q)

        #file_type: CNF_COUNTS
        elif file_type == "CNF_COUNTS":

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

        else:
            print("Unknown file_type parameter.")
            
        #Examine Result of Import:
        print("Training complete.  Running self-check...")
        self._CFG = self.check_CFG()
        if self._CFG:
            self.check_q()
            self._CNF = self.check_CNF()












#Begin helper functions for main conversion function
            
    def add_term_variables(self):

        """
        For each terminal T that appears in the RHS
        of some rule of arity n > 1, replace T by a variable U_T in that rule.
        Also add the unary rule from U_T to T and add the
        associated parameter 1. for this new rule.
        """

        for n in self._n_ary_rules.keys():
            if n > 1:
                for rule in self.get_rules_of_arity(n).copy():
                    new_targets = ()
                    remove = False
                    for i in range(n):
                        symbol = rule.target(i)
                        if type(symbol) is Terminal:
                            remove = True
                            new_var = Variable("U-"+symbol.term_code)
                            new_target = new_var                            
                            self.variables.add(new_var)
                            new_aux_rule = Rule(new_var, (symbol,))
                            self.add_rule(new_aux_rule)
                            self.set_q(new_aux_rule, 1.)
                        else:
                            new_target = symbol
                        new_targets = new_targets + (new_target,)
                    if remove:
                        new_rule = Rule(rule.source(), new_targets)
                        self.add_rule(new_rule)
                        self.set_q(new_rule, self.q(rule))
                        self.remove_rule(rule)
                    
     
    def remove_higher_arities(self):
        for n in self._n_ary_rules.keys():
            if n > 2:
                #For each rule of arity at least 3..
                for rule in self.get_rules_of_arity(n).copy():
                    source = rule.source()
                    targets = rule.targets()
                    #Add the steppingstones...
                    last  = source
                    for i in range(n-1):
                        if i < n - 2:
                            new_var_code = "X" + str(i) + str(hash(rule))
                            new_var = Variable(var_code = new_var_code)
                            self.variables.add(new_var)
                        elif i == n-2:
                            new_var = targets[n-1]
                        else: print("Error")
                        
                        new_binary_rule = Rule(last,(rule.target(i), new_var))
                        self.add_rule(new_binary_rule)
                        new_q  = self.q(rule) if i == 0 else 1.
                        self.set_q(new_binary_rule, new_q)
                        last = new_var
                    #and remove the rule of high arity.
                    self.remove_rule(rule)

    def refresh_start_symbol(self):
        start = self.start_symbol
        #Make a new special symbol...
        special = Variable(var_code = start.var_code + "'")
        self.variables.add(special)
        #...substitute special for the start symbol throughout...
        for n in self._n_ary_rules.keys():
            
            iteration_copy = self.get_rules_of_arity(n).copy()
            for rule in iteration_copy:
                q = self.q(rule)
                self.remove_rule(rule)
                new_rule = rule.substitute({start: special})
                self.add_rule(new_rule)              
                self.set_q(new_rule, q)

        start_symbol_rule = Rule(start, (special,))
        self.add_rule(start_symbol_rule)
        self.set_q(start_symbol_rule, 1.)

    def compute_unit_rule_graph(self):

        graph = dict()
        for unary_rule in self.unary_rules():
            tip  = unary_rule.target(0)
            if type(tip) is Variable:
                tail = unary_rule.source()
                if tail in graph.keys():
                    graph[tail].add(tip)
                else:
                    graph[tail] = {tip}
        dg = Digraph(V = self.variables, E = graph)
        return dg
        # compute s.c.c. of graph

    def remove_and_renormalize(self, rule_to_remove):
        q_to_redist = self.q(rule_to_remove)
        self.remove_rule(rule_to_remove)
        source_to_adjust = rule_to_remove.source()
        for rule in self.get_rules_from_source(source_to_adjust):
            old_q = self.q(rule)
            new_q = old_q + old_q*(q_to_redist / (1 - q_to_redist))
            self.set_q(rule, new_q)


            
        
    def remove_unit_rules(self):
        """
        A unit rule is a unary rule whose target is a Variable.
        """
        
        G = self.compute_unit_rule_graph()

        #First absorb strongly connected components to make acyclic.
        #We compute the equiv. classes
        
        var_to_root_map = G.compute_roots()
        
        root_variables = set()
        for var in self.variables:
            new_var = var_to_root_map[var]
            root_variables.add(new_var)


            
        #Replace each non-root variable occurence by its root in every rule
        for n in self._n_ary_rules.keys():

            q_sums = dict()
            for var in self.variables:
                q_sums[var]=dict()
                
            rules_copy =self.get_rules_of_arity(n).copy()
            
            for rule in rules_copy:
                old_source = rule.source()
                new_rule = rule.substitute(var_to_root_map)
                new_targets = new_rule.targets()
                if new_targets in q_sums[old_source].keys():
                    
                    q_sums[old_source][new_targets] += self.q(rule)
                else:
                    q_sums[old_source][new_targets] = self.q(rule)
                    
                self.remove_rule(rule)

            #This is overkill but
            for rule in rules_copy:
                new_rule = rule.substitute(var_to_root_map)

                new_source = new_rule.source()
                new_targets = new_rule.targets()

                tot = 0
                for eq_var in G.equiv(new_source):
                    if eq_var != new_source:
                        link_rule = Rule(new_source, (eq_var,))
                        if link_rule in self.unary_rules():
                            factor = self.q(link_rule)
                        else:
                            factor = 0
                        tot += factor * q_sums[eq_var][new_targets]
                
                new_q = q_sums[new_source][new_targets] + tot

                self.add_rule(new_rule)
                self.set_q(new_rule, new_q)


                
        #Update self.variables
        self.variables = root_variables
            
        #And remove the trivial unit rules (V -> V)
        for var in self.variables:
            trivial = Rule(var, (var,))
            if trivial in self.unary_rules():
                self.remove_and_renormalize(trivial)

        #Finally we do a reverse topological traversal of the new graph
        H = self.compute_unit_rule_graph()
        #Note that this is now a DAG and thus has a topological order.
        topological = H.reverse_DFS_post_order()
        order  = reversed(topological)
            
        for tip in order:
            """
            Find the edges in H that point to vertex,
            and remove them (after supplying replacement rules and parameters
            Note that the following process automatically re-normalizes since for each
            unit_rule removed, the binary_rules introduced have the
            same source as unit_rule and have RHSs summing to 1
            
            #Note that at this point in the ordering there should only
            #be Terminals and binary targets on the right of tip in any rule
            """

            for tail in self.variables:
                if tip in H.E[tail]:
                    unit_rule = Rule(tail, (tip,))
                    q_to_replace = self.q(unit_rule)
                    for binary_rule in self.binary_rules().copy():
                        if binary_rule.source() == tip:
                            new_rule = Rule(tail, binary_rule.targets())
                            new_q = self.q(binary_rule) * q_to_replace
                            self.add_rule(new_rule)
                            self.set_q(new_rule, new_q)
                    for unary_rule in self.unary_rules().copy():
                        if unary_rule.source() == tip and type(unary_rule.target(0)) is Terminal:
                            new_rule = Rule(tail, unary_rule.targets())
                            new_q = self.q(unary_rule) * q_to_replace
                            self.add_rule(new_rule)
                            self.set_q(new_rule, new_q)
                    self.remove_rule(unit_rule)
                    
    def make_CNF(self):
        """
        Adds appropriate symbols and adds/removes appropriate rules
        to turn any valid CFG into one in Chomsky Normal Form
        """

        print("""This process will change the underlying symbol sets
        and rule sets of the PCFG. 
        Continue? (Enter to Continue, CTRL-C to abort.)""")
        input()            

        
        #1
        self.add_term_variables()

        #2
        self.remove_higher_arities()

        #3
        self.refresh_start_symbol()

        #(Later) remove_zero_ary_rules().  For now just rely on their being absent.

        #4
        self.remove_unit_rules()

        #5 Final diagnostics
        self.check_PCFG()
        
        self._CNF = self.check_CNF()
        


            
    def score(self, sentence, algorithm = "inside"):
        """Score a sentence with respect to the PCFG."""
        terminals = list(self.get_terminals(sentence))
        assert self.check_terminals(terminals)
        if algorithm == "inside":
            if not self._CNF:
                print("This PCFG is not in Chomsky Normal Form. Cannot apply inside algorithm.")
                return None
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
            assert self._CNF, "This PCFG is not in Chomsky Normal Form.  Cannot apply inside algorithm."
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
        
        result = pi[0,N-1, Variable(START_SYMBOL_CODE)]
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
        
        return self.recover_tree(bp, symbols, 0, N-1, Variable(START_SYMBOL_CODE))

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
    
