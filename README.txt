Probabilistic Context Free Grammar Scorer inspired by Yu Usami's PCFG parser (https://github.com/usami/pcfg).

Basic Usage:

>  from pcfg_scorer import PCFGScorer
>  scorer = PCFGScorer()
>  scorer.train("counts_file.txt")
>  scorer.score("I like water") #Note, no punctuation yet.
