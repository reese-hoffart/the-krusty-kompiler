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

    ast : ASTNode = parser.create_ast()
    print(ast)
    
    generator : Generator = Generator(ARGS.output, ast)
    generator.generate_llvm()

    # def interpret_ast(root: ASTNode) -> int:
    #     left_value: int
    #     right_value: int

    #     if root.left:
    #         left_value = interpret_ast(root.left)
    #     if root.right:
    #         right_value = interpret_ast(root.right)

    #     if root.token.type == TokenType.PLUS:
    #         return left_value + right_value
    #     elif root.token.type == TokenType.MINUS:
    #         return left_value - right_value
    #     elif root.token.type == TokenType.STAR:
    #         return left_value * right_value
    #     elif root.token.type == TokenType.SLASH:
    #         return left_value // right_value
    #     elif root.token.type == TokenType.INTEGER_LITERAL:
    #         return root.token.value
    #     else:
    #         raise KrustyFatalException(
    #             "FATAL", f'Unknown Token "{str(root.token.type)}" encountered'
    #         )

    # print(interpret_ast(ast))

    generator.close()
    GLOBAL_SCANNER.close()
    
if __name__ == "__main__":
    main()