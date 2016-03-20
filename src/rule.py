from .symbol import Terminal, Symbol, Variable

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
        """
        Make substitutions (in the source or targets) according to dictionary sub_dict which has
        Symbols as keys and Symbols as values.
        """
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
        
    def substitute_many(self, var, new_targs):
        """
        Perhaps currently poorly named, this method allows Not for more than 
        one *kind* of substitution 
        (as does the method substitute(), but rather for more than one symbol to be substituted 
        in the place of one symbol (which substitute() does not currently allow).
        The resulting Rule may therefore be of a different arity than that of the 
        instance on which this 
        method is called.
        """
        assert type(new_targs) is tuple
        same_source = self.source()
        new_targets = ()
        for target in self.targets():
            if target == var:
                new_targets = new_targets + new_targs
            else:
                new_targets = new_targets + (target,)
        new_rule = Rule(same_source, new_targets)
        return new_rule

    def __str__(self):
        return self._source.__str__() + " " + self._targets.__str__()

    def __eq__(self, other):
        return self._source == other._source and self._targets == other._targets

    def __hash__(self):
        return hash((self._source, self._targets))

    def __repr__(self):
        return self._source.__str__() + " " + self._targets.__str__()
