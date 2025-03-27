#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CRUD操作示例
==========

这个示例展示如何在cooSql中执行完整的CRUD（创建、读取、更新、删除）操作。
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from storage.disk import DiskEngine
from sql.engine.kv import KVEngine
from sql.session import Session

def run_crud_example(db_path):
    """CRUD操作示例"""
    print("\n=== CRUD操作示例 ===")
    
    # 初始化存储引擎和SQL会话
    storage_engine = DiskEngine(db_path)
    kv_engine = KVEngine(storage_engine)
    transaction = kv_engine.begin()
    session = Session(transaction)
    
    try:
        # 第1步：创建表（CREATE）
        print("1. 创建图书表...")
        session.execute("""
        CREATE TABLE books (
            book_id INTEGER NOT NULL,
            title STRING NOT NULL,
            author STRING,
            price FLOAT DEFAULT 0.0,
            stock INTEGER DEFAULT 0,
            is_available BOOLEAN DEFAULT TRUE
        );
        """)
        
        # 第2步：插入数据（CREATE）
        print("\n2. 插入图书数据...")
        
        # 使用完整字段插入
        session.execute("INSERT INTO books VALUES (1001, '三体', '刘慈欣', 69.8, 100, TRUE);")
        session.execute("INSERT INTO books VALUES (1002, '解忧杂货店', '东野圭吾', 39.5, 50, TRUE);")
        
        # 使用部分字段插入，其他使用默认值
        session.execute("INSERT INTO books (book_id, title, author, price) VALUES (1003, '活着', '余华', 35.0);")
        session.execute("INSERT INTO books (book_id, title, author) VALUES (1004, '白夜行', '东野圭吾');")
        
        # 批量插入更多数据
        print("批量插入更多图书...")
        books_data = [
            (1005, '围城', '钱钟书', 45.0, 30, True),
            (1006, '百年孤独', '加西亚·马尔克斯', 58.0, 25, True),
            (1007, '红楼梦', '曹雪芹', 89.9, 40, True),
            (1008, '平凡的世界', '路遥', 79.8, 35, True),
            (1009, '人类简史', '尤瓦尔·赫拉利', 68.0, 0, False)
        ]
        
        for book in books_data:
            session.execute(f"""
            INSERT INTO books VALUES 
            ({book[0]}, '{book[1]}', '{book[2]}', {book[3]}, {book[4]}, {str(book[5]).upper()});
            """)
        
        # 第3步：查询数据（READ）
        print("\n3. 查询所有图书数据...")
        all_books = session.execute("SELECT * FROM books;")
        print_table(all_books, ["图书ID", "书名", "作者", "价格", "库存", "是否可用"])
        
        # 提交事务
        transaction.commit()
        print("\n第一阶段操作已提交")
        
        # 开始新事务
        transaction = kv_engine.begin()
        session = Session(transaction)
        
        # 第4步：更新数据（UPDATE）
        print("\n4. 更新图书数据...")
        
        # 更新库存为0的图书为不可用
        print("更新库存为0的图书为不可用...")
        session.execute("UPDATE books SET is_available = FALSE WHERE stock = 0;")
        
        # 更新某本书的价格和库存
        print("更新《活着》的价格和库存...")
        session.execute("UPDATE books SET price = 42.0, stock = 60 WHERE title = '活着';")
        
        # 批量更新某作者的所有图书价格
        print("将东野圭吾所有图书价格上调10%...")
        session.execute("UPDATE books SET price = price * 1.1 WHERE author = '东野圭吾';")
        
        # 查看更新后的数据
        print("\n查询更新后的图书数据...")
        updated_books = session.execute("SELECT * FROM books;")
        print_table(updated_books, ["图书ID", "书名", "作者", "价格", "库存", "是否可用"])
        
        # 提交更新事务
        transaction.commit()
        print("\n更新操作已提交")
        
        # 开始新事务
        transaction = kv_engine.begin()
        session = Session(transaction)
        
        # 第5步：删除数据（DELETE）
        print("\n5. 删除图书数据...")
        
        # 删除特定图书
        print("删除《百年孤独》...")
        session.execute("DELETE FROM books WHERE title = '百年孤独';")
        
        # 删除某作者的所有图书
        print("删除东野圭吾的所有图书...")
        session.execute("DELETE FROM books WHERE author = '东野圭吾';")
        
        # 删除库存为0的图书
        print("删除库存为0且不可用的图书...")
        session.execute("DELETE FROM books WHERE stock = 0 AND is_available = FALSE;")
        
        # 查看删除后的数据
        print("\n查询删除后的图书数据...")
        remaining_books = session.execute("SELECT * FROM books;")
        print_table(remaining_books, ["图书ID", "书名", "作者", "价格", "库存", "是否可用"])
        
        # 提交删除事务
        transaction.commit()
        print("\n删除操作已提交")
        
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
    db_file = os.path.join(os.path.dirname(__file__), "crud_example.db")
    
    try:
        run_crud_example(db_file)
    finally:
        # 清理临时数据库文件
        if os.path.exists(db_file):
            print(f"\n清理临时数据库文件: {db_file}")
            os.unlink(db_file)