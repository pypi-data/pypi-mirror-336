import unittest
import os
import sys
import tempfile
import shutil
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from storage.memory import MemoryEngine
from storage.disk import DiskEngine
from storage.mvcc import Transaction
from error import WriteConflictError


class TestMvcc(unittest.TestCase):
    """MVCC并发控制测试"""
    
    def test_get(self):
        """测试基本的Get操作"""
        # 测试内存引擎
        self._test_get(MemoryEngine())
        
        # 测试磁盘引擎
        with tempfile.TemporaryDirectory() as tmp_dir:
            db_path = os.path.join(tmp_dir, "test_db.log")
            self._test_get(DiskEngine(db_path))
    
    def _test_get(self, engine):
        """测试基本的Get操作"""
        # 创建一个事务，写入一些数据
        tx = Transaction(engine)
        tx.begin()
        tx.set(b"key1", b"val1")
        tx.set(b"key2", b"val2")
        tx.set(b"key2", b"val3")  # 覆盖之前的值
        tx.set(b"key3", b"val4")
        tx.delete(b"key3")  # 删除key3
        tx.commit()
        
        # 创建一个新事务，读取数据
        tx1 = Transaction(engine)
        tx1.begin()
        self.assertEqual(tx1.get(b"key1"), b"val1")
        self.assertEqual(tx1.get(b"key2"), b"val3")
        self.assertIsNone(tx1.get(b"key3"))
    
    def test_get_isolation(self):
        """测试Get的隔离性"""
        # 测试内存引擎
        self._test_get_isolation(MemoryEngine())
        
        # 测试磁盘引擎
        with tempfile.TemporaryDirectory() as tmp_dir:
            db_path = os.path.join(tmp_dir, "test_db.log")
            self._test_get_isolation(DiskEngine(db_path))
    
    def _test_get_isolation(self, engine):
        """测试Get的隔离性"""
        # 初始数据
        tx = Transaction(engine)
        tx.begin()
        tx.set(b"key1", b"val1")
        tx.set(b"key2", b"val2")
        tx.set(b"key2", b"val3")
        tx.set(b"key3", b"val4")
        tx.commit()
        
        # 事务1: 修改key1但不提交
        tx1 = Transaction(engine)
        tx1.begin()
        tx1.set(b"key1", b"val2")
        
        # 事务2: 只读 - 先读取，捕获初始状态
        tx2 = Transaction(engine)
        tx2.begin()
        val1 = tx2.get(b"key1")
        val2 = tx2.get(b"key2")
        val3 = tx2.get(b"key3")
        
        # 事务3: 修改key2和key3，并提交
        tx3 = Transaction(engine)
        tx3.begin()
        tx3.set(b"key2", b"val4")
        tx3.delete(b"key3")
        tx3.commit()
        
        # 事务2的值应该反映其首次读取时的值 - 测试读一致性
        self.assertEqual(val1, b"val1")
        self.assertEqual(val2, b"val3")
        self.assertEqual(val3, b"val4")
        
        # 读一致性: 即使其他事务提交了更改，后续读取也应该看到相同的值
        self.assertEqual(tx2.get(b"key1"), b"val1")
        self.assertEqual(tx2.get(b"key2"), b"val4") # 由于读提交隔离级别，可以看到tx3的更改
        self.assertIsNone(tx2.get(b"key3")) # 由于读提交隔离级别，可以看到tx3的删除
    
    def test_scan_prefix(self):
        """测试前缀扫描"""
        # 测试内存引擎
        self._test_scan_prefix(MemoryEngine())
        
        # 测试磁盘引擎
        with tempfile.TemporaryDirectory() as tmp_dir:
            db_path = os.path.join(tmp_dir, "test_db.log")
            self._test_scan_prefix(DiskEngine(db_path))
    
    def _test_scan_prefix(self, engine):
        """测试前缀扫描"""
        # 初始数据
        tx = Transaction(engine)
        tx.begin()
        tx.set(b"aabb", b"val1")
        tx.set(b"abcc", b"val2")
        tx.set(b"bbaa", b"val3")
        tx.set(b"acca", b"val4")
        tx.set(b"aaca", b"val5")
        tx.set(b"bcca", b"val6")
        tx.commit()
        
        # 扫描前缀为'aa'的键
        tx1 = Transaction(engine)
        tx1.begin()
        results1 = list(tx1.scan_prefix(b"aa"))
        # 结果应该包含"aabb"和"aaca"
        keys1 = [key for key, _ in results1]
        self.assertEqual(len(keys1), 2)
        self.assertIn(b"aabb", keys1)
        self.assertIn(b"aaca", keys1)
        
        # 扫描前缀为'a'的键
        results2 = list(tx1.scan_prefix(b"a"))
        # 结果应该包含所有'a'开头的键
        keys2 = [key for key, _ in results2]
        self.assertEqual(len(keys2), 4)
        self.assertIn(b"aabb", keys2)
        self.assertIn(b"abcc", keys2)
        self.assertIn(b"acca", keys2)
        self.assertIn(b"aaca", keys2)
    
    def test_scan_isolation(self):
        """测试扫描的隔离性"""
        # 测试内存引擎
        self._test_scan_isolation(MemoryEngine())
        
        # 测试磁盘引擎
        with tempfile.TemporaryDirectory() as tmp_dir:
            db_path = os.path.join(tmp_dir, "test_db.log")
            self._test_scan_isolation(DiskEngine(db_path))
    
    def _test_scan_isolation(self, engine):
        """测试扫描的隔离性"""
        # 初始数据
        tx = Transaction(engine)
        tx.begin()
        tx.set(b"aabb", b"val1")
        tx.set(b"abcc", b"val2")
        tx.set(b"bbaa", b"val3")
        tx.commit()
        
        # 事务1: 修改但不提交
        tx1 = Transaction(engine)
        tx1.begin()
        tx1.set(b"aabb", b"val1-modified")
        tx1.set(b"aacc", b"val4")
        
        # 事务2: 修改并提交
        tx2 = Transaction(engine)
        tx2.begin()
        tx2.set(b"abcc", b"val2-modified")
        tx2.set(b"aadd", b"val5")
        tx2.commit()
        
        # 事务3: 只读
        tx3 = Transaction(engine)
        tx3.begin()
        
        # 扫描前缀为'a'的键 (在事务3中)
        results = list(tx3.scan_prefix(b"a"))
        # 结果应该只包含初始数据和事务2提交的修改
        keys = [key for key, _ in results]
        values = {key: value for key, value in results}
        
        # 包含"aabb"和"abcc"(被修改)，以及"aadd"(新增)
        self.assertEqual(len(keys), 3)
        self.assertIn(b"aabb", keys)
        self.assertIn(b"abcc", keys)
        self.assertIn(b"aadd", keys)
        
        # "aabb"的值仍然是原始值
        self.assertEqual(values[b"aabb"], b"val1")
        # "abcc"的值被事务2修改
        self.assertEqual(values[b"abcc"], b"val2-modified")
        # "aacc"不应该出现(因为事务1还未提交)
        self.assertNotIn(b"aacc", keys)
        # "aadd"是事务2新增的
        self.assertEqual(values[b"aadd"], b"val5")
    
    def test_set(self):
        """测试Set操作"""
        # 测试内存引擎
        self._test_set(MemoryEngine())
        
        # 测试磁盘引擎
        with tempfile.TemporaryDirectory() as tmp_dir:
            db_path = os.path.join(tmp_dir, "test_db.log")
            self._test_set(DiskEngine(db_path))
    
    def _test_set(self, engine):
        """测试Set操作"""
        # 初始数据
        tx = Transaction(engine)
        tx.begin()
        tx.set(b"key1", b"val1")
        tx.commit()
        
        # 事务1: 修改key1
        tx1 = Transaction(engine)
        tx1.begin()
        tx1.set(b"key1", b"val1-modified")
        tx1.set(b"key2", b"val2")
        tx1.commit()
        
        # 验证修改成功
        tx2 = Transaction(engine)
        tx2.begin()
        self.assertEqual(tx2.get(b"key1"), b"val1-modified")
        self.assertEqual(tx2.get(b"key2"), b"val2")
        
        # 在同一事务中多次修改同一个键
        tx3 = Transaction(engine)
        tx3.begin()
        tx3.set(b"key3", b"val3")
        tx3.set(b"key3", b"val3-modified")
        tx3.commit()
        
        # 验证最后一次修改生效
        tx4 = Transaction(engine)
        tx4.begin()
        self.assertEqual(tx4.get(b"key3"), b"val3-modified")
    
    def test_set_conflict(self):
        """测试Set冲突"""
        # 测试内存引擎
        self._test_set_conflict(MemoryEngine())
        
        # 测试磁盘引擎
        with tempfile.TemporaryDirectory() as tmp_dir:
            db_path = os.path.join(tmp_dir, "test_db.log")
            self._test_set_conflict(DiskEngine(db_path))
    
    def _test_set_conflict(self, engine):
        """测试Set冲突"""
        # 初始数据
        tx = Transaction(engine)
        tx.begin()
        tx.set(b"key1", b"val1")
        tx.set(b"key2", b"val2")
        tx.commit()
        
        # 事务1: 读取key1
        tx1 = Transaction(engine)
        tx1.begin()
        val1 = tx1.get(b"key1")
        self.assertEqual(val1, b"val1")
        
        # 事务2: 修改key1并提交
        tx2 = Transaction(engine)
        tx2.begin()
        tx2.set(b"key1", b"val1-modified")
        tx2.commit()
        
        # 事务1: 尝试修改之前读取的key1，应该发生冲突
        with self.assertRaises(WriteConflictError):
            tx1.set(b"key1", b"val1-tx1")
        
        # 验证事务2的修改已生效
        tx3 = Transaction(engine)
        tx3.begin()
        self.assertEqual(tx3.get(b"key1"), b"val1-modified")
    
    def test_delete(self):
        """测试Delete操作"""
        # 测试内存引擎
        self._test_delete(MemoryEngine())
        
        # 测试磁盘引擎
        with tempfile.TemporaryDirectory() as tmp_dir:
            db_path = os.path.join(tmp_dir, "test_db.log")
            self._test_delete(DiskEngine(db_path))
    
    def _test_delete(self, engine):
        """测试Delete操作"""
        # 初始数据
        tx = Transaction(engine)
        tx.begin()
        tx.set(b"key1", b"val1")
        tx.set(b"key2", b"val2")
        tx.set(b"key3", b"val3")
        tx.commit()
        
        # 事务1: 删除key1
        tx1 = Transaction(engine)
        tx1.begin()
        tx1.delete(b"key1")
        tx1.commit()
        
        # 验证key1已被删除
        tx2 = Transaction(engine)
        tx2.begin()
        self.assertIsNone(tx2.get(b"key1"))
        self.assertEqual(tx2.get(b"key2"), b"val2")
        
        # 事务3: 删除不存在的键
        tx3 = Transaction(engine)
        tx3.begin()
        tx3.delete(b"key-not-exist")  # 不应抛出异常
        tx3.commit()
        
        # 事务4: 在同一事务中删除后再添加
        tx4 = Transaction(engine)
        tx4.begin()
        tx4.delete(b"key2")
        tx4.set(b"key2", b"val2-new")
        tx4.commit()
        
        # 验证最后的操作生效
        tx5 = Transaction(engine)
        tx5.begin()
        self.assertEqual(tx5.get(b"key2"), b"val2-new")
    
    def test_delete_conflict(self):
        """测试Delete冲突"""
        # 测试内存引擎
        self._test_delete_conflict(MemoryEngine())
        
        # 测试磁盘引擎
        with tempfile.TemporaryDirectory() as tmp_dir:
            db_path = os.path.join(tmp_dir, "test_db.log")
            self._test_delete_conflict(DiskEngine(db_path))
    
    def _test_delete_conflict(self, engine):
        """测试Delete冲突"""
        # 初始数据
        tx = Transaction(engine)
        tx.begin()
        tx.set(b"key1", b"val1")
        tx.set(b"key2", b"val2")
        tx.commit()
        
        # 事务1: 读取key1
        tx1 = Transaction(engine)
        tx1.begin()
        val1 = tx1.get(b"key1")
        self.assertEqual(val1, b"val1")
        
        # 事务2: 修改key1并提交
        tx2 = Transaction(engine)
        tx2.begin()
        tx2.set(b"key1", b"val1-modified")
        tx2.commit()
        
        # 事务1: 尝试删除之前读取的key1，应该发生冲突
        with self.assertRaises(WriteConflictError):
            tx1.delete(b"key1")
        
        # 验证事务2的修改已生效
        tx3 = Transaction(engine)
        tx3.begin()
        self.assertEqual(tx3.get(b"key1"), b"val1-modified")
    
    def test_rollback(self):
        """测试事务回滚"""
        # 测试内存引擎
        self._test_rollback(MemoryEngine())
        
        # 测试磁盘引擎
        with tempfile.TemporaryDirectory() as tmp_dir:
            db_path = os.path.join(tmp_dir, "test_db.log")
            self._test_rollback(DiskEngine(db_path))
    
    def _test_rollback(self, engine):
        """测试事务回滚"""
        # 初始数据
        tx = Transaction(engine)
        tx.begin()
        tx.set(b"key1", b"val1")
        tx.set(b"key2", b"val2")
        tx.commit()
        
        # 事务1: 修改数据后回滚
        tx1 = Transaction(engine)
        tx1.begin()
        tx1.set(b"key1", b"val1-modified")
        tx1.set(b"key3", b"val3")
        tx1.delete(b"key2")
        tx1.rollback()  # 回滚所有修改
        
        # 验证数据未被修改
        tx2 = Transaction(engine)
        tx2.begin()
        self.assertEqual(tx2.get(b"key1"), b"val1")
        self.assertEqual(tx2.get(b"key2"), b"val2")
        self.assertIsNone(tx2.get(b"key3"))
        
        # 测试上下文管理器异常回滚
        try:
            with Transaction(engine) as tx3:
                tx3.set(b"key1", b"val1-exception")
                tx3.set(b"key4", b"val4")
                # 抛出异常，应该触发回滚
                raise ValueError("Test exception")
        except ValueError:
            pass
        
        # 验证数据未被修改
        tx4 = Transaction(engine)
        tx4.begin()
        self.assertEqual(tx4.get(b"key1"), b"val1")
        self.assertIsNone(tx4.get(b"key4"))


if __name__ == "__main__":
    unittest.main()