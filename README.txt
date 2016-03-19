
(1) Basic Usage
(2) File Types understood by self.train_from_file()
(3) A note on file types and training PCFGs.
(4) Coming Soon / More info

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
 
> cnf_grammar.print_pcfg("univ_pcfg_out.txt")

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

> other_grammar.make_CNF()
This process will change the underlying symbol sets
        and rule sets of the PCFG. 
        Continue? (Enter to Continue, CTRL-C to abort.)

Valid CFG?:   True
Valid Parameters?:   True
CNF?:   True

> other_grammar.check_CNF()
CNF?:   True
Out: True

> other_grammar.score("thomas greets sally")
Applying Inside algorithm...
Final Score:   0.0015844273426889994
Out: 0.0015844273426889994


> other_grammar.parse("thomas greets sally")                                                     
Applying CKY algorithm...
Out:
{'left_branch': {'tag': U-thomas, 'terminal': thomas},
 'right_branch': {'left_branch': {'tag': VT, 'terminal': greets},
  'right_branch': {'tag': U-sally, 'terminal': sally},
  'tag': VP},
 'tag': S}

> other_grammar.score("thomas greets the milkman")
Applying Inside algorithm...
Final Score:   0.0033711220057212757
Out: 0.0033711220057212757

> other_grammar.parse("thomas greets the milkman")                                               
Applying CKY algorithm...
Out:
{'left_branch': {'tag': U-thomas, 'terminal': thomas},
 'right_branch': {'left_branch': {'tag': VT, 'terminal': greets},
  'right_branch': {'left_branch': {'tag': DET, 'terminal': the},
   'right_branch': {'tag': NN, 'terminal': milkman},
   'tag': X0-332371785976609858},
  'tag': VP},
 'tag': S}

> new_grammar = PCFG()
Input data has wrong signature
Valid CFG?:   False

> new_grammar.train_from_file("data/toy_univ_counts.txt", file_type="UNIV_COUNTS")                          
Training complete.  Running self-check...
Valid CFG?:   True
Valid Parameters?:   True
CNF?:   True

> new_grammar.score("Fluffy loves Fluffy")                                                                  
Applying Inside algorithm...
Final Score:   0.024793388429752063
Out[]: 0.024793388429752063


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
                
        For any given line, that the first element (whitespace delimited element) is always
	the source of the rule in question.  
        The last element is always the probability of the transition from this source to the targets
        The aforementioned targests are exactly the zero or more elements between
        the first element and the last element of the line.
        So for example the line S .2 would mean a 0-ary rule with source S and targets (), 
        and that the conditional probability of this transition to () given S is .2.
        Note also that every symbol that appears in the middle but never on the
	left is assumed to be a Terminal


        file_type = "CNF_COUNTS" means the grammar to be learned is in Chomsky Normal Form and
        that the file contains lines of the form <count> <type> <args> where 
        <type> is "NONTERMINAL", "UNARYRULE", or "BINARYRULE"
        <args> are the corresponding one, two, or three Symbols, respectively.
        <count> is some given empirical count for this Symbol (for NONTERMINAL) 
        or for this  transformation (for *ARYRULE)
        Assumes all "NONTERMINAL" come first.

	file_type = "UNIV_COUNTS" means the file format consists of lines of the form

	N SOURCE TARGETS

	where N is some non-negative integer, SOURCE is (an identifier for) some
	source Variable or Non-terminal,
	and TARGETS is a list of zero or more (identifiers for) target symbols
	(either variables or terminals).
	The idea here is that N is the number of times the rule from this SOURCE and to
	these TARGETS appears
	in the semantic data (say a tree-bank) for our training corpus.

	Also note that, as with UNIV_PCFG format, we do not devote separate lines to
	listing the variables,
	and we do not list arities of the rule for the line. There is one and only one rule per line,
	and the arity can be read off as the length of TARGETS.
	And once again we make the simplifying assumptions that, while Non-terminals may appear
	as target symbols,
	a specific instance of a Non-terminal symbol in the semantic corpus data will
	always correspond to
	an instance of a rule where that occurence of the non-terminal is the Source.
	Thus, in order to make a count of the total number of occurrences of a Non-terminal,
	we only need to sum the counts for the rules with that Non-terminal as their source.

***

(3) An observation about file formats and training PCFGs:


Notice that any file that could hope to uniquely train a complete PCFG object must determine a file
in UNIV_PCFG format, and in this way UNIV_PCFG is a kind of universal receiver for training data
set representations.

In practice however, most data that we do obtain in UNIV_PCFG format will have come from some
sort of "counts file" at some point in its creation by way of MLE parameter estimates.

See derivation_example.txt for a simple example of how a counts file might be generated.  Whatever the details...at some point after we obtained a training corpus, since it is not enought to hae a raw training corpus

(1) a choice must be made about legal rules; we can call the subset of allowable rules
the *signature* of the PCFG (consider for instance the CNF restrictions).
But even with our signature selected,

(2) We need semantic (parse) information about the raw corpus sufficient to
record counts for all the rules in our signature.

In order to do (2), there are really only two options.

First, preferably, we obtain a manually annotated tree-bank of sentences in our corpus
(a special case being of course that our corpus was just the raw text from some tree-bank).
From this it should not be too hard to write a program that reads this treebank in its
local format and outputs a counts file.

The second alternative is to use yet another parser on our corpus to get sufficient
semantic information to write your counts file.
(It might be interesting to experiment with bootstrapping these parser objects or
generally treating them as weak learners for some ensemble method.)

***

(4) Coming soon / More Info:



Contact aetilley at gmail dot com.
