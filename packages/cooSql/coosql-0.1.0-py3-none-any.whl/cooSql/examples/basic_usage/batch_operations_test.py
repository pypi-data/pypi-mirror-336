#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
批量操作和压力测试
===============

这个示例展示如何在cooSql中进行批量数据操作和压力测试，包括：
1. 多种表结构(schema)的创建
2. 批量数据写入测试
3. 多种条件的增删改查操作
4. 关闭数据库后重新打开验证数据一致性
"""

import os
import sys
import time
import random
import datetime
from typing import List, Dict, Any

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from storage.disk import DiskEngine
from sql.engine.kv import KVEngine
from sql.session import Session

# 测试参数
PRODUCTS_COUNT = 1000  # 产品数量
CUSTOMERS_COUNT = 500  # 客户数量
ORDERS_COUNT = 2000    # 订单数量

def print_table(results, headers, max_rows=20):
    """打印表格结果，限制最大行数"""
    if not results:
        print("（无结果）")
        return
        
    # 打印表头
    header_str = "\t".join(headers)
    print(header_str)
    print("-" * len(header_str) * 2)
    
    # 打印数据行（最多显示max_rows行）
    count = 0
    for row in results:
        if count >= max_rows:
            print(f"... 还有{len(results) - max_rows}行未显示 ...")
            break
            
        row_values = [str(col.value) if col.value is not None else "NULL" for col in row]
        print("\t".join(row_values))
        count += 1

def create_schemas(session):
    """创建多个表结构"""
    print("\n=== 创建表结构 ===")
    
    # 产品表
    print("创建产品表...")
    session.execute("""
    CREATE TABLE products (
        product_id INTEGER NOT NULL,
        name STRING NOT NULL,
        category STRING,
        price FLOAT NOT NULL,
        stock INTEGER DEFAULT 0,
        created_at STRING
    );
    """)
    
    # 客户表
    print("创建客户表...")
    session.execute("""
    CREATE TABLE customers (
        customer_id INTEGER NOT NULL,
        name STRING NOT NULL,
        email STRING,
        signup_date STRING,
        vip_level INTEGER DEFAULT 0,
        total_spend FLOAT DEFAULT 0.0
    );
    """)
    
    # 订单表
    print("创建订单表...")
    session.execute("""
    CREATE TABLE orders (
        order_id INTEGER NOT NULL,
        customer_id INTEGER NOT NULL,
        order_date STRING NOT NULL,
        status STRING DEFAULT 'pending',
        total_amount FLOAT NOT NULL
    );
    """)
    
    # 订单详情表
    print("创建订单详情表...")
    session.execute("""
    CREATE TABLE order_items (
        item_id INTEGER NOT NULL,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        unit_price FLOAT NOT NULL
    );
    """)
    
    print("所有表结构创建完成")

def generate_products(count: int) -> List[Dict[str, Any]]:
    """生成产品测试数据"""
    products = []
    categories = ["电子", "服装", "家居", "图书", "食品", "玩具", "办公", "运动", "美妆", "宠物"]
    
    for i in range(1, count + 1):
        product = {
            "product_id": i,
            "name": f"产品-{i}",
            "category": random.choice(categories),
            "price": round(random.uniform(10, 5000), 2),
            "stock": random.randint(0, 1000),
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        products.append(product)
    
    return products

def generate_customers(count: int) -> List[Dict[str, Any]]:
    """生成客户测试数据"""
    customers = []
    
    for i in range(1, count + 1):
        signup_date = datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 365))
        customer = {
            "customer_id": i,
            "name": f"客户-{i}",
            "email": f"customer{i}@example.com",
            "signup_date": signup_date.strftime("%Y-%m-%d"),
            "vip_level": random.randint(0, 5),
            "total_spend": round(random.uniform(0, 50000), 2)
        }
        customers.append(customer)
    
    return customers

def generate_orders(count: int, customers_count: int, products_count: int) -> tuple:
    """生成订单和订单详情测试数据"""
    orders = []
    order_items = []
    status_options = ["pending", "confirmed", "shipped", "delivered", "cancelled"]
    item_id = 1
    
    for i in range(1, count + 1):
        customer_id = random.randint(1, customers_count)
        items_count = random.randint(1, 5)  # 每个订单1-5个商品
        order_date = datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 90))
        
        # 计算订单总金额
        total = 0
        order_items_list = []
        
        for j in range(items_count):
            product_id = random.randint(1, products_count)
            quantity = random.randint(1, 10)
            unit_price = round(random.uniform(10, 1000), 2)
            item_total = quantity * unit_price
            total += item_total
            
            order_item = {
                "item_id": item_id,
                "order_id": i,
                "product_id": product_id,
                "quantity": quantity,
                "unit_price": unit_price
            }
            order_items.append(order_item)
            item_id += 1
        
        order = {
            "order_id": i,
            "customer_id": customer_id,
            "order_date": order_date.strftime("%Y-%m-%d %H:%M:%S"),
            "status": random.choice(status_options),
            "total_amount": round(total, 2)
        }
        orders.append(order)
    
    return orders, order_items

def batch_insert_data(session, db_path):
    """批量插入测试数据"""
    print("\n=== 批量插入测试数据 ===")
    
    # 生成测试数据
    products = generate_products(PRODUCTS_COUNT)
    customers = generate_customers(CUSTOMERS_COUNT)
    orders, order_items = generate_orders(ORDERS_COUNT, CUSTOMERS_COUNT, PRODUCTS_COUNT)
    
    # 批量插入产品数据
    print(f"插入 {len(products)} 条产品数据...")
    start_time = time.time()
    
    batch_size = 100
    for i in range(0, len(products), batch_size):
        batch = products[i:i+batch_size]
        values_str = ", ".join([
            f"({p['product_id']}, '{p['name']}', '{p['category']}', {p['price']}, {p['stock']}, '{p['created_at']}')"
            for p in batch
        ])
        session.execute(f"INSERT INTO products VALUES {values_str};")
        
        # 进度显示
        if (i + batch_size) % 500 == 0 or (i + batch_size) >= len(products):
            print(f"  已完成: {min(i + batch_size, len(products))}/{len(products)} 条产品记录")
    
    products_time = time.time() - start_time
    print(f"产品数据插入完成，耗时: {products_time:.2f} 秒")
    
    # 批量插入客户数据
    print(f"\n插入 {len(customers)} 条客户数据...")
    start_time = time.time()
    
    batch_size = 100
    for i in range(0, len(customers), batch_size):
        batch = customers[i:i+batch_size]
        values_str = ", ".join([
            f"({c['customer_id']}, '{c['name']}', '{c['email']}', '{c['signup_date']}', {c['vip_level']}, {c['total_spend']})"
            for c in batch
        ])
        session.execute(f"INSERT INTO customers VALUES {values_str};")
        
        # 进度显示
        if (i + batch_size) % 500 == 0 or (i + batch_size) >= len(customers):
            print(f"  已完成: {min(i + batch_size, len(customers))}/{len(customers)} 条客户记录")
    
    customers_time = time.time() - start_time
    print(f"客户数据插入完成，耗时: {customers_time:.2f} 秒")
    
    # 批量插入订单数据
    print(f"\n插入 {len(orders)} 条订单数据...")
    start_time = time.time()
    
    batch_size = 100
    for i in range(0, len(orders), batch_size):
        batch = orders[i:i+batch_size]
        values_str = ", ".join([
            f"({o['order_id']}, {o['customer_id']}, '{o['order_date']}', '{o['status']}', {o['total_amount']})"
            for o in batch
        ])
        session.execute(f"INSERT INTO orders VALUES {values_str};")
        
        # 进度显示
        if (i + batch_size) % 500 == 0 or (i + batch_size) >= len(orders):
            print(f"  已完成: {min(i + batch_size, len(orders))}/{len(orders)} 条订单记录")
    
    orders_time = time.time() - start_time
    print(f"订单数据插入完成，耗时: {orders_time:.2f} 秒")
    
    # 批量插入订单详情数据
    print(f"\n插入 {len(order_items)} 条订单详情数据...")
    start_time = time.time()
    
    batch_size = 100
    for i in range(0, len(order_items), batch_size):
        batch = order_items[i:i+batch_size]
        values_str = ", ".join([
            f"({item['item_id']}, {item['order_id']}, {item['product_id']}, {item['quantity']}, {item['unit_price']})"
            for item in batch
        ])
        session.execute(f"INSERT INTO order_items VALUES {values_str};")
        
        # 进度显示
        if (i + batch_size) % 500 == 0 or (i + batch_size) >= len(order_items):
            print(f"  已完成: {min(i + batch_size, len(order_items))}/{len(order_items)} 条订单详情记录")
    
    items_time = time.time() - start_time
    print(f"订单详情数据插入完成，耗时: {items_time:.2f} 秒")
    
    # 统计总时间和写入速度
    total_time = products_time + customers_time + orders_time + items_time
    total_records = len(products) + len(customers) + len(orders) + len(order_items)
    print(f"\n总计插入 {total_records} 条记录，总耗时: {total_time:.2f} 秒，平均速度: {total_records/total_time:.2f} 条/秒")
    
    # 简单统计
    data_summary = {
        "products_count": len(products),
        "customers_count": len(customers),
        "orders_count": len(orders),
        "order_items_count": len(order_items),
        "avg_items_per_order": len(order_items) / len(orders)
    }
    
    return data_summary

def perform_queries(session):
    """执行各种查询操作"""
    print("\n=== 执行查询操作 ===")
    start_time = time.time()
    
    # 1. 统计各表的记录数
    print("1. 统计各表记录数...")
    tables = ["products", "customers", "orders", "order_items"]
    for table in tables:
        try:
            # 在cooSql中不支持COUNT函数，所以我们查询所有数据然后计算长度
            results = session.execute(f"SELECT * FROM {table};")
            count = len(results)
            print(f"  {table} 表: {count} 条记录")
        except Exception as e:
            print(f"  查询 {table} 表失败: {e}")
    
    # 2. 查询价格最高的5个产品
    print("\n2. 查询价格最高的产品(TOP 5)...")
    try:
        all_products = session.execute("SELECT * FROM products;")
        # 由于cooSql不支持ORDER BY子句，我们在代码中排序
        sorted_products = sorted(all_products, key=lambda row: row[3].value, reverse=True)  # 第3列是price
        top_products = sorted_products[:5]
        print_table(top_products, ["产品ID", "名称", "类别", "价格", "库存", "创建时间"])
    except Exception as e:
        print(f"  查询失败: {e}")
    
    # 3. 查询VIP等级最高的5个客户
    print("\n3. 查询VIP等级最高的客户(TOP 5)...")
    try:
        all_customers = session.execute("SELECT * FROM customers;")
        # 按VIP等级排序
        sorted_customers = sorted(all_customers, key=lambda row: row[4].value, reverse=True)  # 第4列是vip_level
        top_customers = sorted_customers[:5]
        print_table(top_customers, ["客户ID", "姓名", "邮箱", "注册日期", "VIP等级", "总消费"])
    except Exception as e:
        print(f"  查询失败: {e}")
    
    # 4. 查询订单金额最大的5个订单
    print("\n4. 查询订单金额最大的订单(TOP 5)...")
    try:
        all_orders = session.execute("SELECT * FROM orders;")
        # 按订单金额排序
        sorted_orders = sorted(all_orders, key=lambda row: row[4].value, reverse=True)  # 第4列是total_amount
        top_orders = sorted_orders[:5]
        print_table(top_orders, ["订单ID", "客户ID", "订单日期", "状态", "总金额"])
    except Exception as e:
        print(f"  查询失败: {e}")
    
    # 5. 查询特定分类的产品数量
    print("\n5. 查询各分类的产品数量...")
    try:
        all_products = session.execute("SELECT * FROM products;")
        # 按类别分组统计
        category_counts = {}
        for product in all_products:
            category = product[2].value  # 第2列是category
            if category in category_counts:
                category_counts[category] += 1
            else:
                category_counts[category] = 1
        
        # 打印结果
        for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {category}: {count} 个产品")
    except Exception as e:
        print(f"  查询失败: {e}")
    
    # 6. 查询订单状态分布
    print("\n6. 查询订单状态分布...")
    try:
        all_orders = session.execute("SELECT * FROM orders;")
        # 按状态分组统计
        status_counts = {}
        for order in all_orders:
            status = order[3].value  # 第3列是status
            if status in status_counts:
                status_counts[status] += 1
            else:
                status_counts[status] = 1
        
        # 打印结果
        for status, count in sorted(status_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {status}: {count} 个订单 ({count/len(all_orders)*100:.1f}%)")
    except Exception as e:
        print(f"  查询失败: {e}")
    
    # 7. 查询电子类别且价格大于1000的产品
    print("\n7. 查询电子类别且价格大于1000的产品...")
    try:
        # 由于cooSql支持简单WHERE条件，但不支持复杂条件，我们在代码中过滤
        all_products = session.execute("SELECT * FROM products;")
        filtered_products = [p for p in all_products if p[2].value == "电子" and p[3].value > 1000]
        print_table(filtered_products, ["产品ID", "名称", "类别", "价格", "库存", "创建时间"])
    except Exception as e:
        print(f"  查询失败: {e}")
    
    # 查询操作总耗时
    query_time = time.time() - start_time
    print(f"\n查询操作完成，总耗时: {query_time:.2f} 秒")

def perform_updates(session):
    """执行更新操作"""
    print("\n=== 执行更新操作 ===")
    
    # 1. 更新产品价格
    print("1. 更新产品价格（提高电子类产品价格10%）...")
    try:
        # 查询所有电子类产品
        all_products = session.execute("SELECT * FROM products;")
        electronic_products = [p for p in all_products if p[2].value == "电子"]
        
        # 逐个更新产品价格
        update_count = 0
        for product in electronic_products:
            product_id = product[0].value
            current_price = product[3].value
            new_price = round(current_price * 1.1, 2)  # 提高10%
            session.execute(f"UPDATE products SET price = {new_price} WHERE product_id = {product_id};")
            update_count += 1
        
        print(f"  成功更新 {update_count} 个电子类产品的价格")
    except Exception as e:
        print(f"  更新产品价格失败: {e}")
    
    # 2. 更新客户VIP等级
    print("\n2. 更新客户VIP等级（总消费大于10000的客户提升一级）...")
    try:
        # 查询所有高消费客户
        all_customers = session.execute("SELECT * FROM customers;")
        high_spend_customers = [c for c in all_customers if c[5].value > 10000]  # 第5列是total_spend
        
        # 逐个更新VIP等级
        update_count = 0
        for customer in high_spend_customers:
            customer_id = customer[0].value
            current_vip = customer[4].value
            if current_vip < 5:  # 最高是5级
                new_vip = current_vip + 1
                session.execute(f"UPDATE customers SET vip_level = {new_vip} WHERE customer_id = {customer_id};")
                update_count += 1
        
        print(f"  成功提升 {update_count} 个高消费客户的VIP等级")
    except Exception as e:
        print(f"  更新VIP等级失败: {e}")
    
    # 3. 更新订单状态
    print("\n3. 更新订单状态（将部分pending订单更新为confirmed）...")
    try:
        # 查询所有待处理订单
        all_orders = session.execute("SELECT * FROM orders;")
        pending_orders = [o for o in all_orders if o[3].value == "pending"]
        
        # 随机选择50%的订单进行更新
        update_orders = random.sample(pending_orders, len(pending_orders) // 2)
        
        # 逐个更新订单状态
        update_count = 0
        for order in update_orders:
            order_id = order[0].value
            session.execute(f"UPDATE orders SET status = 'confirmed' WHERE order_id = {order_id};")
            update_count += 1
        
        print(f"  成功更新 {update_count} 个订单的状态从pending到confirmed")
    except Exception as e:
        print(f"  更新订单状态失败: {e}")
    
    # 4. 更新库存（减少被订购产品的库存）
    print("\n4. 更新库存（减少被订购产品的库存）...")
    try:
        # 查询所有订单项
        order_items_data = session.execute("SELECT * FROM order_items;")
        
        # 计算每个产品的订购数量
        product_quantities = {}
        for item in order_items_data:
            product_id = item[2].value  # 第2列是product_id
            quantity = item[3].value    # 第3列是quantity
            
            if product_id in product_quantities:
                product_quantities[product_id] += quantity
            else:
                product_quantities[product_id] = quantity
        
        # 更新产品库存
        update_count = 0
        for product_id, ordered_quantity in product_quantities.items():
            # 查询当前库存
            product_result = session.execute(f"SELECT * FROM products WHERE product_id = {product_id};")
            if product_result and len(product_result) > 0:
                current_stock = product_result[0][4].value  # 第4列是stock
                
                # 确保库存不会为负数
                new_stock = max(0, current_stock - ordered_quantity)
                session.execute(f"UPDATE products SET stock = {new_stock} WHERE product_id = {product_id};")
                update_count += 1
        
        print(f"  成功更新 {update_count} 个产品的库存")
    except Exception as e:
        print(f"  更新库存失败: {e}")

def perform_deletes(session):
    """执行删除操作"""
    print("\n=== 执行删除操作 ===")
    
    # 1. 删除库存为0的产品
    print("1. 删除库存为0的产品...")
    try:
        # 查询所有库存为0的产品
        all_products = session.execute("SELECT * FROM products;")
        zero_stock_products = [p for p in all_products if p[4].value == 0]  # 第4列是stock
        
        # 删除这些产品
        delete_count = 0
        for product in zero_stock_products:
            product_id = product[0].value
            session.execute(f"DELETE FROM products WHERE product_id = {product_id};")
            delete_count += 1
        
        print(f"  成功删除 {delete_count} 个库存为0的产品")
    except Exception as e:
        print(f"  删除产品失败: {e}")
    
    # 2. 删除已取消的订单
    print("\n2. 删除已取消的订单...")
    try:
        # 查询所有已取消的订单
        all_orders = session.execute("SELECT * FROM orders;")
        cancelled_orders = [o for o in all_orders if o[3].value == "cancelled"]
        
        # 删除这些订单
        delete_count = 0
        for order in cancelled_orders:
            order_id = order[0].value
            
            # 删除相关的订单详情
            all_items = session.execute("SELECT * FROM order_items;")
            order_items = [item for item in all_items if item[1].value == order_id]
            
            for item in order_items:
                item_id = item[0].value
                session.execute(f"DELETE FROM order_items WHERE item_id = {item_id};")
            
            # 删除订单本身
            session.execute(f"DELETE FROM orders WHERE order_id = {order_id};")
            delete_count += 1
        
        print(f"  成功删除 {delete_count} 个已取消的订单及其详情")
    except Exception as e:
        print(f"  删除订单失败: {e}")
    
    # 3. 删除低VIP级别且长期未消费的客户
    print("\n3. 删除VIP级别为0且总消费小于100的客户...")
    try:
        # 查询符合条件的客户
        all_customers = session.execute("SELECT * FROM customers;")
        inactive_customers = [c for c in all_customers if c[4].value == 0 and c[5].value < 100]
        
        # 删除这些客户
        delete_count = 0
        for customer in inactive_customers:
            customer_id = customer[0].value
            session.execute(f"DELETE FROM customers WHERE customer_id = {customer_id};")
            delete_count += 1
        
        print(f"  成功删除 {delete_count} 个不活跃的低价值客户")
    except Exception as e:
        print(f"  删除客户失败: {e}")

def verify_data(session, original_summary):
    """验证数据一致性"""
    print("\n=== 验证数据一致性 ===")
    
    # 统计各表的当前记录数
    tables = ["products", "customers", "orders", "order_items"]
    current_summary = {}
    
    for table in tables:
        try:
            results = session.execute(f"SELECT * FROM {table};")
            count = len(results)
            current_summary[f"{table}_count"] = count
            print(f"  {table} 表: {count} 条记录")
        except Exception as e:
            print(f"  查询 {table} 表失败: {e}")
    
    # 计算平均每个订单的商品数量
    orders_count = current_summary.get("orders_count", 0)
    items_count = current_summary.get("order_items_count", 0)
    if orders_count > 0:
        current_summary["avg_items_per_order"] = items_count / orders_count
    else:
        current_summary["avg_items_per_order"] = 0
    
    # 查询更新后的数据状态
    
    # 1. 验证产品价格更新
    print("\n1. 验证电子类产品价格更新...")
    try:
        all_products = session.execute("SELECT * FROM products;")
        electronic_products = [p for p in all_products if p[2].value == "电子"]
        avg_price = sum(p[3].value for p in electronic_products) / len(electronic_products) if electronic_products else 0
        
        print(f"  当前电子类产品数量: {len(electronic_products)}")
        print(f"  当前电子类产品平均价格: {avg_price:.2f}")
    except Exception as e:
        print(f"  验证产品价格更新失败: {e}")
    
    # 2. 验证VIP客户更新
    print("\n2. 验证VIP客户更新...")
    try:
        all_customers = session.execute("SELECT * FROM customers;")
        high_vip_customers = [c for c in all_customers if c[4].value >= 4]  # VIP>=4
        
        print(f"  当前高级VIP客户数量: {len(high_vip_customers)}")
        if high_vip_customers:
            avg_spend = sum(c[5].value for c in high_vip_customers) / len(high_vip_customers)
            print(f"  高级VIP客户平均消费: {avg_spend:.2f}")
    except Exception as e:
        print(f"  验证VIP客户更新失败: {e}")
    
    # 3. 验证订单状态更新
    print("\n3. 验证订单状态更新...")
    try:
        all_orders = session.execute("SELECT * FROM orders;")
        status_counts = {}
        for order in all_orders:
            status = order[3].value
            if status in status_counts:
                status_counts[status] += 1
            else:
                status_counts[status] = 1
        
        print("  当前订单状态分布:")
        for status, count in status_counts.items():
            percentage = count / len(all_orders) * 100 if all_orders else 0
            print(f"    {status}: {count} 个订单 ({percentage:.1f}%)")
    except Exception as e:
        print(f"  验证订单状态更新失败: {e}")
    
    # 4. 验证库存更新
    print("\n4. 验证产品库存更新...")
    try:
        all_products = session.execute("SELECT * FROM products;")
        zero_stock = [p for p in all_products if p[4].value == 0]
        
        print(f"  当前库存为0的产品数量: {len(zero_stock)}")
        
        # 计算库存统计信息
        stock_values = [p[4].value for p in all_products]
        if stock_values:
            avg_stock = sum(stock_values) / len(stock_values)
            max_stock = max(stock_values)
            min_stock = min(stock_values)
            
            print(f"  当前产品库存统计: 平均={avg_stock:.2f}, 最大={max_stock}, 最小={min_stock}")
    except Exception as e:
        print(f"  验证产品库存更新失败: {e}")
    
    # 总结数据变化
    print("\n数据一致性验证完成")
    print("原始数据量 vs 当前数据量:")
    for key in original_summary:
        original = original_summary.get(key, 0)
        current = current_summary.get(key, 0)
        change = current - original
        change_percent = (change / original * 100) if original != 0 else 0
        
        # 对于avg_items_per_order，保留两位小数
        if key == "avg_items_per_order":
            print(f"  {key}: {original:.2f} → {current:.2f} ({change:+.2f}, {change_percent:+.1f}%)")
        else:
            print(f"  {key}: {original} → {current} ({change:+.0f}, {change_percent:+.1f}%)")

def run_batch_test(db_path):
    """运行批量操作测试"""
    print("=== 开始批量操作测试 ===")
    print(f"使用数据库文件: {db_path}")
    
    # 第一阶段：初始化数据库并创建表结构
    print("\n第一阶段：初始化数据库并创建表结构...")
    
    # 创建数据库引擎
    storage_engine = DiskEngine(db_path)
    kv_engine = KVEngine(storage_engine)
    transaction = kv_engine.begin()
    session = Session(transaction)
    
    try:
        # 创建表结构
        create_schemas(session)
        
        # 批量插入数据
        data_summary = batch_insert_data(session, db_path)
        
        # 执行查询操作
        perform_queries(session)
        
        # 执行更新操作
        perform_updates(session)
        
        # 执行删除操作
        perform_deletes(session)
        
        # 提交事务
        print("\n提交第一阶段事务...")
        transaction.commit()
        print("第一阶段事务已提交")
        
    except Exception as e:
        # 发生错误时回滚事务
        print(f"\n发生错误: {e}")
        print("回滚事务...")
        transaction.rollback()
        print("事务已回滚")
        raise
    finally:
        # 关闭第一阶段的数据库连接
        print("关闭第一阶段数据库连接...")
        storage_engine.close()
    
    # 模拟数据库关闭一段时间
    print("\n模拟数据库关闭一段时间...")
    time.sleep(2)
    
    # 第二阶段：重新打开数据库并验证数据
    print("\n第二阶段：重新打开数据库并验证数据...")
    
    # 重新打开数据库
    storage_engine = DiskEngine(db_path)
    kv_engine = KVEngine(storage_engine)
    transaction = kv_engine.begin()
    session = Session(transaction)
    
    try:
        # 验证数据一致性
        verify_data(session, data_summary)
        
        # 提交事务（只读事务）
        print("\n提交第二阶段事务...")
        transaction.commit()
        print("第二阶段事务已提交")
        
    except Exception as e:
        # 发生错误时回滚事务
        print(f"\n发生错误: {e}")
        print("回滚事务...")
        transaction.rollback()
        print("事务已回滚")
        raise
    finally:
        # 关闭第二阶段的数据库连接
        print("关闭第二阶段数据库连接...")
        storage_engine.close()
    
    print("\n批量操作测试完成")

def main():
    """主函数，供run_all_examples.py调用"""
    # 使用当前目录下的临时数据库文件
    db_file = os.path.join(os.path.dirname(__file__), "batch_operations.db")
    
    try:
        # 检查数据库文件是否存在，如果存在则删除
        if os.path.exists(db_file):
            print(f"发现已存在的数据库文件，正在删除: {db_file}")
            os.unlink(db_file)
            print("旧数据库文件已删除")
        
        # 运行批量操作测试
        run_batch_test(db_file)
    finally:
        # 保留数据库文件用于后续检查
        print(f"\n保留数据库文件: {db_file}")
        print("您可以手动删除该文件，或在下次运行示例时自动覆盖")

if __name__ == "__main__":
    main()
