from .scanning import Scanner, TokenType
from .utils import get_args, setup_tracebacks, KrustyFatalException
from .krusty_ast import ASTNode

DEBUG = True
GLOBAL_SCANNER : Scanner

def main():
    global GLOBAL_SCANNER
    args = get_args()
    setup_tracebacks()

    GLOBAL_SCANNER = Scanner(args.PROGRAM)
    from .parsing import Parser
    parser : Parser = Parser()

    ast : ASTNode = parser.create_ast()
    print(ast)

    def interpret_ast(root: ASTNode) -> int:
        left_value: int
        right_value: int

        if root.left:
            left_value = interpret_ast(root.left)
        if root.right:
            right_value = interpret_ast(root.right)

        if root.token.type == TokenType.PLUS:
            return left_value + right_value
        elif root.token.type == TokenType.MINUS:
            return left_value - right_value
        elif root.token.type == TokenType.STAR:
            return left_value * right_value
        elif root.token.type == TokenType.SLASH:
            return left_value // right_value
        elif root.token.type == TokenType.INTEGER_LITERAL:
            return root.token.value
        else:
            raise KrustyFatalException(
                "FATAL", f'Unknown Token "{str(root.token.type)}" encountered'
            )

    print(interpret_ast(ast))


    GLOBAL_SCANNER.close()
    
if __name__ == "__main__":
    main()