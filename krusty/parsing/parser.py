from ..krusty import GLOBAL_SCANNER
from ..krusty_ast import ASTNode
from ..scanning import Token, TokenType
from ..utils import KrustySyntaxError

class Parser:

    def __init__(self):
        # Attributes
        self.put_back_buffer : Token = None

    def create_ast(self) -> ASTNode:
        return self._parse_expr()
        
    def _parse_expr(self) -> ASTNode:
        return self._parse_addExpr()

    def _parse_addExpr(self) -> ASTNode:
        left : ASTNode
        right : ASTNode
        value : Token

        left = self._parse_mulExpr()

        if self._peek_next_token().matches_types([TokenType.PLUS, TokenType.MINUS]):
            value = self._consume_next_token()
            right = self._parse_addExpr()
            return ASTNode(value, left, right)

        return left

    def _parse_mulExpr(self) -> ASTNode:
        left : ASTNode
        right : ASTNode
        value : Token

        left = self._parse_terminal()

        if self._peek_next_token().matches_types([TokenType.STAR, TokenType.SLASH]):
            value = self._consume_next_token()
            right = self._parse_mulExpr()
            return ASTNode(value, left, right)

        return left

    def _parse_terminal(self) -> ASTNode:
        # Invalid Syntax Handling
        if not self._peek_next_token().matches_types([TokenType.INTEGER_LITERAL]):
            raise KrustySyntaxError(f'Expected terminal symbol but got {self._peek_next_token()}')
        
        return ASTNode(self._consume_next_token())

    # Scanner interface functions
    def _peek_next_token(self) -> Token:
        if(self.put_back_buffer):
            return self.put_back_buffer

        nextToken : Token = GLOBAL_SCANNER.scan_next()
        self.put_back_buffer = nextToken
        return nextToken
    
    def _consume_next_token(self) -> Token:
        if(self.put_back_buffer):
            tokenToReturn : Token = self.put_back_buffer
            self.put_back_buffer = None
            return tokenToReturn
        
        return GLOBAL_SCANNER.scan_next()
