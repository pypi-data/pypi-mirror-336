import unittest
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sql.engine.kv import KVEngine
from sql.session import Session
from storage.memory import MemoryEngine
from storage.disk import DiskEngine
from sql.types.data_types import Value, DataType, Row
from sql.schema import TableSchema, ColumnSchema
from sql.parser.ast import Column, Expression, Consts
from error import InternalError
import tempfile


class TestSQLEngine(unittest.TestCase):
    """SQL引擎测试"""
    
    def setUp(self):
        """设置测试环境"""
        # 使用内存引擎
        self.storage_engine = MemoryEngine()
        self.kv_engine = KVEngine(self.storage_engine)
        self.transaction = self.kv_engine.begin()
    
    def test_create_table(self):
        """测试创建表"""
        # 创建一个表
        columns = [
            ColumnSchema("id", DataType.INTEGER, False),
            ColumnSchema("name", DataType.STRING, True),
            ColumnSchema("age", DataType.INTEGER, True),
        ]
        table = TableSchema("users", columns)
        
        # 创建表
        self.transaction.create_table(table)
        
        # 获取表
        retrieved_table = self.transaction.get_table("users")
        self.assertIsNotNone(retrieved_table)
        self.assertEqual(retrieved_table.name, "users")
        self.assertEqual(len(retrieved_table.columns), 3)
        
        # 验证列信息
        self.assertEqual(retrieved_table.columns[0].name, "id")
        self.assertEqual(retrieved_table.columns[0].datatype, DataType.INTEGER)
        self.assertEqual(retrieved_table.columns[0].nullable, False)
        
        self.assertEqual(retrieved_table.columns[1].name, "name")
        self.assertEqual(retrieved_table.columns[1].datatype, DataType.STRING)
        self.assertEqual(retrieved_table.columns[1].nullable, True)
        
        self.assertEqual(retrieved_table.columns[2].name, "age")
        self.assertEqual(retrieved_table.columns[2].datatype, DataType.INTEGER)
        self.assertEqual(retrieved_table.columns[2].nullable, True)
        
        # 测试创建重复表
        with self.assertRaises(InternalError):
            self.transaction.create_table(table)
    
    def test_create_row(self):
        """测试创建行"""
        # 创建一个表
        columns = [
            ColumnSchema("id", DataType.INTEGER, False),
            ColumnSchema("name", DataType.STRING, True),
            ColumnSchema("age", DataType.INTEGER, True),
        ]
        table = TableSchema("users", columns)
        self.transaction.create_table(table)
        
        # 创建一行数据
        row1 = [
            Value.integer(1),
            Value.string("Alice"),
            Value.integer(25)
        ]
        self.transaction.create_row("users", row1)
        
        # 创建另一行数据
        row2 = [
            Value.integer(2),
            Value.string("Bob"),
            Value.null()  # NULL值
        ]
        self.transaction.create_row("users", row2)
        
        # 创建违反NOT NULL约束的行
        row3 = [
            Value.null(),  # ID不能为NULL
            Value.string("Charlie"),
            Value.integer(30)
        ]
        with self.assertRaises(InternalError):
            self.transaction.create_row("users", row3)
        
        # 创建类型不匹配的行
        row4 = [
            Value.integer(4),
            Value.integer(123),  # 应该是字符串
            Value.integer(30)
        ]
        with self.assertRaises(InternalError):
            self.transaction.create_row("users", row4)
        
        # 列数不匹配
        row5 = [
            Value.integer(5),
            Value.string("Dave")
            # 缺少age列
        ]
        with self.assertRaises(InternalError):
            self.transaction.create_row("users", row5)
    
    def test_scan_table(self):
        """测试扫描表"""
        # 创建一个表
        columns = [
            ColumnSchema("id", DataType.INTEGER, False),
            ColumnSchema("name", DataType.STRING, True),
            ColumnSchema("age", DataType.INTEGER, True),
        ]
        table = TableSchema("users", columns)
        self.transaction.create_table(table)
        
        # 插入一些数据
        rows = [
            [Value.integer(1), Value.string("Alice"), Value.integer(25)],
            [Value.integer(2), Value.string("Bob"), Value.integer(30)],
            [Value.integer(3), Value.string("Charlie"), Value.null()]
        ]
        
        for row in rows:
            self.transaction.create_row("users", row)
        
        # 扫描表
        result = self.transaction.scan_table("users")
        
        # 验证结果
        self.assertEqual(len(result), 3)
        
        # 验证行ID顺序（按照键的顺序，可能与插入顺序不同）
        ids = [row[0].value for row in result]
        self.assertIn(1, ids)
        self.assertIn(2, ids)
        self.assertIn(3, ids)
        
        # 查找并验证每行的数据
        for row in result:
            if row[0].value == 1:
                self.assertEqual(row[1].value, "Alice")
                self.assertEqual(row[2].value, 25)
            elif row[0].value == 2:
                self.assertEqual(row[1].value, "Bob")
                self.assertEqual(row[2].value, 30)
            elif row[0].value == 3:
                self.assertEqual(row[1].value, "Charlie")
                self.assertIsNone(row[2].value)


class TestSQLSession(unittest.TestCase):
    """SQL会话测试"""
    
    def setUp(self):
        """设置测试环境"""
        # 使用内存引擎
        self.storage_engine = MemoryEngine()
        self.kv_engine = KVEngine(self.storage_engine)
        self.transaction = self.kv_engine.begin()
        self.session = Session(self.transaction)
    
    def test_create_table_statement(self):
        """测试CREATE TABLE语句执行"""
        sql = """
        CREATE TABLE test_table (
            id INTEGER NOT NULL,
            name STRING,
            age INTEGER,
            active BOOLEAN DEFAULT FALSE
        );
        """
        
        # 执行SQL
        self.session.execute(sql)
        
        # 验证表是否创建成功
        table = self.transaction.get_table("test_table")
        self.assertIsNotNone(table)
        self.assertEqual(table.name, "test_table")
        self.assertEqual(len(table.columns), 4)
        
        # 验证列信息
        self.assertEqual(table.columns[0].name, "id")
        self.assertEqual(table.columns[0].datatype, DataType.INTEGER)
        self.assertEqual(table.columns[0].nullable, False)
        
        self.assertEqual(table.columns[1].name, "name")
        self.assertEqual(table.columns[1].datatype, DataType.STRING)
        self.assertEqual(table.columns[1].nullable, True)  # 未指定NOT NULL约束，默认为True
        
        self.assertEqual(table.columns[2].name, "age")
        self.assertEqual(table.columns[2].datatype, DataType.INTEGER)
        self.assertEqual(table.columns[2].nullable, True)  # 未指定NOT NULL约束，默认为True
        
        self.assertEqual(table.columns[3].name, "active")
        self.assertEqual(table.columns[3].datatype, DataType.BOOLEAN)
        self.assertEqual(table.columns[3].nullable, True)  # 未指定NOT NULL约束，默认为True
    
    def test_insert_statement(self):
        """测试INSERT语句执行"""
        # 先创建表
        create_sql = """
        CREATE TABLE users (
            id INTEGER NOT NULL,
            name STRING,
            age INTEGER DEFAULT 18
        );
        """
        self.session.execute(create_sql)
        
        # 测试不指定列名的INSERT
        insert_sql1 = "INSERT INTO users VALUES (1, 'Alice', 25);"
        self.session.execute(insert_sql1)
        
        # 测试指定列名的INSERT
        insert_sql2 = "INSERT INTO users (id, name) VALUES (2, 'Bob');"
        self.session.execute(insert_sql2)
        
        # 验证数据
        rows = self.transaction.scan_table("users")
        self.assertEqual(len(rows), 2)
        
        # 找到并验证每行的数据
        for row in rows:
            if row[0].value == 1:
                self.assertEqual(row[1].value, "Alice")
                self.assertEqual(row[2].value, 25)
            elif row[0].value == 2:
                self.assertEqual(row[1].value, "Bob")
                self.assertEqual(row[2].value, 18)  # 使用默认值
    
    def test_select_statement(self):
        """测试SELECT语句执行"""
        # 先创建表并插入数据
        self.session.execute("CREATE TABLE users (id INTEGER NOT NULL, name STRING, age INTEGER);")
        self.session.execute("INSERT INTO users VALUES (1, 'Alice', 25);")
        self.session.execute("INSERT INTO users VALUES (2, 'Bob', 30);")
        
        # 执行SELECT
        result = self.session.execute("SELECT * FROM users;")
        
        # 验证结果
        self.assertEqual(len(result), 2)
        
        # 验证行内容
        ids = [row[0].value for row in result]
        self.assertIn(1, ids)
        self.assertIn(2, ids)
        
        for row in result:
            if row[0].value == 1:
                self.assertEqual(row[1].value, "Alice")
                self.assertEqual(row[2].value, 25)
            elif row[0].value == 2:
                self.assertEqual(row[1].value, "Bob")
                self.assertEqual(row[2].value, 30)
    
    def test_integrated_statements(self):
        """测试整合的SQL语句执行流程"""
        # 创建表
        self.session.execute("""
        CREATE TABLE employees (
            id INTEGER NOT NULL,
            name STRING,
            department STRING DEFAULT 'General',
            salary INTEGER DEFAULT 0
        );
        """)
        
        # 插入数据
        self.session.execute("INSERT INTO employees VALUES (1, 'Alice', 'Engineering', 5000);")
        self.session.execute("INSERT INTO employees (id, name, salary) VALUES (2, 'Bob', 6000);")
        self.session.execute("INSERT INTO employees (id, name, department) VALUES (3, 'Charlie', 'Marketing');")
        self.session.execute("INSERT INTO employees (id, name) VALUES (4, 'Dave');")
        
        # 查询数据
        result = self.session.execute("SELECT * FROM employees;")
        
        # 验证结果
        self.assertEqual(len(result), 4)
        
        # 验证行内容
        for row in result:
            if row[0].value == 1:
                self.assertEqual(row[1].value, "Alice")
                self.assertEqual(row[2].value, "Engineering")
                self.assertEqual(row[3].value, 5000)
            elif row[0].value == 2:
                self.assertEqual(row[1].value, "Bob")
                self.assertEqual(row[2].value, "General")  # 默认值
                self.assertEqual(row[3].value, 6000)
            elif row[0].value == 3:
                self.assertEqual(row[1].value, "Charlie")
                self.assertEqual(row[2].value, "Marketing")
                self.assertEqual(row[3].value, 0)  # 默认值
            elif row[0].value == 4:
                self.assertEqual(row[1].value, "Dave")
                self.assertEqual(row[2].value, "General")  # 默认值
                self.assertEqual(row[3].value, 0)  # 默认值


class TestSQLWithDiskEngine(unittest.TestCase):
    """使用磁盘引擎测试SQL功能"""
    
    def setUp(self):
        """设置测试环境"""
        # 创建临时文件作为存储引擎的数据文件
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        self.db_path = self.temp_file.name
        
        # 使用磁盘引擎
        self.storage_engine = DiskEngine(self.db_path)
        self.kv_engine = KVEngine(self.storage_engine)
        self.transaction = self.kv_engine.begin()
        self.session = Session(self.transaction)
    
    def tearDown(self):
        """清理测试环境"""
        # 确保事务已提交
        try:
            self.transaction.commit()
        except:
            pass
            
        # 删除临时文件
        if os.path.exists(self.db_path):
            try:
                os.unlink(self.db_path)
            except:
                pass
    
    def test_disk_persistence(self):
        """测试磁盘存储的持久性"""
        # 创建表并插入数据
        self.session.execute("CREATE TABLE users (id INTEGER NOT NULL, name STRING);")
        self.session.execute("INSERT INTO users VALUES (1, 'Alice');")
        self.session.execute("INSERT INTO users VALUES (2, 'Bob');")
        
        # 提交事务
        self.transaction.commit()
        
        # 创建新的引擎和会话
        storage_engine = DiskEngine(self.db_path)
        kv_engine = KVEngine(storage_engine)
        transaction = kv_engine.begin()
        session = Session(transaction)
        
        # 查询数据
        result = session.execute("SELECT * FROM users;")
        
        # 验证结果
        self.assertEqual(len(result), 2)
        
        # 验证行内容
        ids = [row[0].value for row in result]
        self.assertIn(1, ids)
        self.assertIn(2, ids)
        
        for row in result:
            if row[0].value == 1:
                self.assertEqual(row[1].value, "Alice")
            elif row[0].value == 2:
                self.assertEqual(row[1].value, "Bob")


if __name__ == "__main__":
    unittest.main() 