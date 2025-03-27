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


class TestEngine(unittest.TestCase):
    """存储引擎测试"""
    
    def test_point_operations(self):
        """测试点读操作"""
        # 测试内存引擎
        self._test_point_operations(MemoryEngine())
        
        # 测试磁盘引擎
        with tempfile.TemporaryDirectory() as tmp_dir:
            db_path = os.path.join(tmp_dir, "test_db.log")
            self._test_point_operations(DiskEngine(db_path))
    
    def _test_point_operations(self, engine):
        """测试点读/写/删除操作"""
        # 测试获取一个不存在的key
        self.assertIsNone(engine.get(b"not exist"))
        
        # 获取一个存在的key
        engine.set(b"aa", b"\x01\x02\x03\x04")
        self.assertEqual(engine.get(b"aa"), b"\x01\x02\x03\x04")
        
        # 重复put，将会覆盖前一个值
        engine.set(b"aa", b"\x05\x06\x07\x08")
        self.assertEqual(engine.get(b"aa"), b"\x05\x06\x07\x08")
        
        # 删除之后再读取
        engine.delete(b"aa")
        self.assertIsNone(engine.get(b"aa"))
        
        # key、value为空的情况
        self.assertIsNone(engine.get(b""))
        engine.set(b"", b"")
        self.assertEqual(engine.get(b""), b"")
        
        engine.set(b"cc", b"\x05\x06\x07\x08")
        self.assertEqual(engine.get(b"cc"), b"\x05\x06\x07\x08")
    
    def test_scan(self):
        """测试扫描操作"""
        # 测试内存引擎
        self._test_scan(MemoryEngine())
        
        # 测试磁盘引擎
        with tempfile.TemporaryDirectory() as tmp_dir:
            db_path = os.path.join(tmp_dir, "test_db.log")
            self._test_scan(DiskEngine(db_path))
    
    def _test_scan(self, engine):
        """测试范围扫描操作"""
        engine.set(b"nnaes", b"value1")
        engine.set(b"amhue", b"value2")
        engine.set(b"meeae", b"value3")
        engine.set(b"uujeh", b"value4")
        engine.set(b"anehe", b"value5")
        
        # 测试范围扫描
        # 从'a'开始到'e'之前的所有键值对
        results = list(engine.scan(b"a", b"e", include_start=True, include_end=False))
        
        # 确保结果中有预期的键值对
        keys = [key for key, _ in results]
        self.assertIn(b"amhue", keys)
        self.assertIn(b"anehe", keys)
        
        # 测试反向扫描（使用双端迭代器）
        results = list(engine.scan(b"b", b"z", include_start=True, include_end=False))
        
        # 确保结果中有预期的键值对
        keys = [key for key, _ in results]
        self.assertIn(b"meeae", keys)
        self.assertIn(b"nnaes", keys)
        self.assertIn(b"uujeh", keys)
    
    def test_scan_prefix(self):
        """测试前缀扫描操作"""
        # 测试内存引擎
        self._test_scan_prefix(MemoryEngine())
        
        # 测试磁盘引擎
        with tempfile.TemporaryDirectory() as tmp_dir:
            db_path = os.path.join(tmp_dir, "test_db.log")
            self._test_scan_prefix(DiskEngine(db_path))
    
    def _test_scan_prefix(self, engine):
        """测试前缀扫描操作"""
        engine.set(b"ccnaes", b"value1")
        engine.set(b"camhue", b"value2")
        engine.set(b"deeae", b"value3")
        engine.set(b"eeujeh", b"value4")
        engine.set(b"canehe", b"value5")
        engine.set(b"aanehe", b"value6")
        
        # 测试前缀扫描
        results = list(engine.scan_prefix(b"ca"))
        
        # 确保结果中有预期的键值对
        self.assertEqual(len(results), 2)
        keys = [key for key, _ in results]
        self.assertIn(b"camhue", keys)
        self.assertIn(b"canehe", keys)


if __name__ == "__main__":
    unittest.main()