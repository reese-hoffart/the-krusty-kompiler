from argparse import Namespace
from .scanning import Scanner, TokenType
from .utils import get_args, setup_tracebacks, KrustyFatalException
from .krusty_ast import ASTNode

DEBUG = True
GLOBAL_SCANNER : Scanner
ARGS : Namespace

def main():
    global GLOBAL_SCANNER, ARGS
    ARGS = get_args()
    setup_tracebacks()

    GLOBAL_SCANNER = Scanner(ARGS.PROGRAM)
    from .parsing import Parser
    from .generation import Generator
    parser : Parser = Parser()

    generator : Generator = Generator(ARGS.output)
    generator.generate_llvm(parser)

    generator.close()
    GLOBAL_SCANNER.close()
    
if __name__ == "__main__":
    main()