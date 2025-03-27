#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
内存存储引擎示例
===============

这个示例展示如何使用内存存储引擎和SQL引擎执行基本的SQL操作。
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from storage.memory import MemoryEngine
from sql.engine.kv import KVEngine
from sql.session import Session

def run_memory_example():
    """使用内存存储引擎的SQL操作示例"""
    print("=== 内存存储引擎示例 ===")
    
    # 初始化存储引擎和SQL会话
    storage_engine = MemoryEngine()
    kv_engine = KVEngine(storage_engine)
    transaction = kv_engine.begin()
    session = Session(transaction)
    
    try:
        # 创建表
        print("创建用户表...")
        session.execute("""
        CREATE TABLE users (
            id INTEGER NOT NULL,
            name STRING,
            age INTEGER DEFAULT 18,
            is_active BOOLEAN DEFAULT TRUE
        );
        """)
        
        # 插入数据
        print("插入用户数据...")
        session.execute("INSERT INTO users VALUES (1, 'Alice', 25, TRUE);")
        session.execute("INSERT INTO users VALUES (2, 'Bob', 30, TRUE);")
        session.execute("INSERT INTO users (id, name) VALUES (3, 'Charlie');")
        
        # 查询数据
        print("查询所有用户...")
        results = session.execute("SELECT * FROM users;")
        
        # 打印结果
        print("\n用户列表:")
        print("ID\t姓名\t年龄\t是否活跃")
        print("-------------------------")
        for row in results:
            print(f"{row[0].value}\t{row[1].value}\t{row[2].value}\t{row[3].value}")
        
        # 提交事务
        transaction.commit()
        print("\n事务已提交")
        
    except Exception as e:
        # 发生错误时回滚事务
        transaction.rollback()
        print(f"发生错误，事务已回滚: {e}")
        raise

def main():
    """主函数，供run_all_examples.py调用"""
    run_memory_example()

if __name__ == "__main__":
    run_memory_example() 