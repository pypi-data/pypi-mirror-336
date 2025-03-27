from enum import Enum
from typing import Optional, Iterator, List, Tuple
import re
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from error import ParseError


class Keyword(Enum):
    """SQL关键字"""
    CREATE = 'CREATE'
    TABLE = 'TABLE'
    INT = 'INT'
    INTEGER = 'INTEGER'
    BOOLEAN = 'BOOLEAN'
    BOOL = 'BOOL'
    STRING = 'STRING'
    TEXT = 'TEXT'
    VARCHAR = 'VARCHAR'
    FLOAT = 'FLOAT'
    DOUBLE = 'DOUBLE'
    SELECT = 'SELECT'
    FROM = 'FROM'
    INSERT = 'INSERT'
    INTO = 'INTO'
    VALUES = 'VALUES'
    TRUE = 'TRUE'
    FALSE = 'FALSE'
    DEFAULT = 'DEFAULT'
    NOT = 'NOT'
    NULL = 'NULL'
    PRIMARY = 'PRIMARY'
    KEY = 'KEY'
    UPDATE = 'UPDATE'
    SET = 'SET'
    DELETE = 'DELETE'
    WHERE = 'WHERE'
    AND = 'AND'
    OR = 'OR'
    
    @classmethod
    def from_str(cls, ident: str) -> Optional['Keyword']:
        """从字符串获取关键字"""
        try:
            return cls(ident.upper())
        except ValueError:
            return None
            
    def __str__(self):
        return self.value


class Token:
    """词法分析中的token定义"""
    def __init__(self, token_type: str, value=None):
        self.token_type = token_type
        self.value = value
    
    @classmethod
    def keyword(cls, keyword: Keyword):
        """关键字Token"""
        return cls('keyword', keyword)
    
    @classmethod
    def ident(cls, ident: str):
        """标识符Token"""
        return cls('ident', ident)
    
    @classmethod
    def string(cls, string: str):
        """字符串Token"""
        return cls('string', string)
    
    @classmethod
    def integer(cls, int_val: int):
        """整数Token"""
        return cls('integer', int_val)
    
    @classmethod
    def float(cls, float_val: float):
        """浮点数Token"""
        return cls('float', float_val)
    
    @classmethod
    def open_paren(cls):
        """左括号Token"""
        return cls('open_paren')
    
    @classmethod
    def close_paren(cls):
        """右括号Token"""
        return cls('close_paren')
    
    @classmethod
    def comma(cls):
        """逗号Token"""
        return cls('comma')
    
    @classmethod
    def semicolon(cls):
        """分号Token"""
        return cls('semicolon')
    
    @classmethod
    def asterisk(cls):
        """星号Token"""
        return cls('asterisk')
    
    @classmethod
    def plus(cls):
        """加号Token"""
        return cls('plus')
    
    @classmethod
    def minus(cls):
        """减号Token"""
        return cls('minus')
    
    @classmethod
    def slash(cls):
        """斜杠Token"""
        return cls('slash')
    
    @classmethod
    def equals(cls):
        """等号Token"""
        return cls('equals')
    
    @classmethod
    def operator(cls, op: str):
        """运算符Token"""
        return cls('operator', op)
    
    def __eq__(self, other):
        if not isinstance(other, Token):
            return False
        if self.token_type != other.token_type:
            return False
        return self.value == other.value
    
    def __repr__(self):
        if self.token_type == 'keyword':
            return f"Token.keyword({self.value!r})"
        elif self.token_type == 'ident':
            return f"Token.ident({self.value!r})"
        elif self.token_type == 'string':
            return f"Token.string({self.value!r})"
        elif self.token_type == 'integer':
            return f"Token.integer({self.value!r})"
        elif self.token_type == 'float':
            return f"Token.float({self.value!r})"
        elif self.token_type == 'operator':
            return f"Token.operator({self.value!r})"
        return f"Token.{self.token_type}()"
    
    def __str__(self):
        if self.token_type == 'keyword':
            return str(self.value)
        elif self.token_type in ('ident', 'string', 'integer', 'float', 'operator'):
            return str(self.value)
        elif self.token_type == 'open_paren':
            return '('
        elif self.token_type == 'close_paren':
            return ')'
        elif self.token_type == 'comma':
            return ','
        elif self.token_type == 'semicolon':
            return ';'
        elif self.token_type == 'asterisk':
            return '*'
        elif self.token_type == 'plus':
            return '+'
        elif self.token_type == 'minus':
            return '-'
        elif self.token_type == 'slash':
            return '/'
        elif self.token_type == 'equals':
            return '='
        return self.token_type


class Lexer:
    """
    SQL词法分析器
    
    支持的SQL语法:

    1. Create Table
    --------------------------------------
    CREATE TABLE table_name (
        [ column_name data_type [ column_constraint [...] ] ]
        [, ... ]
    );

    where data_type is:
     - BOOLEAN(BOOL): true | false
     - FLOAT(DOUBLE)
     - INTEGER(INT)
     - STRING(TEXT, VARCHAR)

    where column_constraint is:
    [ NOT NULL | NULL | DEFAULT expr ]

    2. Insert Into
    --------------------------------------
    INSERT INTO table_name
    [ ( column_name [, ...] ) ]
    values ( expr [, ...] );

    3. Select * From
    --------------------------------------
    SELECT * FROM table_name;

    4. Update
    --------------------------------------
    UPDATE table_name
    SET column_name = expr [, ...]
    [ WHERE condition ];

    5. Delete
    --------------------------------------
    DELETE FROM table_name
    [ WHERE condition ];
    """
    
    def __init__(self, sql_text: str):
        """
        初始化词法分析器
        
        Args:
            sql_text: SQL语句文本
        """
        self.sql_text = sql_text
        self.position = 0
    
    def tokenize(self) -> List[Token]:
        """
        解析SQL文本为token序列
        
        Returns:
            token序列
        """
        tokens = []
        while self.position < len(self.sql_text):
            token = self.scan_token()
            if token:
                tokens.append(token)
        return tokens
    
    def scan_token(self) -> Optional[Token]:
        """
        扫描一个token
        
        Returns:
            token，如果没有则返回None
        """
        # 跳过空白字符
        self._skip_whitespace()
        
        # 如果已经扫描到末尾，则返回None
        if self.position >= len(self.sql_text):
            return None
        
        # 获取当前字符
        char = self.sql_text[self.position]
        
        # 扫描字符串字面量
        if char in ("'", '"'):
            return self._scan_string()
        
        # 扫描数字字面量
        if char.isdigit() or (char == '.' and 
                             self.position + 1 < len(self.sql_text) and 
                             self.sql_text[self.position + 1].isdigit()):
            return self._scan_number()
        
        # 扫描标识符或关键字
        if char.isalpha() or char == '_':
            return self._scan_identifier()
        
        # 扫描符号
        return self._scan_symbol()
    
    def _skip_whitespace(self):
        """跳过空白字符"""
        while self.position < len(self.sql_text) and self.sql_text[self.position].isspace():
            self.position += 1
    
    def _scan_string(self) -> Token:
        """
        扫描字符串字面量
        
        Returns:
            字符串token
        """
        # 记录起始位置
        start = self.position
        
        # 获取引号类型
        quote = self.sql_text[start]
        self.position += 1
        
        # 处理字符串内容
        string_value = ''
        escape = False
        
        while self.position < len(self.sql_text):
            char = self.sql_text[self.position]
            
            if escape:
                if char == 'n':
                    string_value += '\n'
                elif char == 't':
                    string_value += '\t'
                elif char == '\\':
                    string_value += '\\'
                elif char == "'":
                    string_value += "'"
                elif char == '"':
                    string_value += '"'
                else:
                    string_value += char
                    
                escape = False
            elif char == '\\':
                escape = True
            elif char == quote:
                self.position += 1
                return Token.string(string_value)
            else:
                string_value += char
                
            self.position += 1
        
        # 如果到达这里，说明字符串没有结束
        raise ParseError(f"[Lexer] Unterminated string literal at position {start}")
    
    def _scan_number(self) -> Token:
        """
        扫描数字字面量
        
        Returns:
            数字token
        """
        # 记录起始位置
        start = self.position
        
        # 处理整数部分
        while self.position < len(self.sql_text) and self.sql_text[self.position].isdigit():
            self.position += 1
        
        # 检查是否是浮点数
        if self.position < len(self.sql_text) and self.sql_text[self.position] == '.':
            self.position += 1
            
            # 处理小数部分
            while self.position < len(self.sql_text) and self.sql_text[self.position].isdigit():
                self.position += 1
            
            # 浮点数
            value = float(self.sql_text[start:self.position])
            return Token.float(value)
        
        # 整数
        value = int(self.sql_text[start:self.position])
        return Token.integer(value)
    
    def _scan_identifier(self) -> Token:
        """
        扫描标识符
        
        Returns:
            标识符token或关键字token
        """
        # 记录起始位置
        start = self.position
        
        # 处理标识符
        while self.position < len(self.sql_text) and (
                self.sql_text[self.position].isalnum() or 
                self.sql_text[self.position] == '_'):
            self.position += 1
        
        # 获取标识符
        ident = self.sql_text[start:self.position]
        
        # 检查是否是关键字
        keyword = Keyword.from_str(ident)
        if keyword is not None:
            return Token.keyword(keyword)
        
        # 返回标识符
        return Token.ident(ident)
    
    def _scan_symbol(self) -> Optional[Token]:
        """
        扫描符号
        
        Returns:
            符号token
        """
        char = self.sql_text[self.position]
        self.position += 1
        
        # 常见符号
        if char == '(':
            return Token.open_paren()
        elif char == ')':
            return Token.close_paren()
        elif char == ',':
            return Token.comma()
        elif char == ';':
            return Token.semicolon()
        elif char == '*':
            return Token.asterisk()
        elif char == '+':
            return Token.plus()
        elif char == '-':
            return Token.minus()
        elif char == '/':
            return Token.slash()
        elif char == '=':
            return Token.equals()
        
        # 多字符运算符
        if char == '!' and self.position < len(self.sql_text) and self.sql_text[self.position] == '=':
            self.position += 1
            return Token.operator('!=')
        elif char == '<':
            if self.position < len(self.sql_text) and self.sql_text[self.position] == '=':
                self.position += 1
                return Token.operator('<=')
            return Token.operator('<')
        elif char == '>':
            if self.position < len(self.sql_text) and self.sql_text[self.position] == '=':
                self.position += 1
                return Token.operator('>=')
            return Token.operator('>')
        
        # 未知字符
        raise ParseError(f"[Lexer] Unexpected character: {char} at position {self.position - 1}")