from .digraph import Digraph
from .symbol import Symbol, Variable, Terminal
from .rule import Rule

TOLERANCE = .00000000000001
START_SYMBOL_CODE = "S"

def read_lines(training_file_path):
    """Read lines from a file a return an iterator of lists"""
    fi = open(training_file_path, 'r')
    for line in fi:
        fields = line.strip().split(' ')
        yield fields

class CFG:
    """
    A context free grammar.
    """
    
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
        and again, values are corresponding *sets* of Rules"""
        self._rules_by_var = self.compute_rules_by_var()

        self._CFG = self.check_CFG()
        if self._CFG:
            self._CNF = self.check_CNF()

    def compute_rules_by_var(self):
        """ another dict where the indices are source Variables, 
        and again, values are corresponding *sets* of Rules.  Assumes _n_ary_rules is correct."""
        result = dict()
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
            p = type(symbol) is Terminal
            if not p:
                 print("Not every element in self.terminal is a Terminal")
                 result = False

        #Check that every element in self.variable is a Variable
        for symbol in self.variables:
            p = type(symbol) is Variable
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
                    print("Not CNF:  The arity", key, "is non-empty")
                
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
    
