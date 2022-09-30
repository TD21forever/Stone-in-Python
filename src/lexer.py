from tkinter.messagebox import NO
from src.tokens import NumberToken,StringToken,IdentifyToken,Token
import string
import re

class Laxer:
    """词法分析器

    使用正则表达式抽取token: 依次为 注释,整形字面量,标识符,字符串
    """

    punct = string.punctuation
    punct = punct.replace('"', '')
    punct = punct.replace('/', '')

    number_token_pattern = "[0-9]+"
    identify_token_pattern = f"[A-Z_a-z][A-Z_a-z0-9]*|==|<=|>=|&&|\|\||[{punct}]"
    string_token_pattern = '"((\"|\\\\|\\n|[^\"])*)"'
    comment_pattern = r"//.*"
    token_pattern = f"\s*(({comment_pattern})|({number_token_pattern})|({identify_token_pattern})|{string_token_pattern})?"

    def __init__(self,source_code) -> None:
        self.__pattern = re.compile(self.token_pattern,re.M)
        self.__queue = []
        self.__cur_line = 0
        self.codes = source_code.split("\n")

    def peak(self,i):
        if self._fill_queue(i):
            return self.__queue[i]
        else:
            return Token.EOF

    def read(self):
        if self._fill_queue(0):
            return self.__queue.pop(0)
        else:
            return Token.EOF
    
    def _fill_queue(self,i):
        """i表示下标,指的是i+1个单词是否已经准备好
        """
        while i >= len(self.__queue):
            # 增加一个token
            if self._has_next_line():
                self._read_line()
            else:
                return False
        return True
            
    
    def _read_line(self):
        if self._has_next_line():
            code = self.codes[self.__cur_line]
            for match in self.__pattern.finditer(code):
                self._add_token(self.__cur_line,match)
            self.__cur_line += 1
        else:
            return 

    def _add_token(self,line,match):
        m = match.group(1)
        # 空格
        if m is None:
            return
        # 注释
        if match.group(2) is not None:
            return
        if match.group(3) is not None:
            token = NumberToken(line,int(m))
        elif match.group(4) is not None:
            token = IdentifyToken(line,str(m))
        else:
            token = StringToken(line,str(m))
        self.__queue.append(token)


    def _has_next_line(self):
        if self.__cur_line < len(self.codes):
            return True
        else:
            return False


if __name__ == "__main__":
    codes = """
        i = 10
        sum = 0
        while i > 0 {
            sum = sum + 1 // comment
            i = i - 1 
        }
    """

    laxer = Laxer(codes)
    token = laxer.read()
    while token != Token.EOF:
        print(token.get_line_number,token.get_text())
        token = laxer.read()