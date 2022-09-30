from src.errors import StoneException

class Token:
    


    def __init__(self,line) -> None:
        self.__line_number = line
    
    @property
    def get_line_number(self):
        return self.__line_number

    @property 
    def is_identifier(self):
        return False

    @property
    def is_number(self):
        return False

    @property
    def is_string(self):
        return False

    def get_text(self):
        return NotImplementedError
    
    def get_number(self):
        raise NotImplementedError


class NumberToken(Token):
    def __init__(self, line,val) -> None:
        super().__init__(line)
        self.val = val

    @property
    def is_number(self):
        return True
    
    def get_number(self):
        return self.val
    
    def get_text(self):
        return str(self.val)

class IdentifyToken(Token):
    def __init__(self, line, id_) -> None:
        super().__init__(line)
        self.text = id_
    
    @property
    def is_identifier(self):
        return True
    
    def get_number(self):
        raise StoneException("Not number token Error")
    
    def get_text(self):
        return self.text

class StringToken(Token):
    def __init__(self, line, string) -> None:
        super().__init__(line)
        self.literal = string
    
    @property
    def is_string(self):
        return True
    
    def get_number(self):
        raise StoneException("Not number token Error")

    def get_text(self): 
        return self.literal

        
        
    
Token.EOF = Token(-1)
Token.EOL = "\n"