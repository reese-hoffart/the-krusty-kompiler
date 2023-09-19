from typing import TextIO
from ..utils import KrustyFileError
from ..scanning import Token, TokenType
from ..krusty import ARGS
from ..krusty_ast import ASTNode

class Generator:
    def __init__(self, filename : str, ast : ASTNode):
        # Attributes
        self.LLVM_FILE : TextIO
        self.AST : ASTNode = ast
        self.registerCount = 0

        try:
            self.LLVM_FILE = open(filename, "w")
        except Exception as e:
            raise KrustyFileError(str(e))
    
    def close(self):
        self.LLVM_FILE.close()

    def generate_llvm(self):
        self.LLVM_FILE.write(self._llvm_preamble())
        self.LLVM_FILE.write(self._llvm_alloca_and_store())

        self.LLVM_FILE.write(self._llvm_from_ast())

        self.LLVM_FILE.write(self._llvm_postamble())
                
    def _llvm_from_ast(self) -> str:
        llvm_code : str = ""
        def postorder(ast : ASTNode):
            nonlocal llvm_code, self

            if ast.left:
                postorder(ast.left)
            if ast.right:
                postorder(ast.right)

            leftVal : ASTNode = ast.left
            rightVal : ASTNode = ast.right
            
            if ast.token.is_operator():
                # load registers
                llvm_code += self._llvm_load_into_register(leftVal)
                llvm_code += self._llvm_load_into_register(rightVal)

                # generate llvm
                operator : Token = ast.token
                operatorCmd : str
                if operator.type == TokenType.PLUS:
                    operatorCmd = "add nsw"
                elif operator.type == TokenType.MINUS:
                    operatorCmd = "sub nsw"
                elif operator.type == TokenType.STAR:
                    operatorCmd = "mul nsw"
                elif operator.type == TokenType.SLASH:
                    operatorCmd = "udiv"
                else:
                    raise TypeError(f"An operator of unknown type was encountered when generating LLVM from AST: {ast.token}")
                operator.registerLoadedIn = self._increment_register_count()
                llvm_code += f"\t%{operator.registerLoadedIn} = {operatorCmd} {self._get_llvm_type(leftVal)} {leftVal.token.registerLoadedIn}, {rightVal.token.registerLoadedIn}\n"
        
        postorder(self.AST)
        llvm_code += f"\tcall i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @print_int_fstring , i32 0, i32 0), i32 %{self.registerCount-1})\n"
        return llvm_code

    def _increment_register_count(self) -> int:
        # Increment registerCount attribute & return the number that should be used for a new register
        self.registerCount += 1
        return self.registerCount

    def _get_llvm_type(self, astNode : ASTNode) -> str:
        typeMap : dict[TokenType, str] = {
            TokenType.INTEGER_LITERAL: "i32"
        }

        if astNode.token.type in typeMap:
            return typeMap[astNode.token.type]
        elif astNode.left:
            return self._get_llvm_type(astNode.left)
        else:
            raise TypeError(f"A literal of unknown type was encountered when converting to llvm type: {astNode.token}")

    # LLVM Snippit Functions
    def _llvm_preamble(self) -> str:
        return f"""
; ModuleID = '{ARGS.PROGRAM}'
source_filename = "{ARGS.PROGRAM}"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

@print_int_fstring = private unnamed_addr constant [4 x i8] c"%d\\0A\\00", align 1

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @main() #0 {{
"""

    def _llvm_alloca_and_store(self) -> str:
        llvm_code : str = ""

        def postorder(astNode : ASTNode):
            nonlocal llvm_code, self

            if astNode.left:
                postorder(astNode.left)
            if astNode.right:
                postorder(astNode.right)
            token : Token = astNode.token
            nextRegNum = self._increment_register_count()
            token.registerOfPtr = nextRegNum
            llvm_code += f"\t%{nextRegNum} = alloca {self._get_llvm_type(astNode)}, align 4\n"
            llvm_code += f"\tstore {self._get_llvm_type(astNode)} {token.value}, {self._get_llvm_type(astNode)}* %{nextRegNum}, align 4\n"
        
        postorder(self.AST)
        return llvm_code

    def _llvm_load_into_register(self, astNodeToLoad : ASTNode) -> str:
        llvm_code : str = ""
        if not astNodeToLoad.token.registerLoadedIn:
            register : int = self._increment_register_count()
            astNodeToLoad.token.registerLoadedIn = register
            llvm_code += f"\t%{astNodeToLoad.token.registerLoadedIn} = load {self._get_llvm_type(astNodeToLoad)}, {self._get_llvm_type(astNodeToLoad)}* %{astNodeToLoad.token.registerOfPtr}, align 4\n"
        return llvm_code

    def _llvm_postamble(self) -> str:
        return """
    ret i32 0
}

declare i32 @printf(i8*, ...) #1
attributes #0 = { noinline nounwind optnone uwtable "frame-pointer"="all" "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { "frame-pointer"="all" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
!llvm.module.flags = !{!0, !1, !2, !3, !4}
!llvm.ident = !{!5}
!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{i32 7, !"PIC Level", i32 2}
!2 = !{i32 7, !"PIE Level", i32 2}
!3 = !{i32 7, !"uwtable", i32 1}
!4 = !{i32 7, !"frame-pointer", i32 2}
!5 = !{!"Ubuntu clang version 10.0.0-4ubuntu1"}
"""
