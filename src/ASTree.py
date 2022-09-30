from typing import Iterator
from src.tokens import Token


class ASTree:
    
    def __init__(self) -> None:
        ...

    def num_children(self):
        raise NotImplementedError

    def children(self):
        raise NotImplementedError
    
    def location(self):
        raise NotImplementedError
    
    def child(self,i):
        raise NotImplementedError
    
class ASTLeaf(ASTree):

    __empty = []

    def __init__(self,token:Token) -> None:
        super().__init__()
        self._token = token

    def child(self,i):
        raise IndexError
    
    def num_children(self):
        return 0

    def location(self):
        return "at line " + self._token.get_line_number()

    def children(self):
        return iter(self.__empty)
    
    @property
    def token(self):
        return self._token
    
    def __str__(self) -> str:
        return self._token.get_text()


class ASTList(ASTree):

    def __init__(self,AST_list) -> None:
        super().__init__()
        self._children = AST_list
    
    def child(self, i):
        return self._children[i]
    
    def num_children(self):
        return len(self._children)
    
    def children(self):
        return iter(self._children)
    
    def __str__(self) -> str:
        res = "("
        for child in self._children:
            res += str(child)
            res += " "
        res += ")"
        return res

    def location(self):
        ...

    
class NumberLiteral(ASTLeaf):

    def __init__(self, token: Token) -> None:
        super().__init__(token)
    
    @property
    def value(self):
        return self.token.get_number()

class Name(ASTLeaf):

    def __init__(self, token: Token) -> None:
        super().__init__(token)
    
    @property
    def name(self):
        return self.token.get_text()
    

class BinaryExpr(ASTList):

    def __init__(self) -> None:
        super().__init__()
    
    def left(self):
        return self.child(0)
    
    def right(self):
        return self.child(2)

    def operator(self):
        return self.child(1).token().get_text()    


    
    

    
    