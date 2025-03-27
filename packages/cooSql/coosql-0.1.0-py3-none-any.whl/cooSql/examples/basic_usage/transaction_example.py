#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
事务处理示例
===========

这个示例展示如何使用SQL引擎进行事务处理，包括提交和回滚操作。
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from storage.memory import MemoryEngine
from sql.engine.kv import KVEngine
from sql.session import Session

def successful_transaction():
    """成功提交的事务示例"""
    print("=== 成功提交的事务示例 ===")
    
    # 初始化存储引擎和SQL会话
    storage_engine = MemoryEngine()
    kv_engine = KVEngine(storage_engine)
    transaction = kv_engine.begin()
    session = Session(transaction)
    
    try:
        # 创建表
        print("创建银行账户表...")
        session.execute("""
        CREATE TABLE accounts (
            id INTEGER NOT NULL,
            holder STRING,
            balance FLOAT DEFAULT 0.0
        );
        """)
        
        # 插入初始数据
        print("插入初始账户数据...")
        session.execute("INSERT INTO accounts VALUES (1, 'Alice', 1000.0);")
        session.execute("INSERT INTO accounts VALUES (2, 'Bob', 500.0);")
        
        # 执行转账：Alice向Bob转账200元
        print("执行转账操作: Alice -> Bob 转账200元")
        
        # 1. 从Alice账户扣除200元
        # 这里需要先获取Alice的当前余额
        alice_account = session.execute("SELECT * FROM accounts WHERE id = 1;")[0]
        alice_balance = alice_account[2].value
        new_alice_balance = alice_balance - 200.0
        
        # 2. 向Bob账户增加200元
        # 这里需要先获取Bob的当前余额
        bob_account = session.execute("SELECT * FROM accounts WHERE id = 2;")[0]
        bob_balance = bob_account[2].value
        new_bob_balance = bob_balance + 200.0
        
        # 3. 更新账户余额（这里使用INSERT模拟UPDATE操作）
        print(f"更新Alice余额: {alice_balance} -> {new_alice_balance}")
        session.execute(f"INSERT INTO accounts VALUES (1, 'Alice', {new_alice_balance});")
        
        print(f"更新Bob余额: {bob_balance} -> {new_bob_balance}")
        session.execute(f"INSERT INTO accounts VALUES (2, 'Bob', {new_bob_balance});")
        
        # 查询更新后的账户数据
        print("\n转账后的账户数据:")
        results = session.execute("SELECT * FROM accounts;")
        print("ID\t户主\t余额")
        print("------------------")
        for row in results:
            print(f"{row[0].value}\t{row[1].value}\t{row[2].value}")
        
        # 提交事务
        transaction.commit()
        print("\n事务已成功提交")
        
    except Exception as e:
        # 发生错误时回滚事务
        transaction.rollback()
        print(f"发生错误，事务已回滚: {e}")
        raise

def failed_transaction():
    """失败回滚的事务示例"""
    print("\n=== 失败回滚的事务示例 ===")
    
    # 初始化存储引擎和SQL会话
    storage_engine = MemoryEngine()
    kv_engine = KVEngine(storage_engine)
    transaction = kv_engine.begin()
    session = Session(transaction)
    
    try:
        # 创建表
        print("创建银行账户表...")
        session.execute("""
        CREATE TABLE accounts (
            id INTEGER NOT NULL,
            holder STRING,
            balance FLOAT DEFAULT 0.0
        );
        """)
        
        # 提交创建表，并开始新事务
        transaction.commit()
        transaction = kv_engine.begin()
        session = Session(transaction)
        
        # 插入初始数据
        print("插入初始账户数据...")
        session.execute("INSERT INTO accounts VALUES (1, 'Alice', 1000.0);")
        session.execute("INSERT INTO accounts VALUES (2, 'Bob', 500.0);")
        
        # 查询初始账户数据
        print("\n初始账户数据:")
        initial_results = session.execute("SELECT * FROM accounts;")
        print("ID\t户主\t余额")
        print("------------------")
        for row in initial_results:
            print(f"{row[0].value}\t{row[1].value}\t{row[2].value}")
        
        # 尝试执行转账，但金额超过Alice的余额
        print("\n尝试执行转账操作: Alice -> Bob 转账2000元（超过Alice余额）")
        
        # 1. 从Alice账户扣除2000元
        alice_account = session.execute("SELECT * FROM accounts WHERE id = 1;")[0]
        alice_balance = alice_account[2].value
        new_alice_balance = alice_balance - 2000.0
        
        # 检查余额是否足够
        if new_alice_balance < 0:
            raise ValueError("余额不足，无法完成转账")
        
        # 如果转账能够执行，则继续以下操作（实际上不会执行到这里）
        bob_account = session.execute("SELECT * FROM accounts WHERE id = 2;")[0]
        bob_balance = bob_account[2].value
        new_bob_balance = bob_balance + 2000.0
        
        session.execute(f"INSERT INTO accounts VALUES (1, 'Alice', {new_alice_balance});")
        session.execute(f"INSERT INTO accounts VALUES (2, 'Bob', {new_bob_balance});")
        
        # 提交事务
        transaction.commit()
        
    except Exception as e:
        # 发生错误时回滚事务
        transaction.rollback()
        print(f"发生错误，事务已回滚: {e}")
        
        # 验证回滚后的数据
        print("\n验证回滚后的数据状态...")
        
        try:
            # 创建新事务
            new_transaction = kv_engine.begin()
            new_session = Session(new_transaction)
            
            # 查询数据
            results = new_session.execute("SELECT * FROM accounts;")
            
            # 显示结果
            if results and len(results) > 0:
                print("\n回滚后的账户数据:")
                print("ID\t户主\t余额")
                print("------------------")
                for row in results:
                    print(f"{row[0].value}\t{row[1].value}\t{row[2].value}")
            else:
                print("未找到任何账户数据，可能是表被回滚或未创建。")
                
        except Exception as e2:
            print(f"查询回滚后的数据时出错: {str(e2)}")
            print("这是正常的，因为我们在回滚后，表可能不存在。")

def main():
    """主函数，供run_all_examples.py调用"""
    # 运行成功提交的事务示例
    successful_transaction()
    
    # 运行失败回滚的事务示例
    failed_transaction()

if __name__ == "__main__":
    # 运行成功提交的事务示例
    successful_transaction()
    
    # 运行失败回滚的事务示例
    failed_transaction() 