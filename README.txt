Probabilistic Context Free Grammar parser/scorer object inspired by Yu Usami's PCFG parser (https://github.com/usami/pcfg).

Basic Usage:

>  from pcfg import PCFG
>  grammar = PCFG()
>  grammar.train_from_file("data/typed_counts_file_0.txt")
>  grammar.score("I cited her")
>  grammar.parse("I cited her")
