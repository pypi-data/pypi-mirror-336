from typing import List, Optional, Any, Dict
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from error import ParseError
from sql.types.data_types import DataType
from sql.parser.lexer import Lexer, Token, Keyword
from sql.parser.ast import Statement, Column, Expression, Consts, Condition


class Parser:
    """SQL解析器"""
    
    def __init__(self, input_sql: str):
        """
        初始化解析器
        
        Args:
            input_sql: SQL语句文本
        """
        self.lexer = Lexer(input_sql)
        self.tokens = self.lexer.tokenize()
        self.position = 0
    
    def parse(self) -> Statement:
        """
        解析SQL语句，获取抽象语法树
        
        Returns:
            SQL语句的抽象语法树表示
            
        Raises:
            ParseError: 解析错误
        """
        stmt = self._parse_statement()
        
        # 期望SQL语句的最后有个分号
        self._next_expect(Token.semicolon())
        
        # 分号之后不能有其他的符号
        if self.position < len(self.tokens):
            token = self.tokens[self.position]
            raise ParseError(f"[Parser] Unexpected token {token}")
            
        return stmt
    
    def _parse_statement(self) -> Statement:
        """解析SQL语句"""
        # 查看第一个Token类型
        token = self._peek()
        if token is None:
            raise ParseError("[Parser] Unexpected end of input")
            
        if token.token_type == 'keyword':
            if token.value == Keyword.CREATE:
                return self._parse_ddl()
            elif token.value == Keyword.SELECT:
                return self._parse_select()
            elif token.value == Keyword.INSERT:
                return self._parse_insert()
            elif token.value == Keyword.UPDATE:
                return self._parse_update()
            elif token.value == Keyword.DELETE:
                return self._parse_delete()
                
        raise ParseError(f"[Parser] Unexpected token {token}")
    
    def _parse_ddl(self) -> Statement:
        """解析DDL语句"""
        token = self._next()
        if token.token_type != 'keyword' or token.value != Keyword.CREATE:
            raise ParseError(f"[Parser] Expected CREATE, got {token}")
            
        token = self._next()
        if token.token_type != 'keyword' or token.value != Keyword.TABLE:
            raise ParseError(f"[Parser] Expected TABLE, got {token}")
            
        return self._parse_create_table()
    
    def _parse_create_table(self) -> Statement:
        """解析CREATE TABLE语句"""
        # 表名
        table_name = self._next_ident()
        
        # 左括号
        self._next_expect(Token.open_paren())
        
        # 解析列定义
        columns = []
        while True:
            columns.append(self._parse_column())
            
            # 如果下一个token不是逗号，则结束列定义
            if not self._next_if_token(Token.comma()):
                break
        
        # 右括号
        self._next_expect(Token.close_paren())
        
        return Statement.create_table(table_name, columns)
    
    def _parse_column(self) -> Column:
        """解析列定义"""
        # 列名
        column_name = self._next_ident()
        
        # 数据类型
        token = self._next()
        if token.token_type != 'keyword':
            raise ParseError(f"[Parser] Expected data type, got {token}")
            
        data_type = None
        if token.value in (Keyword.INT, Keyword.INTEGER):
            data_type = DataType.INTEGER
        elif token.value in (Keyword.BOOL, Keyword.BOOLEAN):
            data_type = DataType.BOOLEAN
        elif token.value in (Keyword.FLOAT, Keyword.DOUBLE):
            data_type = DataType.FLOAT
        elif token.value in (Keyword.STRING, Keyword.TEXT, Keyword.VARCHAR):
            data_type = DataType.STRING
        else:
            raise ParseError(f"[Parser] Unexpected data type {token}")
            
        column = Column(column_name, data_type)
        
        # 解析列约束
        while True:
            token = self._peek()
            if token is None or token.token_type != 'keyword':
                break
                
            if token.value == Keyword.NULL:
                self._next()  # 消费NULL
                column.nullable = True
            elif token.value == Keyword.NOT:
                self._next()  # 消费NOT
                self._next_expect(Token.keyword(Keyword.NULL))
                column.nullable = False
            elif token.value == Keyword.DEFAULT:
                self._next()  # 消费DEFAULT
                column.default = self._parse_expression()
            else:
                break
        
        return column
    
    def _parse_select(self) -> Statement:
        """解析SELECT语句"""
        # SELECT
        self._next_expect(Token.keyword(Keyword.SELECT))
        
        # *
        self._next_expect(Token.asterisk())
        
        # FROM
        self._next_expect(Token.keyword(Keyword.FROM))
        
        # 表名
        table_name = self._next_ident()
        
        # 解析WHERE子句（可选）
        where_condition = None
        if self._next_if_token(Token.keyword(Keyword.WHERE)):
            where_condition = self._parse_condition()
        
        return Statement.select(table_name, where_condition)
    
    def _parse_insert(self) -> Statement:
        """解析INSERT语句"""
        # INSERT
        self._next_expect(Token.keyword(Keyword.INSERT))
        
        # INTO
        self._next_expect(Token.keyword(Keyword.INTO))
        
        # 表名
        table_name = self._next_ident()
        
        # 列名（可选）
        columns = None
        if self._next_if_token(Token.open_paren()):
            columns = []
            while True:
                columns.append(self._next_ident())
                
                # 如果下一个token不是逗号，则结束列名列表
                if not self._next_if_token(Token.comma()):
                    break
            
            self._next_expect(Token.close_paren())
        
        # VALUES
        self._next_expect(Token.keyword(Keyword.VALUES))
        
        # 值列表
        values = []
        while True:
            self._next_expect(Token.open_paren())
            
            row_values = []
            while True:
                row_values.append(self._parse_expression())
                
                # 如果下一个token不是逗号，则结束值列表
                if not self._next_if_token(Token.comma()):
                    break
            
            self._next_expect(Token.close_paren())
            values.append(row_values)
            
            # 如果下一个token不是逗号，则结束插入值列表
            if not self._next_if_token(Token.comma()):
                break
        
        return Statement.insert(table_name, columns, values)
    
    def _parse_update(self) -> Statement:
        """解析UPDATE语句"""
        # UPDATE
        self._next_expect(Token.keyword(Keyword.UPDATE))
        
        # 表名
        table_name = self._next_ident()
        
        # SET
        self._next_expect(Token.keyword(Keyword.SET))
        
        # 更新的列和值
        updates = {}
        while True:
            # 列名
            col_name = self._next_ident()
            
            # 等号
            self._next_expect(Token.equals())
            
            # 值表达式
            expr = self._parse_expression()
            
            # 添加到更新列表
            updates[col_name] = expr
            
            # 如果下一个token不是逗号，则结束更新列表
            if not self._next_if_token(Token.comma()):
                break
        
        # 解析WHERE子句（可选）
        where_condition = None
        if self._next_if_token(Token.keyword(Keyword.WHERE)):
            where_condition = self._parse_condition()
        
        return Statement.update(table_name, updates, where_condition)
    
    def _parse_delete(self) -> Statement:
        """解析DELETE语句"""
        # DELETE
        self._next_expect(Token.keyword(Keyword.DELETE))
        
        # FROM
        self._next_expect(Token.keyword(Keyword.FROM))
        
        # 表名
        table_name = self._next_ident()
        
        # 解析WHERE子句（可选）
        where_condition = None
        if self._next_if_token(Token.keyword(Keyword.WHERE)):
            where_condition = self._parse_condition()
        
        return Statement.delete(table_name, where_condition)
    
    def _parse_condition(self) -> Condition:
        """解析条件表达式"""
        # 解析第一个条件
        left_condition = self._parse_basic_condition()
        
        # 检查是否有AND/OR操作符
        token = self._peek()
        if token is None or token.token_type != 'keyword':
            return left_condition
        
        if token.value == Keyword.AND:
            self._next()  # 消费AND
            right_condition = self._parse_condition()
            return Condition.and_op(left_condition, right_condition)
        elif token.value == Keyword.OR:
            self._next()  # 消费OR
            right_condition = self._parse_condition()
            return Condition.or_op(left_condition, right_condition)
        
        return left_condition
    
    def _parse_basic_condition(self) -> Condition:
        """解析基本条件"""
        token = self._peek()
        
        # 如果是开括号，表示是一个括号包围的复杂条件
        if token.token_type == 'open_paren':
            self._next()  # 消费开括号
            condition = self._parse_condition()  # 解析括号内的条件
            self._next_expect(Token.close_paren())  # 期望闭括号
            return condition
            
        # 列名
        column = self._next_ident()
        
        # 比较操作符
        token = self._next()
        if token.token_type == 'operator':
            op = token.value
        elif token.token_type == 'equals':
            op = '='
        else:
            raise ParseError(f"[Parser] Expected comparison operator, got {token}")
        
        # 值表达式
        expr = self._parse_expression()
        
        # 根据操作符创建条件
        if op == '=':
            return Condition.equals(column, expr)
        elif op == '!=':
            return Condition.not_equals(column, expr)
        elif op == '>':
            return Condition.gt(column, expr)
        elif op == '>=':
            return Condition.gte(column, expr)
        elif op == '<':
            return Condition.lt(column, expr)
        elif op == '<=':
            return Condition.lte(column, expr)
        else:
            raise ParseError(f"[Parser] Unsupported comparison operator: {op}")
    
    def _parse_expression(self) -> Expression:
        """解析表达式"""
        token = self._next()
        
        # NULL
        if token.token_type == 'keyword' and token.value == Keyword.NULL:
            return Expression.consts(Consts.null())
        
        # TRUE/FALSE
        if token.token_type == 'keyword':
            if token.value == Keyword.TRUE:
                return Expression.consts(Consts.boolean(True))
            elif token.value == Keyword.FALSE:
                return Expression.consts(Consts.boolean(False))
        
        # 整数
        if token.token_type == 'integer':
            return Expression.consts(Consts.integer(token.value))
        
        # 浮点数
        if token.token_type == 'float':
            return Expression.consts(Consts.float(token.value))
        
        # 字符串
        if token.token_type == 'string':
            return Expression.consts(Consts.string(token.value))
        
        raise ParseError(f"[Parser] Unexpected token in expression: {token}")
    
    def _peek(self) -> Optional[Token]:
        """获取下一个Token但不消费它"""
        if self.position >= len(self.tokens):
            return None
        return self.tokens[self.position]
    
    def _next(self) -> Token:
        """获取并消费下一个Token"""
        if self.position >= len(self.tokens):
            raise ParseError("[Parser] Unexpected end of input")
        token = self.tokens[self.position]
        self.position += 1
        return token
    
    def _next_ident(self) -> str:
        """获取并消费下一个标识符Token"""
        token = self._next()
        if token.token_type != 'ident':
            raise ParseError(f"[Parser] Expected identifier, got {token}")
        return token.value
    
    def _next_expect(self, expected: Token):
        """获取并消费下一个Token，并检查它是否是期望的Token"""
        token = self._next()
        if token != expected:
            raise ParseError(f"[Parser] Expected {expected}, got {token}")
    
    def _next_if_token(self, expected: Token) -> bool:
        """如果下一个Token是期望的Token，则消费它并返回True；否则，不消费并返回False"""
        token = self._peek()
        if token is None:
            return False
        if token == expected:
            self._next()
            return True
        return False