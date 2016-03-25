
(1) Basic Usage
(2) File Types understood by self.train_from_file()
(3) A note on file types and training PCFGs.

(*) Coming Soon / More info

***

(1) Basic Usage:

>  from src.pcfg import PCFG

>  grammar = PCFG()
Input data has wrong signature
Valid CFG?:  False

> grammar.train_from_file("data/toy_univ_tree.txt", file_type="UNIV_TREE")
Training complete.  Running self-check...
Valid CFG?:   True
Valid Parameters?:   True
CNF?:   True

> grammar.check_PCFG()
Valid CFG?: True
Valid Parameters?: True
Out: True

> grammar.check_CNF()
CNF?:  True
Out: True

> grammar.score("Fluffy loves Fluffy")
Applying Inside algorithm...
Final Score:   0.024793388429752063
Out: 0.024793388429752063

> tree = grammar.parse("Fluffy loves Fluffy")                                                     
Applying CKY algorithm...

> tree.label
Out: 'S'

> len(tree.children)
Out: 2

> tree.to_expr()
Out: '(S (NP Fluffy) (VP (VT loves) (NP Fluffy)))'
 
> grammar.write_pcfg("data/toy_univ_pcfg.txt")

> grammar.parse_file("data/toy_raw.txt", "data/toy_univ_tree.txt")
Applying CKY algorithm...
Applying CKY algorithm...
Applying CKY algorithm...
Applying CKY algorithm...
Applying CKY algorithm...
Applying CKY algorithm...

> other_grammar = PCFG()
Input data has wrong signature
Valid CFG?:   False

> other_grammar.train_from_file("data/univ_pcfg_0.txt", file_type = "UNIV_PCFG")
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
Not CNF: the arity  3 is non-empty
Not CNF:  The unary rule NN (NP,)  has as target NP
Not CNF:  There are binary rules with targets that are not Variables
CNF?:   False
Out: False

> other_grammar.score("thomas greets sally")
This PCFG is not in Chomsky Normal Form. Cannot apply inside algorithm.

> other_grammar.make_CNF()
This process will change the underlying symbol sets and rule sets of the PCFG. 
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

> other_tree = other_grammar.parse("thomas greets sally")                                        
Applying CKY algorithm...

> other_tree.label
Out: 'S'

> other_tree.terminal
Out: False

> len(other_tree.children)
Out: 2

> other_tree.to_expr()
Out: '(S (NP thomas) (VP (VT greets) (NP sally)))'

> other_grammar.score("thomas greets the milkman")
Applying Inside algorithm...
Final Score:   0.0033711220057212757
Out: 0.0033711220057212757

> another_tree = other_grammar.parse("thomas greets the milkman")                                
Applying CKY algorithm...

> another_tree.to_expr()
Out: '(S (NP thomas) (VP (VT greets) (NP (DET the) (U-milkman milkman))))'

> len(another_tree.children)
Out: 2

> another_tree.children[1].to_expr()
Out: '(VP (VT greets) (NP (DET the) (U-milkman milkman)))'

> g1 = PCFG()
Input data has wrong signature
Valid CFG?:   False

> g2 = PCFG()
Input data has wrong signature
Valid CFG?:   False

> g3 = PCFG()
Input data has wrong signature
Valid CFG?:   False

> g1.train_from_file("data/toy_univ_pcfg.txt", file_type = "UNIV_PCFG")                          
Training complete.  Running self-check...
Valid CFG?:   True
Valid Parameters?:   True
CNF?:   True

> g2.train_from_file("data/toy_univ_counts.txt", file_type = "UNIV_COUNTS")                  
Training complete.  Running self-check...
Valid CFG?:   True
Valid Parameters?:   True
CNF?:   True

> g3.train_from_file("data/toy_univ_tree.txt", file_type = "UNIV_TREE")
Training complete.  Running self-check...
Valid CFG?:   True
Valid Parameters?:   True
CNF?:   True

> g1 == g2
Out: True

> g2 == g3
Out: True

...

***



(2) File Types understood by self.train_from_file:

(i) UNIV_PCFG
(ii) UNIV_COUNTS
(iii) UNIV_TREE

(i) UNIV_PCFG

uses the assumptions that, in any description of a PCFG:
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

For any given line, that the first element (whitespace delimited element) is
always the (identifier for the) source of the rule in question.  
The last element is always a floating point literal for the probability of the transition
from this source to the targets
The aforementioned (indentifiers for the) target Symbols are exactly the zero or more symbols between
the first element and the last element of the line.
Notice in particular the line S .2 would refer to a 0-ary rule with source S and targets (),
(the empty target list) and indicate that the conditional probability of this transition
to () given S is .2.
Note also that every symbol that appears in the middle but never on the left can be assumed
to be a Terminal.


(ii) UNIV_COUNTS

format consists of lines of the form

N SOURCE TARGETS

where N is some non-negative integer, SOURCE is (an identifier for) some
source Variable or Non-terminal,
and TARGETS is a list of zero or more (identifiers for) target symbols
(either variables or terminals).
The idea here is that N is the number of times the rule from this SOURCE and to
these TARGETS appears
in the semantic data (say a tree-bank) for our training corpus.

Also note that, as with UNIV_PCFG format, we do not devote separate lines to
listing the variables, and we do not list arities of the rule for the line.
There is one and only one rule per line,
and the arity can be read off as the length of TARGETS. And once again we make the
simplifying assumptions that, while Non-terminals may appear as target symbols, a specific
instance of a Non-terminal symbol in the semantic corpus data will always correspond to
an instance of a rule where that occurence of the non-terminal is the Source.
Thus, in order to make a count of the total number of occurrences of a Non-terminal,
we only need to sum the counts for the rules with that Non-terminal as their source.

(iii) UNIV_TREE

To define UNIV_TREE format, we first define what a tree-expression is
 a tree-expression is any character string that follows the recursive definition

(i) And lone (identifier for a) Terminal

<terminal>

is a tree-expression (of depth zero), and in addition

(ii) Given N a non-negative integer (possibly zero), and given N tree-expressions
<tree1>, <tree2>, ... , <treeN>, of depths d1, d2, ..., dN,
and given <symbol> a (identifier for a) Variable symbol, the character string

(<symbol> <tree1> <tree2> ... <treeN>)

is a tree-expression (of depth 1 + max{d1, d2, ..., dN})

where we take max{} = 0 so that the tree-expression (S) has depth 1, as does, say,
(S Damn) if Damn is in our set of Terminals.

Finally, we say a file is in UNIV_TREE format, if every line consists of exactly one
tree-expression of positive depth.


***

(3) An observation about file formats and training PCFGs:


Notice that any file that could hope to uniquely train a complete PCFG object must determine a file
in UNIV_PCFG format, and in this way UNIV_PCFG is a kind of universal receiver for training data
set representations.

In practice however, most data that we do obtain in UNIV_PCFG format will have come from some
sort of "counts file" at some point in its creation by way of MLE parameter estimates.

See derivation_example.txt for a simple example of how a counts file might be generated.
Whatever the details...at some point after we obtained a training corpus,
since it is not enought to have a raw training corpus

(1) a choice must be made about legal rules; we can call the subset of allowable rules
the *signature* of the PCFG (consider for instance the CNF restrictions).
But even with our signature selected,

(2) We need semantic (parse) information about the raw corpus sufficient to
record counts for all the rules in our signature.

In order to do (2), there are really only two options.

First, preferably, we obtain a manually annotated tree-bank of sentences in our corpus
(a special case being of course that our corpus was just the raw text from some tree-bank).
From this it should not be too hard to write a program that reads this treebank in its
local format and outputs a counts file or another tree-bank (see UNIV_COUNTS and UNIV_TREE formats).

The second alternative is to use yet another parser on our corpus to get sufficient
semantic information to write your counts file.
(It might be interesting to experiment with boosting PCFG objects or
more generally treating them as weak learners for some ensemble method.)

***


(*) Coming soon / More Info / To Do:

self.parse() should output in UNIV_TREE format.



(contact aetilley at gmail dot com)
