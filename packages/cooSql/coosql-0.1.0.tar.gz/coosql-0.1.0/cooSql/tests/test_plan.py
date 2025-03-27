import unittest
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from sql.parser import Parser
from sql.parser.ast import Expression, Consts
from sql.plan import Plan, CreateTableNode, InsertNode, ScanNode, UpdateNode, DeleteNode
from sql.schema import TableSchema


class TestPlan(unittest.TestCase):
    """计划模块测试"""
    
    def test_plan_create_table(self):
        """测试创建表计划"""
        # 测试标准的CREATE TABLE语句
        sql1 = """
        CREATE TABLE tbl1 (
            a INTEGER DEFAULT 100,
            b FLOAT NOT NULL,
            c STRING NULL,
            d BOOLEAN DEFAULT TRUE
        );
        """
        stmt1 = Parser(sql1).parse()
        p1 = Plan.build(stmt1)
        
        # 测试格式不同但语义相同的语句
        sql2 = """
        CREATE            TABLE tbl1 (
            a INTEGER DEFAULT     100,
            b FLOAT NOT NULL     ,
            c STRING      NULL,
            d       BOOLEAN DEFAULT        TRUE
        );
        """
        stmt2 = Parser(sql2).parse()
        p2 = Plan.build(stmt2)
        
        # 确保两个计划生成的是相同的表结构
        self.assertEqual(p1.node.schema.name, p2.node.schema.name)
        self.assertEqual(len(p1.node.schema.columns), len(p2.node.schema.columns))
        
        for i in range(len(p1.node.schema.columns)):
            col1 = p1.node.schema.columns[i]
            col2 = p2.node.schema.columns[i]
            self.assertEqual(col1.name, col2.name)
            self.assertEqual(col1.datatype, col2.datatype)
            self.assertEqual(col1.nullable, col2.nullable)
            if col1.default is not None and col2.default is not None:
                self.assertEqual(col1.default.value, col2.default.value)
            else:
                self.assertEqual(col1.default, col2.default)
    
    def test_plan_insert(self):
        """测试插入计划"""
        # 测试不指定列名的插入
        sql1 = "INSERT INTO tbl1 VALUES (1, 2, 3, 'a', TRUE);"
        stmt1 = Parser(sql1).parse()
        p1 = Plan.build(stmt1)
        
        self.assertIsInstance(p1.node, InsertNode)
        self.assertEqual(p1.node.table_name, "tbl1")
        self.assertEqual(p1.node.columns, [])
        self.assertEqual(len(p1.node.values), 1)
        self.assertEqual(len(p1.node.values[0]), 5)
        
        # 验证插入的值
        values1 = p1.node.values[0]
        self.assertEqual(values1[0].expr_type, 'consts')
        self.assertEqual(values1[0].value.const_type, 'integer')
        self.assertEqual(values1[0].value.value, 1)
        
        self.assertEqual(values1[3].value.const_type, 'string')
        self.assertEqual(values1[3].value.value, 'a')
        
        self.assertEqual(values1[4].value.const_type, 'boolean')
        self.assertEqual(values1[4].value.value, True)
        
        # 测试指定列名的多行插入
        sql2 = "INSERT INTO tbl2 (c1, c2, c3) VALUES (3, 'a', TRUE), (4, 'b', FALSE);"
        stmt2 = Parser(sql2).parse()
        p2 = Plan.build(stmt2)
        
        self.assertIsInstance(p2.node, InsertNode)
        self.assertEqual(p2.node.table_name, "tbl2")
        self.assertEqual(p2.node.columns, ["c1", "c2", "c3"])
        self.assertEqual(len(p2.node.values), 2)
        
        # 验证第一行值
        row1 = p2.node.values[0]
        self.assertEqual(row1[0].value.const_type, 'integer')
        self.assertEqual(row1[0].value.value, 3)
        self.assertEqual(row1[1].value.const_type, 'string')
        self.assertEqual(row1[1].value.value, 'a')
        self.assertEqual(row1[2].value.const_type, 'boolean')
        self.assertEqual(row1[2].value.value, True)
        
        # 验证第二行值
        row2 = p2.node.values[1]
        self.assertEqual(row2[0].value.const_type, 'integer')
        self.assertEqual(row2[0].value.value, 4)
        self.assertEqual(row2[1].value.const_type, 'string')
        self.assertEqual(row2[1].value.value, 'b')
        self.assertEqual(row2[2].value.const_type, 'boolean')
        self.assertEqual(row2[2].value.value, False)
    
    def test_plan_select(self):
        """测试查询计划"""
        # 基本查询
        sql = "SELECT * FROM tbl1;"
        stmt = Parser(sql).parse()
        p = Plan.build(stmt)
        
        self.assertIsInstance(p.node, ScanNode)
        self.assertEqual(p.node.table_name, "tbl1")
        self.assertIsNone(p.node.where)
        
        # 带WHERE条件的查询
        sql_where = "SELECT * FROM tbl1 WHERE id = 1;"
        stmt_where = Parser(sql_where).parse()
        p_where = Plan.build(stmt_where)
        
        self.assertIsInstance(p_where.node, ScanNode)
        self.assertEqual(p_where.node.table_name, "tbl1")
        self.assertIsNotNone(p_where.node.where)
        self.assertEqual(p_where.node.where.cond_type, "equals")
        self.assertEqual(p_where.node.where.column, "id")
        self.assertEqual(p_where.node.where.value.value.value, 1)
    
    def test_plan_update(self):
        """测试更新计划"""
        # 基本更新
        sql = "UPDATE tbl1 SET name = 'new_name', age = 30;"
        stmt = Parser(sql).parse()
        p = Plan.build(stmt)
        
        self.assertIsInstance(p.node, UpdateNode)
        self.assertEqual(p.node.table_name, "tbl1")
        self.assertEqual(len(p.node.updates), 2)
        self.assertIsNone(p.node.where)
        
        # 验证更新值
        self.assertEqual(p.node.updates["name"].value.const_type, "string")
        self.assertEqual(p.node.updates["name"].value.value, "new_name")
        self.assertEqual(p.node.updates["age"].value.const_type, "integer")
        self.assertEqual(p.node.updates["age"].value.value, 30)
        
        # 带WHERE条件的更新
        sql_where = "UPDATE tbl1 SET salary = 5000.0 WHERE id = 1;"
        stmt_where = Parser(sql_where).parse()
        p_where = Plan.build(stmt_where)
        
        self.assertIsInstance(p_where.node, UpdateNode)
        self.assertEqual(p_where.node.table_name, "tbl1")
        self.assertEqual(len(p_where.node.updates), 1)
        self.assertIsNotNone(p_where.node.where)
        
        # 验证更新值
        self.assertEqual(p_where.node.updates["salary"].value.const_type, "float")
        self.assertEqual(p_where.node.updates["salary"].value.value, 5000.0)
        
        # 验证条件
        self.assertEqual(p_where.node.where.cond_type, "equals")
        self.assertEqual(p_where.node.where.column, "id")
        self.assertEqual(p_where.node.where.value.value.value, 1)
    
    def test_plan_delete(self):
        """测试删除计划"""
        # 基本删除
        sql = "DELETE FROM tbl1;"
        stmt = Parser(sql).parse()
        p = Plan.build(stmt)
        
        self.assertIsInstance(p.node, DeleteNode)
        self.assertEqual(p.node.table_name, "tbl1")
        self.assertIsNone(p.node.where)
        
        # 带WHERE条件的删除
        sql_where = "DELETE FROM tbl1 WHERE id > 5;"
        stmt_where = Parser(sql_where).parse()
        p_where = Plan.build(stmt_where)
        
        self.assertIsInstance(p_where.node, DeleteNode)
        self.assertEqual(p_where.node.table_name, "tbl1")
        self.assertIsNotNone(p_where.node.where)
        
        # 验证条件
        self.assertEqual(p_where.node.where.cond_type, "gt")
        self.assertEqual(p_where.node.where.column, "id")
        self.assertEqual(p_where.node.where.value.value.value, 5)


if __name__ == "__main__":
    unittest.main()