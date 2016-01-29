
(1) Basic Usage
(2) File Types understood by self.train_from_file()

***

(1) Basic Usage:

>  from pcfg import PCFG

>  cnf_grammar = PCFG()
Input data has wrong signature
Valid CFG?:  False

>  cnf_grammar.train_from_file("data/toy_cnf_counts", file_type="CNF_COUNTS")
Training complete.  Running self-check...
Valid CFG?:   True
Valid Parameters?:   True
CNF?:   True


> cnf_grammar.check_PCFG()
Valid CFG?: True
Valid Parameters?: True
Out: True

> cnf_grammar.check_CNF()
CNF?:  True
Out: True

>  cnf_grammar.score("I cited her")
Applying Inside algorithm...
Final Score:   1.657968137022819e-11
Out[]: 1.657968137022819e-11

>  cnf_grammar.parse("I cited her")
Applying CKY algorithm...
Out[]: 
{'left_branch': {'tag': NP+PRON, 'terminal': I},
 'right_branch': {'left_branch': {'tag': VERB, 'terminal': cited},
  'right_branch': {'tag': NP+PRON, 'terminal': her},
  'tag': VP},
 'tag': S}

> other_grammar = PCFG()
Input data has wrong signature
Valid CFG?:   False

> other_grammar.train_from_file("data/toy_univ_pcfg.txt", file_type = "UNIV_PCFG")
Training complete.  Running self-check...
Valid CFG?:   True
Valid Parameters?:   True
Not CNF: the arity  3 is non-empty
Not CNF:  There are unary rules that do not have a Terminal as target
Not CNF:  There are binary rules with targets that are not Variables
CNF?:   False

> other_grammar.check_CFG()
Valid CFG?:   True
Out: True

> other_grammar.check_q()
Valid Parameters?:   True
Out: True

> other_grammar.check_CNF()
Not CNF:  There are unary rules that do not have a Terminal as target
CNF?:   False
Out: False

> other_grammar.score("thomas greets sally")
This PCFG is not in Chomsky Normal Form. Cannot apply inside algorithm.

>len(other_grammar.variables)
Out: 8

>other_grammar.make_CNF()
This process will change the underlying symbol sets
        and rule sets of the PCFG. 
        Continue? (Enter to Continue, CTRL-C to abort.)

CNF?:   True

>other_grammar.check_CNF()
CNF?:   True
Out: True

>len(other_grammar.variables)
Out: 11

>other_grammar.score("thomas greets sally")
Applying Inside algorithm...
Final Score:   0.00252
Out: 0.00252

> other_grammar.parse("thomas greets sally")                                             
Applying CKY algorithm...
Out:
{'left_branch': {'tag': NP, 'terminal': thomas},
 'right_branch': {'left_branch': {'tag': VT, 'terminal': greets},
  'right_branch': {'tag': NP, 'terminal': sally},
  'tag': VP},
 'tag': S}


***



(2) File Types understood by self.train_from_file:

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

