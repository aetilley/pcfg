
class Symbol:
    
    def __init__(self, symbol_code):
        self._symbol_code = symbol_code

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

