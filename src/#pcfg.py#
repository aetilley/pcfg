from .tree import Tree
from .digraph import Digraph
from .rule import Rule
from .symbol import Variable, Symbol, Terminal
from .cfg import CFG


TOLERANCE = .00000000000001
START_SYMBOL_CODE = "S"

"""Probabilistic Context-Free Grammar parser/scorer."""

def read_lines(training_file_path):
    """Read lines from a file a return an iterator of lists"""
    fi = open(training_file_path, 'r')
    for line in fi:
        fields = line.strip().split(' ')
        yield fields

                 
class PCFG(CFG):
    """
    A CFG with real numbers called parameters assigned to each rule such that the rules with 
    fixed source have parameters summing to one.
    """
    
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
    def add_rule(self, rule):
        super().add_rule(rule)
    def remove_rule(self, rule):
        super().remove_rule(rule)
        self._q.pop(rule)
    def set_q(self, rule, q):
        """Set the parameter value for a given rule."""
        self._q[rule] = q
            
    def q(self, rule):
        return self._q[rule]

    def write_pcfg(self, new_file_path = None):
        """Create a file with name and location given by new_file_path giving the 
        complete data for this pcfg object in UNIV_PCFG file format."""
        
        WRITE_FILE_PATH = new_file_path or "univ_pcfg_0.txt"
        write_file = open(WRITE_FILE_PATH, 'w')

        arities = list(self._n_ary_rules.keys())
        arities.sort()
        arities.reverse()
        
        for n in arities:
            for rule in self.get_rules_of_arity(n):
                source = rule.source()
                targets = rule.targets()
                q = self.q(rule)
                write_file.write(source._symbol_code)
                write_file.write(" ")
                for target in targets:
                    write_file.write(target._symbol_code)
                    write_file.write(" ")
                write_file.write(str(q))
                write_file.write("\n")
        write_file.close()

    def __eq__(self, other):
        return self._n_ary_rules == other._n_ary_rules and \
            self._q == other._q and \
            self._rules_by_var == other._rules_by_var and \
            self.variables == other.variables and \
            self.terminals == other.terminals
    
        

    def train_from_counts_dict(self, counts):
        """
        Train a PCFG from a dictionary of rule counts.

        Assumes counts keys are Rules with generic targets (possibly
        Symbols not Terminals or Variables) and the items have integer values
        """

        variable_counts = dict() #A dict with keys Variables and values counts

        #Double read
        for rule in counts.keys():
            count = counts[rule]
            source = rule.source()
            if source in variable_counts.keys():
                variable_counts[source] += count
            else:
                variable_counts[source] = count
                self.variables.add(source)

        for rule in counts.keys():
            count = counts[rule]
            source = rule.source()
            targets = rule.targets()
            arity = rule.arity()
            new_targets = ()
            for target in targets:
                symbol = target._symbol_code
                new_var = Variable(symbol)
                if new_var in self.variables:
                    new_targets += (new_var,)
                else:
                    new_term = Terminal(symbol)
                    new_targets += (new_term,)
                    self.terminals.add(new_term)
            rule = Rule(source, new_targets)
            #MLE Estimate
            q = count / variable_counts[source]
            self.add_rule(rule)
            self.set_q(rule, q)

            
    def train_from_file(self, file_path, file_type):
        """
        Available File Types:
        UNIV_PCFG
        UNIV_COUNTS
        UNIV_TREE

        See README.txt and derivation_example.txt for a detailed description of each file_type.

        This method (while might eventually be made part of a constructor) is meant to act on
        a variety of data file formats in order to
 
        1)  Learn the Terminals and Variables AND
        2)  Compute the transition rule set (for self.get_rules_of_arity(<arity>)) AND
        3)  Compute the q parameter for each transition rule (for self.q(<rule>)

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

        #file_type:  UNIV_COUNTS
        elif file_type == "UNIV_COUNTS":
            d = dict()
            for l in read_lines(file_path):
                count = int(l[0])
                source_symbol = l[1]
                source = Variable(source_symbol)
                target_symbols = l[2:]
                targets = ()
                for target_symbol in target_symbols:
                    symbol = Symbol(target_symbol)
                    targets += (symbol,)
                rule = Rule(source, targets)
                d[rule] = count
            self.train_from_counts_dict(d)


                    
        #UNIV_TREE file type
        elif(file_type == "UNIV_TREE"):
            counts = dict()
            file = open(file_path, 'r')
            for line in file:
                expr = line.strip()
                tree = Tree(expr)
                tree.add_counts_return_label(counts)
            self.train_from_counts_dict(counts)
            #Now proceed as in UNIV_COUNTS
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

    def absorb_strong_components(self, recursion_depth = 0):
        
        G = self.compute_unit_rule_graph()

        #We aim to absorb strongly connected components to make digraph acyclic.
        
        var_to_root_map = G.compute_roots()
        
        #print("root of NP is", var_to_root_map[Variable("NP")])
        
        root_variables = set()
        for var in self.variables:
            new_var = var_to_root_map[var]
            root_variables.add(new_var)

        for var in self.variables.difference(root_variables):
            extensions = self.get_rules_from_source(var).copy()
            filla = Terminal("FILLA")
            keep = {(filla,): 0}
            for extension in extensions:
                if var in extension.targets():
                    keep[filla] += self.q(extension)
                else:
                    keep[extension.targets()] = self.q(extension)
                self.remove_rule(extension)
            for n in self._n_ary_rules.copy().keys():
                for rule in self.get_rules_of_arity(n).copy():
                    if var in rule.targets():
                        for sub_targets in keep.keys():
                            new_rule = rule.substitute_many(var, sub_targets)
                            new_q = self.q(rule) * keep[sub_targets]
                            self.add_rule(new_rule)
                            self.set_q(new_rule, new_q)
                        self.remove_rule(rule)
                    else:
                        pass
            
        #Update self.variables
        self.variables = root_variables

        #And remove the trivial unit rules (V -> V)
        for var in self.variables:
            trivial = Rule(var, (var,))
            if trivial in self.unary_rules():
                self.remove_and_renormalize(trivial)

        
    def remove_unit_rules(self):
        """
        A unit rule is a unary rule whose source and target are both Variables.
        """

        #Replace each non-root variable occurence by its root in every rule.

        #First we build a dictionary from source symbols in the larger language into
        #target strings in the reduced language
        """

        unary_rules_copy = self.unary_rules().copy() #hack
        q_copy = self._q.copy() #hack
        
        for n in self._n_ary_rules.keys():

            q_sums = dict()
            for var in self.variables:
                q_sums[var]=dict()
                
            rules_of_arity_n_copy =self.get_rules_of_arity(n).copy()

            for rule in rules_of_arity_n_copy:
                old_source = rule.source()
                new_rule = rule.substitute(var_to_root_map)
                new_targets = new_rule.targets()
                if new_targets in q_sums[old_source].keys():
                    
                    q_sums[old_source][new_targets] += self.q(rule)
                else:
                    q_sums[old_source][new_targets] = self.q(rule)

                self.remove_rule(rule)


            #Now make new rules
            for rule in rules_of_arity_n_copy:
    
                new_rule = rule.substitute(var_to_root_map)
                new_source = new_rule.source()
                new_targets = new_rule.targets()

                tot = 0
                for eq_var in G.equiv(new_source):
                    if eq_var != new_source:
                        link_rule = Rule(new_source, (eq_var,))
                        if link_rule in unary_rules_copy:
                            factor1 = q_copy[link_rule]
                        else:
                            factor1 = 0
                        if new_targets in q_sums[eq_var].keys():
                            factor2 = q_sums[eq_var][new_targets]
                        else:
                            factor2 = 0
                        tot += factor1 * factor2
                term0 = q_sums[new_source][new_targets] \
                        if new_targets in q_sums[new_source].keys() else 0
                new_q = term0 + tot
                
                self.add_rule(new_rule)

                self.set_q(new_rule, new_q)
        """
        

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

        print("""This process will change the underlying symbol sets and rule sets of the PCFG. 
        Continue? (Enter to Continue, CTRL-C to abort.)""")
        input()            
        #0
        self.absorb_strong_components()
        
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
        










#Begin Parse / Score methods


            
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
        Applies CYK algorithm to list symbols of symbols.  Returns parse tree as a dict.
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
        
        
        if i == j:
            
            expr = "(" + X.var_code + " " + symbols[i].term_code + ")"
            return Tree(expr)
            
        else:
            rule, cut = bp[i, j, X]
            left, right = rule.targets()
            left_child = self.recover_tree(bp, symbols, i, cut, left)
            right_child = self.recover_tree(bp, symbols, cut+1, j, right)
            expr = "(" + X._symbol_code + " " + left_child.to_expr() + \
                   " " + right_child.to_expr() + " )"
            return Tree(expr)
    

    def parse_file(self, source_file_path, dest_file_path):
        raw_file = open(source_file_path, 'r')
        new_file = open(dest_file_path, 'w')

        for raw_line in raw_file:
            tree = self.parse(raw_line)
            expr = tree.to_expr()+"\n"
            new_file.write(expr)

        new_file.close()
        raw_file.close()
