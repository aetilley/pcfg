from .symbol import Symbol, Variable, Terminal
from .rule import Rule


class Tree:
    """
    Every has a symbol and a list of zero or more children.  A node with no children 
    (and only nodes with no children) may be "terminal," but not all nodes with
    no children are terminal.
    """
    
    def __init__(self, expr):
        """Assumes expr is an expression in the format of a line of a UNIV_TREE file"""
        
        if expr[0] != "(":  #tree-expression is atomic (a terminal)
            self.terminal = True
            self.label = expr
            self.children = list()
        else: #tree-expression is non-atomic
            self.terminal = False
            inside = expr[1:-1].strip() #Remove outerparentheses, Then outside whitespace.
            self.label = (inside.split(" "))[0] #crude way to get first word
            

            #A simple finite state machine to parse out child tree-expressions from
            #what remains after the label
            self.children = list()
            start_index = len(self.label) + 1
            #^^index in expr of character immediately after label
            curr_expr = ""
            #l_paren_count = 1
            #r_paren_count = 0
            paren_depth = 1
            #left minus right parens.  We've passed one opening parenthesis
            read_mode = False 
            rest = expr[start_index:]
            for curr_char in rest:
                if curr_char == "(":
                    paren_depth += 1
                    curr_expr += curr_char
                    read_mode = True
                    
                elif curr_char == ")":
                    paren_depth -= 1
                    if (paren_depth == 0) and read_mode:
                        child = Tree(curr_expr)
                        self.children.append(child)
                        curr_expr = ""
                        read_mode = False
                        break
                    
                    curr_expr += curr_char
                    if  (paren_depth == 1) and read_mode:
                        child = Tree(curr_expr)
                        self.children.append(child)
                        curr_expr = ""
                        read_mode = False
                    
                elif curr_char in {" ", "\t"}:
                    if read_mode:
                        if paren_depth == 1:
                            child = Tree(curr_expr)
                            self.children.append(child)
                            curr_expr = ""
                            read_mode = False
                        else:
                            curr_expr += " "
                            
            
                else:#Some character in some (identifier for) some Symbol
                    read_mode = True
                    curr_expr += curr_char


    def to_expr(self):
        if self.terminal:
            return self.label
        else:
            result = "(" + self.label
            for child in self.children:
                result += (" " + child.to_expr())
            result += ")"
            return result
    
        
    def add_counts_return_label(self, rule_counts):
        """Add counts for self into dictionary rule_counts.  
        Return label as Variable or Terminal."""
        
        if self.terminal: #Terminal (single-node) trees have no occurences of Rules)
            return Terminal(self.label)
        else:
            source_code = self.label
            source = Variable(source_code)
            targets = ()
            for child in self.children:
                targets += (child.add_counts_return_label(rule_counts),)

            current_rule = Rule(source, targets)
            if current_rule in rule_counts.keys():
                rule_counts[current_rule] += 1
            else:
                rule_counts[current_rule] = 1
            return source
        
