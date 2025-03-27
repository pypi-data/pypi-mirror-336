import unittest
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sql.parser.lexer import Lexer, Token, Keyword
from error import ParseError


class TestLexer(unittest.TestCase):
    """SQL词法分析器测试"""
    
    def test_create_table_tokens(self):
        """测试CREATE TABLE语句的词法分析"""
        sql = """
        CREATE TABLE users (
            id INTEGER NOT NULL,
            name STRING,
            age INTEGER DEFAULT 18,
            active BOOLEAN DEFAULT FALSE
        );
        """
        
        lexer = Lexer(sql)
        tokens = lexer.tokenize()
        print("tokens: ", tokens)
        # 验证词法分析结果
        expected = [
            Token.keyword(Keyword.CREATE),
            Token.keyword(Keyword.TABLE),
            Token.ident('users'),
            Token.open_paren(),
            Token.ident('id'),
            Token.keyword(Keyword.INTEGER),
            Token.keyword(Keyword.NOT),
            Token.keyword(Keyword.NULL),
            Token.comma(),
            Token.ident('name'),
            Token.keyword(Keyword.STRING),
            Token.comma(),
            Token.ident('age'),
            Token.keyword(Keyword.INTEGER),
            Token.keyword(Keyword.DEFAULT),
            Token.integer(18),
            Token.comma(),
            Token.ident('active'),
            Token.keyword(Keyword.BOOLEAN),
            Token.keyword(Keyword.DEFAULT),
            Token.keyword(Keyword.FALSE),
            Token.close_paren(),
            Token.semicolon()
        ]
        
        self.assertEqual(len(tokens), len(expected))
        for i, (actual, expected_token) in enumerate(zip(tokens, expected)):
            self.assertEqual(actual, expected_token, f"Token at position {i} does not match")
    
    def test_insert_tokens(self):
        """测试INSERT语句的词法分析"""
        sql = "INSERT INTO users VALUES (1, 'Alice'), (2, 'Bob');"
        
        lexer = Lexer(sql)
        tokens = lexer.tokenize()
        
        # 验证词法分析结果
        expected = [
            Token.keyword(Keyword.INSERT),
            Token.keyword(Keyword.INTO),
            Token.ident('users'),
            Token.keyword(Keyword.VALUES),
            Token.open_paren(),
            Token.integer(1),
            Token.comma(),
            Token.string('Alice'),
            Token.close_paren(),
            Token.comma(),
            Token.open_paren(),
            Token.integer(2),
            Token.comma(),
            Token.string('Bob'),
            Token.close_paren(),
            Token.semicolon()
        ]
        
        self.assertEqual(len(tokens), len(expected))
        for i, (actual, expected_token) in enumerate(zip(tokens, expected)):
            self.assertEqual(actual, expected_token, f"Token at position {i} does not match")
    
    def test_select_tokens(self):
        """测试SELECT语句的词法分析"""
        sql = "SELECT * FROM users;"
        
        lexer = Lexer(sql)
        tokens = lexer.tokenize()
        
        # 验证词法分析结果
        expected = [
            Token.keyword(Keyword.SELECT),
            Token.asterisk(),
            Token.keyword(Keyword.FROM),
            Token.ident('users'),
            Token.semicolon()
        ]
        
        self.assertEqual(len(tokens), len(expected))
        for i, (actual, expected_token) in enumerate(zip(tokens, expected)):
            self.assertEqual(actual, expected_token, f"Token at position {i} does not match")
    
    def test_error_handling(self):
        """测试错误处理"""
        # 未闭合的字符串
        sql = "SELECT * FROM users WHERE name = 'unclosed;"
        
        lexer = Lexer(sql)
        with self.assertRaises(ParseError):
            lexer.tokenize()


if __name__ == "__main__":
    unittest.main()