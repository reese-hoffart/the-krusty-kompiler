from typing import TextIO, List
import os

from .token import Token, TokenType
from ..utils.logging import KrustyFileNotFound, KrustySyntaxError

class Scanner:
    filename : str
    file : TextIO
    currentLine : int = 1

    putBackBuffer : str = ""

    def __init__(self, filename):
        self.filename = filename

        if os.path.exists(filename):
            self.file = open(self.filename, "r")
        else:
            raise KrustyFileNotFound(filename)
    
    def close(self):
        self.file.close()

    def next_character(self) -> str:
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
    
    def next_character_skip_whitespace(self) -> str:
        nextChar : str = self.next_character()
        while nextChar.isspace():
            nextChar = self.next_character()
        return nextChar
    
    def put_back(self, c : str):
        if len(c) != 1:
            raise TypeError(f"put_back() expected a character, but string of length {len(c)} found")
        self.putBackBuffer = c
    
    def scan_integer_literal(self, currentChar : str) -> int:
        intAsString = ""

        while currentChar.isdigit():
            intAsString += currentChar
            currentChar = self.next_character()
        
        self.put_back(currentChar)
        
        return int(intAsString)
    
    def scan_all(self):
        currentChar : str

        while True:
            currentChar = self.next_character_skip_whitespace()

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
                    print(Token(TokenType.INTEGER_LITERAL, self.scan_integer_literal(currentChar)))
                else:
                    raise KrustySyntaxError(f'Unrecognized token "{currentChar}"')
