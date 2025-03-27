#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据持久化示例
===========

这个示例展示如何在cooSql中实现数据的持久化，包括关闭数据库后重新打开并查询数据。
"""

import os
import sys
import time

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from storage.disk import DiskEngine
from sql.engine.kv import KVEngine
from sql.session import Session

def create_database(db_path):
    """创建数据库并初始化数据"""
    print("\n=== 第一阶段：创建数据库和初始化数据 ===")
    
    # 初始化存储引擎和SQL会话
    storage_engine = DiskEngine(db_path)
    kv_engine = KVEngine(storage_engine)
    transaction = kv_engine.begin()
    session = Session(transaction)
    
    try:
        # 先检查表是否已存在，如果存在则删除
        tables_to_check = ["students", "courses", "enrollments"]
        for table_name in tables_to_check:
            try:
                session.execute(f"DROP TABLE IF EXISTS {table_name};")
                print(f"检查到表 {table_name} 已存在，已删除")
            except Exception as e:
                # 忽略表不存在的错误
                pass
        
        # 创建学生表
        print("创建学生表...")
        session.execute("""
        CREATE TABLE students (
            student_id INTEGER NOT NULL,
            name STRING NOT NULL,
            gender STRING,
            age INTEGER DEFAULT 18,
            major STRING,
            gpa FLOAT DEFAULT 0.0
        );
        """)
        
        # 创建课程表
        print("创建课程表...")
        session.execute("""
        CREATE TABLE courses (
            course_id INTEGER NOT NULL,
            title STRING NOT NULL,
            credits INTEGER DEFAULT 3,
            instructor STRING,
            department STRING
        );
        """)
        
        # 创建选课表
        print("创建选课表...")
        session.execute("""
        CREATE TABLE enrollments (
            enrollment_id INTEGER NOT NULL,
            student_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            semester STRING NOT NULL,
            grade FLOAT DEFAULT 0.0
        );
        """)
        
        # 插入学生数据
        print("\n插入学生数据...")
        session.execute("INSERT INTO students VALUES (10001, '王小明', '男', 20, '计算机科学', 3.8);")
        session.execute("INSERT INTO students VALUES (10002, '李小红', '女', 19, '数学', 3.9);")
        session.execute("INSERT INTO students VALUES (10003, '张小华', '男', 21, '物理', 3.7);")
        session.execute("INSERT INTO students VALUES (10004, '赵小燕', '女', 20, '化学', 3.6);")
        session.execute("INSERT INTO students VALUES (10005, '刘小军', '男', 22, '计算机科学', 3.5);")
        
        # 插入课程数据
        print("插入课程数据...")
        session.execute("INSERT INTO courses VALUES (2001, '数据结构', 4, '陈教授', '计算机科学');")
        session.execute("INSERT INTO courses VALUES (2002, '高等数学', 5, '李教授', '数学');")
        session.execute("INSERT INTO courses VALUES (2003, '量子力学', 4, '张教授', '物理');")
        session.execute("INSERT INTO courses VALUES (2004, '有机化学', 3, '黄教授', '化学');")
        session.execute("INSERT INTO courses VALUES (2005, '数据库原理', 4, '王教授', '计算机科学');")
        
        # 插入选课数据
        print("插入选课数据...")
        session.execute("INSERT INTO enrollments VALUES (1, 10001, 2001, '2023秋季', 92.5);")
        session.execute("INSERT INTO enrollments VALUES (2, 10001, 2005, '2023秋季', 88.0);")
        session.execute("INSERT INTO enrollments VALUES (3, 10002, 2002, '2023秋季', 95.0);")
        session.execute("INSERT INTO enrollments VALUES (4, 10003, 2003, '2023秋季', 87.5);")
        session.execute("INSERT INTO enrollments VALUES (5, 10004, 2004, '2023秋季', 90.0);")
        session.execute("INSERT INTO enrollments VALUES (6, 10005, 2001, '2023秋季', 85.0);")
        session.execute("INSERT INTO enrollments VALUES (7, 10005, 2005, '2023秋季', 82.5);")
        
        # 查询初始数据
        print("\n查询初始学生数据...")
        students = session.execute("SELECT * FROM students;")
        print_table(students, ["学号", "姓名", "性别", "年龄", "专业", "GPA"])
        
        print("\n查询初始课程数据...")
        courses = session.execute("SELECT * FROM courses;")
        print_table(courses, ["课程ID", "课程名称", "学分", "教师", "所属系"])
        
        print("\n查询初始选课数据...")
        enrollments = session.execute("SELECT * FROM enrollments;")
        print_table(enrollments, ["选课ID", "学生ID", "课程ID", "学期", "成绩"])
        
        # 提交事务
        transaction.commit()
        print("\n数据库初始化完成，事务已提交")
        
    except Exception as e:
        # 发生错误时回滚事务
        transaction.rollback()
        print(f"发生错误，事务已回滚: {e}")
        raise
    finally:
        # 关闭资源
        print("关闭数据库连接...")
        storage_engine.close()

def modify_database(db_path):
    """重新打开数据库并进行修改"""
    print("\n=== 第二阶段：重新打开数据库并修改数据 ===")
    
    # 重新打开数据库
    storage_engine = DiskEngine(db_path)
    kv_engine = KVEngine(storage_engine)
    transaction = kv_engine.begin()
    session = Session(transaction)
    
    try:
        # 验证数据库中的表是否存在
        print("验证学生表数据...")
        students = session.execute("SELECT * FROM students;")
        if len(students) > 0:
            print(f"成功读取 {len(students)} 条学生记录")
        
        # 添加新的学生
        print("\n添加新学生...")
        session.execute("INSERT INTO students VALUES (10006, '陈小林', '男', 19, '人工智能', 3.9);")
        session.execute("INSERT INTO students VALUES (10007, '郑小婷', '女', 20, '计算机科学', 4.0);")
        
        # 更新现有学生的GPA
        print("更新学生GPA...")
        session.execute("UPDATE students SET gpa = 3.95 WHERE student_id = 10001;")
        
        # 添加新的选课记录
        print("添加新的选课记录...")
        session.execute("INSERT INTO enrollments VALUES (8, 10006, 2001, '2023秋季', 94.0);")
        session.execute("INSERT INTO enrollments VALUES (9, 10006, 2005, '2023秋季', 96.5);")
        session.execute("INSERT INTO enrollments VALUES (10, 10007, 2001, '2023秋季', 98.0);")
        
        # 查看更新后的学生数据
        print("\n查询更新后的学生数据...")
        updated_students = session.execute("SELECT * FROM students;")
        print_table(updated_students, ["学号", "姓名", "性别", "年龄", "专业", "GPA"])
        
        # 查看更新后的选课数据
        print("\n查询更新后的选课数据...")
        updated_enrollments = session.execute("SELECT * FROM enrollments;")
        print_table(updated_enrollments, ["选课ID", "学生ID", "课程ID", "学期", "成绩"])
        
        # 提交事务
        transaction.commit()
        print("\n数据修改完成，事务已提交")
        
    except Exception as e:
        # 发生错误时回滚事务
        transaction.rollback()
        print(f"发生错误，事务已回滚: {e}")
        raise
    finally:
        # 关闭资源
        print("关闭数据库连接...")
        storage_engine.close()

def query_database(db_path):
    """重新打开数据库并查询数据"""
    print("\n=== 第三阶段：重新打开数据库并查询数据 ===")
    
    # 重新打开数据库
    storage_engine = DiskEngine(db_path)
    kv_engine = KVEngine(storage_engine)
    transaction = kv_engine.begin()
    session = Session(transaction)
    
    try:
        # 查询所有表的数据，验证持久化
        print("查询所有学生数据...")
        all_students = session.execute("SELECT * FROM students;")
        print_table(all_students, ["学号", "姓名", "性别", "年龄", "专业", "GPA"])
        
        print("\n查询所有课程数据...")
        all_courses = session.execute("SELECT * FROM courses;")
        print_table(all_courses, ["课程ID", "课程名称", "学分", "教师", "所属系"])
        
        print("\n查询所有选课数据...")
        all_enrollments = session.execute("SELECT * FROM enrollments;")
        print_table(all_enrollments, ["选课ID", "学生ID", "课程ID", "学期", "成绩"])
        
        # 执行一些高级查询
        print("\n查询计算机科学专业的学生...")
        cs_students = session.execute("SELECT * FROM students WHERE major = '计算机科学';")
        print_table(cs_students, ["学号", "姓名", "性别", "年龄", "专业", "GPA"])
        
        print("\n查询GPA大于3.8的学生...")
        high_gpa_students = session.execute("SELECT * FROM students WHERE gpa > 3.8;")
        print_table(high_gpa_students, ["学号", "姓名", "性别", "年龄", "专业", "GPA"])
        
        print("\n查询选修了数据结构课程的学生...")
        # 由于当前引擎不支持列选择，先获取完整数据再筛选
        
        # 1. 找到"数据结构"课程的ID
        all_courses = session.execute("SELECT * FROM courses;")
        course_id = None
        for course in all_courses:
            if course[1].value == '数据结构':  # 1是课程名称列
                course_id = course[0].value
                break
                
        if course_id:
            # 2. 找到选修了该课程的所有选课记录
            all_enrollments = session.execute("SELECT * FROM enrollments;")
            student_ids = []
            for enrollment in all_enrollments:
                if enrollment[2].value == course_id:  # 2是课程ID列
                    student_ids.append(enrollment[1].value)  # 1是学生ID列
            
            # 3. 获取这些学生的信息
            print("学生ID\t姓名")
            print("-------------------")
            all_students = session.execute("SELECT * FROM students;")
            for student in all_students:
                if student[0].value in student_ids:  # 0是学生ID列
                    print(f"{student[0].value}\t{student[1].value}")
        else:
            print("未找到'数据结构'课程")
        
        # 提交事务（只读事务）
        transaction.commit()
        print("\n查询完成")
        
    except Exception as e:
        # 发生错误时回滚事务
        transaction.rollback()
        print(f"发生错误，事务已回滚: {e}")
        raise
    finally:
        # 关闭资源
        print("关闭数据库连接...")
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
    # 使用当前目录下的持久化数据库文件
    db_file = os.path.join(os.path.dirname(__file__), "persistence_example.db")
    
    try:
        # 检查数据库文件是否存在，如果存在则删除
        if os.path.exists(db_file):
            print(f"发现已存在的数据库文件，正在删除: {db_file}")
            os.unlink(db_file)
            print("旧数据库文件已删除")
        
        # 第一阶段：创建数据库并初始化数据
        create_database(db_file)
        
        # 模拟数据库关闭一段时间
        print("\n模拟数据库关闭一段时间...")
        time.sleep(2)
        
        # 第二阶段：重新打开数据库并修改数据
        modify_database(db_file)
        
        # 再次模拟数据库关闭
        print("\n再次模拟数据库关闭...")
        time.sleep(2)
        
        # 第三阶段：重新打开数据库并查询数据
        query_database(db_file)
        
    finally:
        # 保留数据库文件用于后续检查
        print(f"\n保留数据库文件: {db_file}")
        print("您可以手动删除该文件，或在下次运行示例时自动覆盖")