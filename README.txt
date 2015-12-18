Probabilistic Context Free Grammar parser/scorer object inspired by Yu Usami's PCFG parser (https://github.com/usami/pcfg).

Basic Usage:

>  from pcfg import PCFG
>  grammar = PCFG()
>  grammar.train("counts_file.txt")
>  grammar.score("I cited her")
>  grammar.parse("I cited her")
