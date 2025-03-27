import unittest
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sql.session import Session
from sql.engine.kv import KVEngine
from storage.memory import MemoryEngine
from error import InternalError


class TestCRUD(unittest.TestCase):
    """CRUD操作集成测试"""
    
    def setUp(self):
        """测试前初始化环境"""
        # 创建一个内存引擎的会话
        self.storage_engine = MemoryEngine()
        self.kv_engine = KVEngine(self.storage_engine)
        self.transaction = self.kv_engine.begin()
        self.session = Session(self.transaction)
        
        # 创建测试表
        self.session.execute("""
        CREATE TABLE test_users (
            id INTEGER NOT NULL,
            name STRING,
            age INTEGER DEFAULT 18,
            salary FLOAT,
            is_active BOOLEAN DEFAULT TRUE
        );
        """)
        
        # 提交创建表，然后开始新事务
        self.transaction.commit()
        self.transaction = self.kv_engine.begin()
        self.session = Session(self.transaction)
    
    def test_insert_and_select(self):
        """测试插入和查询操作"""
        # 插入数据
        self.session.execute("INSERT INTO test_users VALUES (1, 'Alice', 25, 3000.0, TRUE);")
        self.session.execute("INSERT INTO test_users VALUES (2, 'Bob', 30, 3500.0, TRUE);")
        self.session.execute("INSERT INTO test_users (id, name, salary) VALUES (3, 'Charlie', 4000.0);")
        
        # 查询全表数据
        results = self.session.execute("SELECT * FROM test_users;")
        
        # 验证结果
        self.assertEqual(len(results), 3)
        
        # 验证第一行
        self.assertEqual(results[0][0].value, 1)
        self.assertEqual(results[0][1].value, 'Alice')
        self.assertEqual(results[0][2].value, 25)
        self.assertEqual(results[0][3].value, 3000.0)
        self.assertEqual(results[0][4].value, True)
        
        # 验证第三行（使用默认值的行）
        self.assertEqual(results[2][0].value, 3)
        self.assertEqual(results[2][1].value, 'Charlie')
        self.assertEqual(results[2][2].value, 18)  # 默认值
        self.assertEqual(results[2][3].value, 4000.0)
        self.assertEqual(results[2][4].value, True)  # 默认值
    
    def test_update(self):
        """测试更新操作"""
        # 插入数据
        self.session.execute("INSERT INTO test_users VALUES (1, 'Alice', 25, 3000.0, TRUE);")
        self.session.execute("INSERT INTO test_users VALUES (2, 'Bob', 30, 3500.0, TRUE);")
        self.session.execute("INSERT INTO test_users VALUES (3, 'Charlie', 35, 4000.0, TRUE);")
        
        # 更新单条数据
        self.session.execute("UPDATE test_users SET salary = 5000.0 WHERE id = 1;")
        
        # 验证更新结果
        results = self.session.execute("SELECT * FROM test_users WHERE id = 1;")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][3].value, 5000.0)
        
        # 更新多条数据
        self.session.execute("UPDATE test_users SET is_active = FALSE WHERE age > 25;")
        
        # 验证批量更新结果
        results = self.session.execute("SELECT * FROM test_users;")
        active_users = [row for row in results if row[4].value]
        inactive_users = [row for row in results if not row[4].value]
        
        self.assertEqual(len(active_users), 1)  # 只有Alice还是active
        self.assertEqual(len(inactive_users), 2)  # Bob和Charlie变成了inactive
        
        # 更新多个字段
        self.session.execute("UPDATE test_users SET name = 'David', age = 40 WHERE id = 3;")
        
        # 验证多字段更新结果
        results = self.session.execute("SELECT * FROM test_users WHERE id = 3;")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][1].value, 'David')
        self.assertEqual(results[0][2].value, 40)
    
    def test_delete(self):
        """测试删除操作"""
        # 插入数据
        self.session.execute("INSERT INTO test_users VALUES (1, 'Alice', 25, 3000.0, TRUE);")
        self.session.execute("INSERT INTO test_users VALUES (2, 'Bob', 30, 3500.0, FALSE);")
        self.session.execute("INSERT INTO test_users VALUES (3, 'Charlie', 35, 4000.0, TRUE);")
        self.session.execute("INSERT INTO test_users VALUES (4, 'David', 40, 4500.0, FALSE);")
        
        # 删除单条数据
        self.session.execute("DELETE FROM test_users WHERE id = 1;")
        
        # 验证删除结果
        results = self.session.execute("SELECT * FROM test_users;")
        self.assertEqual(len(results), 3)
        ids = [row[0].value for row in results]
        self.assertNotIn(1, ids)
        
        # 条件删除
        self.session.execute("DELETE FROM test_users WHERE is_active = FALSE;")
        
        # 验证条件删除结果
        results = self.session.execute("SELECT * FROM test_users;")
        self.assertEqual(len(results), 1)  # 只剩下Charlie
        self.assertEqual(results[0][0].value, 3)
        self.assertEqual(results[0][1].value, 'Charlie')
        
        # 删除所有数据
        self.session.execute("DELETE FROM test_users;")
        
        # 验证全表删除结果
        results = self.session.execute("SELECT * FROM test_users;")
        self.assertEqual(len(results), 0)
    
    def test_complex_conditions(self):
        """测试复杂条件查询"""
        # 插入数据
        self.session.execute("INSERT INTO test_users VALUES (1, 'Alice', 25, 3000.0, TRUE);")
        self.session.execute("INSERT INTO test_users VALUES (2, 'Bob', 30, 3500.0, TRUE);")
        self.session.execute("INSERT INTO test_users VALUES (3, 'Charlie', 35, 4000.0, FALSE);")
        self.session.execute("INSERT INTO test_users VALUES (4, 'David', 40, 4500.0, FALSE);")
        self.session.execute("INSERT INTO test_users VALUES (5, 'Eve', 28, 5000.0, TRUE);")
        
        # AND条件
        results = self.session.execute("SELECT * FROM test_users WHERE age > 25 AND is_active = TRUE;")
        self.assertEqual(len(results), 2)  # Bob和Eve
        
        # OR条件
        results = self.session.execute("SELECT * FROM test_users WHERE id = 1 OR salary > 4000.0;")
        self.assertEqual(len(results), 3)  # Alice, David和Eve
        
        # 复合条件 - 先测试简单形式，不用括号
        results = self.session.execute("SELECT * FROM test_users WHERE age > 35 AND is_active = FALSE;")
        self.assertEqual(len(results), 1)  # David
    
    def test_error_handling(self):
        """测试错误处理"""
        # 表不存在
        with self.assertRaises(InternalError):
            self.session.execute("SELECT * FROM non_existent_table;")
        
        # 列不存在
        with self.assertRaises(InternalError):
            self.session.execute("INSERT INTO test_users (id, non_existent_column) VALUES (5, 'value');")
        
        # 类型不匹配
        with self.assertRaises(InternalError):
            self.session.execute("INSERT INTO test_users VALUES ('not_a_number', 'name', 25, 3000.0, TRUE);")
        
        # SQL语法错误
        with self.assertRaises(Exception):  # 可能是ParseError或InternalError
            self.session.execute("SELECT * FORM test_users;")  # FORM是故意拼写错误
            
    def tearDown(self):
        """测试后清理"""
        try:
            self.transaction.commit()  # 确保事务被提交
        except:
            self.transaction.rollback()  # 如果提交失败则回滚


if __name__ == "__main__":
    unittest.main()