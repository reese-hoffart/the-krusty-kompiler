from enum import Enum

class TokenType(Enum):

    UNKNOWN_TOKEN = "unknown token"

    # Operators
    PLUS = "+"
    MINUS = "-"
    STAR = "*"
    SLASH = "/"

    # Literals
    INTEGER_LITERAL = "integer literal"

    # Keywords
    PRINT = "print"

    # Other
    SEMNICOLON = ";"
    EOF = "EOF"

    @staticmethod
    def from_string(string : str) -> "TokenType":
        for type in TokenType:
            if str(type) == string:
                return type
        return TokenType.UNKNOWN_TOKEN

    def __str__(self) -> str:
        return self.value

    def __int__(self) -> int:
        return TokenType._member_names_.index(self.name)

class Token:
    def __init__(self, _type : TokenType = TokenType.UNKNOWN_TOKEN, _value : int = 0):
        # Attributes
        self.type : TokenType = _type
        self.value : int = _value
        self.registerOfPtr : int = None # used for llvm generation
        self.registerLoadedIn : int = None # used for llvm generation
    
    def is_terminal(self) -> bool:
        if (self.type == TokenType.INTEGER_LITERAL or 
            self.type == TokenType.EOF):
            return True
        return False

    def is_operator(self) -> bool:
        if (self.type == TokenType.PLUS or self.type == TokenType.MINUS or
            self.type == TokenType.STAR or self.type == TokenType.SLASH):
            return True
        return False

    def is_literal(self) -> bool:
        if (self.type == TokenType.INTEGER_LITERAL):
            return True
        return False
    
    def matches_types(self, matches : list[TokenType]) -> bool:
        for tokenType in matches:
            if tokenType == self.type:
                return True
        return False

    def __repr__(self) -> str:
        return f"Token({str(self.type)}" + (
            f", {self.value})"
            if self.type == TokenType.INTEGER_LITERAL
            else ")"
        )
