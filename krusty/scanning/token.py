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

    def __str__(self) -> str:
        return self.value

    def __int__(self) -> int:
        return TokenType._member_names_.index(self.name)

class Token:
    type : TokenType
    value : int

    def __init__(self, _type : TokenType = TokenType.UNKNOWN_TOKEN, _value : int = 1):
        self.type = _type
        self.value = _value

    def __repr__(self):
        return f"Token:\n\tTYPE = [{str(self.type)}] ({int(self.type)})" + (
            f"\n\tVALUE = {self.value}"
            if self.type == TokenType.INTEGER_LITERAL
            else ""
        )