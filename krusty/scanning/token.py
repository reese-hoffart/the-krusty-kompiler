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

    # Other
    EOF = "EOF"

    def __str__(self) -> str:
        return self.value

    def __int__(self) -> int:
        return TokenType._member_names_.index(self.name)

class Token:
    def __init__(self, _type : TokenType = TokenType.UNKNOWN_TOKEN, _value : int = 0):
        # Attributes
        self.type : TokenType = _type
        self.value : int = _value
    
    def is_terminal(self) -> bool:
        if (self.type == TokenType.INTEGER_LITERAL or 
            self.type == TokenType.EOF):
            return True
        return False
    
    def matches_types(self, matches : list) -> bool:
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
