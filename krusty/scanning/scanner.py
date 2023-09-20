from typing import TextIO, List
import os

from .token import Token, TokenType
from ..utils.logging import KrustyFileNotFound, KrustySyntaxError, KrustyIdentifierError

class Scanner:
    MAX_TOKEN_LENGTH : int = 512

    def __init__(self, filename):
        # Attributes
        self.filename = filename
        self.file : TextIO
        self.currentLine : int = 1
        self.putBackBuffer : str = ""

        if os.path.exists(filename):
            self.file = open(self.filename, "r")
        else:
            raise KrustyFileNotFound(filename)
    
    def close(self):
        self.file.close()

    def _next_character(self) -> str:
        nextChar : str = ""

        # check put back buffer first
        if(self.putBackBuffer):
            nextChar = self.putBackBuffer
            self.putBackBuffer = ""
            return nextChar
        
        nextChar = self.file.read(1)
        if(nextChar == "\n"):
            self.currentLine += 1
        
        return nextChar
    
    def _next_character_skip_whitespace(self) -> str:
        nextChar : str = self._next_character()
        while nextChar.isspace():
            nextChar = self._next_character()
        return nextChar
    
    def _put_back(self, c : str):
        if len(c) != 1:
            raise TypeError(f"put_back() expected a character, but string of length {len(c)} found")
        self.putBackBuffer = c
    
    def _scan_integer_literal(self, currentChar : str) -> int:
        intAsString = ""

        while currentChar.isdigit():
            intAsString += currentChar
            currentChar = self._next_character()
        
        self._put_back(currentChar)
        
        return int(intAsString)
    
    def _scan_identifier(self, currentChar : str) -> str:
        identifier : str = ""

        while currentChar.isalnum() or currentChar == "_":
            identifier += currentChar
            currentChar = self._next_character()
            
            if len(identifier) > self.MAX_TOKEN_LENGTH:
                raise KrustyIdentifierError(f"Identifier exceeded limit of {self.MAX_TOKEN_LENGTH} characters.")
        
        self._put_back(currentChar)
        return identifier
    
    def scan_next(self) -> Token:
        currentChar : str = self._next_character_skip_whitespace()

        if currentChar == "":
            # EOF reached
            return Token(TokenType.EOF)
        elif [str(x) for x in TokenType].count(currentChar) > 0:
            return Token(TokenType.from_string(currentChar))
        elif currentChar.isalpha() or currentChar == "_":
            # Is identifier or token
            identifier : str = self._scan_identifier(currentChar)
            for tokenType in TokenType:
                if str(tokenType) == identifier:
                    return Token(tokenType)
            raise KrustySyntaxError(f"Unrecognized identifier \"{currentChar}\"")
        elif currentChar.isdigit():
            # Is integer literal
            return Token(TokenType.INTEGER_LITERAL, self._scan_integer_literal(currentChar))
        else:
            raise KrustySyntaxError(f"Unrecognized token \"{currentChar}\"")
                    
    def scan_all(self):
        currentChar : str

        while True:
            currentChar = self._next_character_skip_whitespace()

            # EOF reached
            if(currentChar == ""):
                return
            
            # Check if character is token (only supports one-character tokens)
            charIsToken : bool = False
            for tokenType in TokenType:
                if currentChar == str(tokenType):
                    charIsToken = True
                    print(Token(tokenType))
            
            if not charIsToken:
                if currentChar.isdigit():
                    print(Token(TokenType.INTEGER_LITERAL, self._scan_integer_literal(currentChar)))
                else:
                    raise KrustySyntaxError(f'Unrecognized token "{currentChar}"')
