import unittest
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sql.parser import Parser
from sql.parser.ast import Statement, Expression, Consts
from sql.types.data_types import DataType
from error import ParseError


class TestParser(unittest.TestCase):
    """SQL解析器测试"""
    
    def test_create_table(self):
        """测试CREATE TABLE语句解析"""
        sql = """
        CREATE TABLE users (
            id INTEGER NOT NULL,
            name STRING,
            age INTEGER DEFAULT 18,
            active BOOLEAN DEFAULT TRUE
        );
        """
        
        parser = Parser(sql)
        stmt = parser.parse()
        
        # 验证语句类型
        self.assertEqual(stmt.stmt_type, 'create_table')
        self.assertEqual(stmt.name, 'users')
        
        # 验证列定义
        self.assertEqual(len(stmt.columns), 4)
        
        # id列
        col_id = stmt.columns[0]
        self.assertEqual(col_id.name, 'id')
        self.assertEqual(col_id.datatype, DataType.INTEGER)
        self.assertEqual(col_id.nullable, False)
        
        # name列
        col_name = stmt.columns[1]
        self.assertEqual(col_name.name, 'name')
        self.assertEqual(col_name.datatype, DataType.STRING)
        self.assertIsNone(col_name.nullable)
        
        # age列
        col_age = stmt.columns[2]
        self.assertEqual(col_age.name, 'age')
        self.assertEqual(col_age.datatype, DataType.INTEGER)
        self.assertIsNone(col_age.nullable)
        self.assertIsNotNone(col_age.default)
        self.assertEqual(col_age.default.value.const_type, 'integer')
        self.assertEqual(col_age.default.value.value, 18)
        
        # active列
        col_active = stmt.columns[3]
        self.assertEqual(col_active.name, 'active')
        self.assertEqual(col_active.datatype, DataType.BOOLEAN)
        self.assertIsNone(col_active.nullable)
        self.assertIsNotNone(col_active.default)
        self.assertEqual(col_active.default.value.const_type, 'boolean')
        self.assertEqual(col_active.default.value.value, True)
    
    def test_insert(self):
        """测试INSERT语句解析"""
        # 测试不带列名的插入
        sql1 = "INSERT INTO users VALUES (1, 'Alice'), (2, 'Bob');"
        
        parser = Parser(sql1)
        stmt = parser.parse()
        
        # 验证语句类型
        self.assertEqual(stmt.stmt_type, 'insert')
        self.assertEqual(stmt.table_name, 'users')
        self.assertIsNone(stmt.columns)
        
        # 验证值
        self.assertEqual(len(stmt.values), 2)
        
        # 第一行
        row1 = stmt.values[0]
        self.assertEqual(len(row1), 2)
        self.assertEqual(row1[0].value.const_type, 'integer')
        self.assertEqual(row1[0].value.value, 1)
        self.assertEqual(row1[1].value.const_type, 'string')
        self.assertEqual(row1[1].value.value, 'Alice')
        
        # 第二行
        row2 = stmt.values[1]
        self.assertEqual(len(row2), 2)
        self.assertEqual(row2[0].value.const_type, 'integer')
        self.assertEqual(row2[0].value.value, 2)
        self.assertEqual(row2[1].value.const_type, 'string')
        self.assertEqual(row2[1].value.value, 'Bob')
        
        # 测试带列名的插入
        sql2 = "INSERT INTO users (id, name) VALUES (3, 'Charlie');"
        
        parser = Parser(sql2)
        stmt = parser.parse()
        
        # 验证语句类型
        self.assertEqual(stmt.stmt_type, 'insert')
        self.assertEqual(stmt.table_name, 'users')
        self.assertEqual(stmt.columns, ['id', 'name'])
        
        # 验证值
        self.assertEqual(len(stmt.values), 1)
        row = stmt.values[0]
        self.assertEqual(len(row), 2)
        self.assertEqual(row[0].value.const_type, 'integer')
        self.assertEqual(row[0].value.value, 3)
        self.assertEqual(row[1].value.const_type, 'string')
        self.assertEqual(row[1].value.value, 'Charlie')
    
    def test_select(self):
        """测试SELECT语句解析"""
        sql = "SELECT * FROM users;"
        
        parser = Parser(sql)
        stmt = parser.parse()
        
        # 验证语句类型
        self.assertEqual(stmt.stmt_type, 'select')
        self.assertEqual(stmt.table_name, 'users')
    
    def test_parse_error(self):
        """测试解析错误"""
        # 语法错误
        sql1 = "SELECT FROM users;"
        parser = Parser(sql1)
        with self.assertRaises(ParseError):
            parser.parse()
        
        # 未结束的语句
        sql2 = "SELECT * FROM users"
        parser = Parser(sql2)
        with self.assertRaises(ParseError):
            parser.parse()
        
        # 不支持的语法特性（例如子查询）
        sql3 = "SELECT * FROM (SELECT * FROM users);"
        parser = Parser(sql3)
        with self.assertRaises(ParseError):
            parser.parse()


if __name__ == "__main__":
    unittest.main()