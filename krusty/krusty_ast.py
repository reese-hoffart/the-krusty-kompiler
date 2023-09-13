from .scanning import Token
from copy import deepcopy

class ASTNode:
    def __init__(self, value : Token, left = None, right = None, parent = None):
        # Attributes
        self.token : Token = deepcopy(value)
        self.left : ASTNode = left
        self.right : ASTNode = right
        self.parent : ASTNode = parent

        if left:
            self.left.parent = self
        if right:
            self.right.parent = self
    
    def __str__(self) -> str:
        outStr : str = ""
        level : int = 0
        def preorder(self):
            nonlocal level, outStr
            for _ in range(level):
                outStr += "| "
            outStr += f"{self.token}\n"

            level += 1
            if self.left:
                preorder(self.left)
            if self.right:
                preorder(self.right)
            level -= 1
        
        preorder(self)
        return outStr