#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
多Schema示例
===========

这个示例展示如何在cooSql中创建和使用多个schema（表），并展示表之间的关系。
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from storage.disk import DiskEngine
from sql.engine.kv import KVEngine
from sql.session import Session

def run_multi_schema_example(db_path):
    """多Schema操作示例"""
    print("\n=== 多Schema示例 ===")
    
    # 初始化存储引擎和SQL会话
    storage_engine = DiskEngine(db_path)
    kv_engine = KVEngine(storage_engine)
    transaction = kv_engine.begin()
    session = Session(transaction)
    
    try:
        # 创建部门表
        print("创建部门表...")
        session.execute("""
        CREATE TABLE departments (
            dept_id INTEGER NOT NULL,
            dept_name STRING NOT NULL,
            location STRING DEFAULT 'Unknown'
        );
        """)
        
        # 创建员工表
        print("创建员工表...")
        session.execute("""
        CREATE TABLE employees (
            emp_id INTEGER NOT NULL,
            name STRING NOT NULL,
            dept_id INTEGER NOT NULL,
            salary FLOAT DEFAULT 0.0,
            hire_date STRING
        );
        """)
        
        # 创建项目表
        print("创建项目表...")
        session.execute("""
        CREATE TABLE projects (
            project_id INTEGER NOT NULL,
            project_name STRING NOT NULL,
            dept_id INTEGER NOT NULL,
            start_date STRING,
            end_date STRING,
            budget FLOAT DEFAULT 0.0
        );
        """)
        
        # 插入部门数据
        print("\n插入部门数据...")
        session.execute("INSERT INTO departments VALUES (101, 'Engineering', 'Building A');")
        session.execute("INSERT INTO departments VALUES (102, 'Marketing', 'Building B');")
        session.execute("INSERT INTO departments VALUES (103, 'HR', 'Building C');")
        
        # 插入员工数据
        print("插入员工数据...")
        session.execute("INSERT INTO employees VALUES (1001, 'Zhang Wei', 101, 8000.0, '2020-01-15');")
        session.execute("INSERT INTO employees VALUES (1002, 'Li Na', 101, 7500.0, '2020-02-20');")
        session.execute("INSERT INTO employees VALUES (1003, 'Wang Fang', 102, 6800.0, '2020-03-10');")
        session.execute("INSERT INTO employees VALUES (1004, 'Chen Jie', 103, 6000.0, '2020-04-05');")
        
        # 插入项目数据
        print("插入项目数据...")
        session.execute("INSERT INTO projects VALUES (2001, 'Database Redesign', 101, '2023-01-01', '2023-06-30', 150000.0);")
        session.execute("INSERT INTO projects VALUES (2002, 'Website Relaunch', 102, '2023-02-15', '2023-08-15', 120000.0);")
        session.execute("INSERT INTO projects VALUES (2003, 'Recruitment System', 103, '2023-03-01', '2023-12-31', 80000.0);")
        
        # 查询各个表
        print("\n查询部门表...")
        dept_results = session.execute("SELECT * FROM departments;")
        print_table(dept_results, ["部门ID", "部门名称", "位置"])
        
        print("\n查询员工表...")
        emp_results = session.execute("SELECT * FROM employees;")
        print_table(emp_results, ["员工ID", "姓名", "部门ID", "薪资", "入职日期"])
        
        print("\n查询项目表...")
        proj_results = session.execute("SELECT * FROM projects;")
        print_table(proj_results, ["项目ID", "项目名称", "部门ID", "开始日期", "结束日期", "预算"])
        
        # 提交事务
        transaction.commit()
        print("\n所有操作已提交")
        
    except Exception as e:
        # 发生错误时回滚事务
        transaction.rollback()
        print(f"发生错误，事务已回滚: {e}")
        raise
    finally:
        # 关闭资源
        storage_engine.close()

def print_table(results, headers):
    """打印表格结果"""
    # 打印表头
    header_str = "\t".join(headers)
    print(header_str)
    print("-" * len(header_str) * 2)
    
    # 打印数据行
    for row in results:
        row_values = [str(col.value) if col.value is not None else "NULL" for col in row]
        print("\t".join(row_values))

if __name__ == "__main__":
    # 使用当前目录下的临时数据库文件
    db_file = os.path.join(os.path.dirname(__file__), "multi_schema.db")
    
    try:
        run_multi_schema_example(db_file)
    finally:
        # 清理临时数据库文件
        if os.path.exists(db_file):
            print(f"\n清理临时数据库文件: {db_file}")
            os.unlink(db_file)