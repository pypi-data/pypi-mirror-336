#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
磁盘存储引擎示例
===============

这个示例展示如何使用磁盘存储引擎和SQL引擎执行基本的SQL操作，并验证数据持久性。
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from storage.disk import DiskEngine
from sql.engine.kv import KVEngine
from sql.session import Session

def run_disk_example(db_path):
    """使用磁盘存储引擎的SQL操作示例"""
    print("\n=== 磁盘存储引擎示例 ===")
    
    # 初始化存储引擎和SQL会话
    storage_engine = DiskEngine(db_path)
    kv_engine = KVEngine(storage_engine)
    transaction = kv_engine.begin()
    session = Session(transaction)
    
    try:
        # 创建表
        print("创建产品表...")
        session.execute("""
        CREATE TABLE products (
            id INTEGER NOT NULL,
            name STRING,
            price FLOAT DEFAULT 0.0,
            in_stock BOOLEAN DEFAULT FALSE
        );
        """)
        
        # 插入数据
        print("插入产品数据...")
        session.execute("INSERT INTO products VALUES (101, 'Laptop', 999.99, TRUE);")
        session.execute("INSERT INTO products VALUES (102, 'Smartphone', 499.99, TRUE);")
        session.execute("INSERT INTO products (id, name, price) VALUES (103, 'Headphones', 59.99);")
        
        # 查询数据
        print("查询所有产品...")
        results = session.execute("SELECT * FROM products;")
        
        # 打印结果
        print("\n产品列表:")
        print("ID\t名称\t\t价格\t库存")
        print("----------------------------------")
        for row in results:
            name = row[1].value if row[1].value else ""
            price = row[2].value if row[2].value else 0.0
            in_stock = row[3].value if row[3].value is not None else False
            print(f"{row[0].value}\t{name}\t{price}\t{in_stock}")
        
        # 提交事务
        transaction.commit()
        print("\n事务已提交")
        
        # 展示持久性：再次打开数据库并查询
        print("\n重新打开数据库验证持久性...")
        new_storage = DiskEngine(db_path)
        new_kv = KVEngine(new_storage)
        new_txn = new_kv.begin()
        new_session = Session(new_txn)
        
        products = new_session.execute("SELECT * FROM products;")
        print(f"从磁盘读取到 {len(products)} 条产品记录")
        
        if len(products) > 0:
            print("\n读取的产品列表:")
            print("ID\t名称\t\t价格\t库存")
            print("----------------------------------")
            for row in products:
                name = row[1].value if row[1].value else ""
                price = row[2].value if row[2].value else 0.0
                in_stock = row[3].value if row[3].value is not None else False
                print(f"{row[0].value}\t{name}\t{price}\t{in_stock}")
        
    except Exception as e:
        # 发生错误时回滚事务
        transaction.rollback()
        print(f"发生错误，事务已回滚: {e}")
        raise

def main():
    """主函数，供run_all_examples.py调用"""
    # 使用当前目录下的临时数据库文件
    db_file = os.path.join(os.path.dirname(__file__), "example.db")
    
    try:
        run_disk_example(db_file)
    finally:
        # 清理临时数据库文件
        if os.path.exists(db_file):
            print(f"\n清理临时数据库文件: {db_file}")
            os.unlink(db_file)

if __name__ == "__main__":
    # 使用当前目录下的临时数据库文件
    db_file = os.path.join(os.path.dirname(__file__), "example.db")
    
    try:
        run_disk_example(db_file)
    finally:
        # 清理临时数据库文件
        if os.path.exists(db_file):
            print(f"\n清理临时数据库文件: {db_file}")
            os.unlink(db_file) 