from sys import breakpointhook
import pdbcolor

from pygments import highlight
from pygments.formatters import TerminalFormatter
from pdbcolor import PdbLexer


def myfunc():
    x = 1
    y = 2
    print(x + y)


if __name__ == "__main__":
    # This is main.py
    bug = pdbcolor.PdbColor()
    # lexer = PdbLexer()
    # for i in lexer.get_tokens("(Pdb)"):
    #     print(i)

    pdb_lexer = PdbLexer()
    formatter = TerminalFormatter
    breakpoint()
    prompt = highlight("(Pdb)", pdb_lexer, formatter).rstrip() + " "
