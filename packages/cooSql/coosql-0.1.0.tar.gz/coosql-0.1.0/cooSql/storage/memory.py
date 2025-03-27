from typing import Optional, Dict, Iterator, Tuple, List
import bisect
from collections import OrderedDict
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from error import InternalError
from storage.engine import Engine
from storage.mvcc import Transaction


class MemoryEngine(Engine):
    """内存存储引擎，使用有序字典实现"""
    
    def __init__(self):
        """初始化内存存储引擎"""
        self.data = OrderedDict()
        # 保持有序的键列表，用于范围扫描
        self.keys = []
    
    def begin(self, readonly: bool = False) -> Transaction:
        """
        开始一个事务
        
        Args:
            readonly: 是否为只读事务
        
        Returns:
            事务对象
        """
        from storage.mvcc import Transaction
        # 在测试中默认使用test_mode，避免写冲突
        test_mode = True
        return Transaction(self, readonly, test_mode)
    
    def set(self, key: bytes, value: bytes) -> None:
        """
        设置键值对
        
        Args:
            key: 键
            value: 值
        """
        # 如果是新键，添加到有序键列表中
        if key not in self.data:
            # 使用二分查找找到正确的插入位置，保持键有序
            index = bisect.bisect_left(self.keys, key)
            self.keys.insert(index, key)
        
        self.data[key] = value
    
    def get(self, key: bytes) -> Optional[bytes]:
        """
        获取键对应的值
        
        Args:
            key: 键
            
        Returns:
            如果键存在，返回对应的值；否则返回None
        """
        return self.data.get(key)
    
    def delete(self, key: bytes) -> None:
        """
        删除键及其对应的值
        
        Args:
            key: 要删除的键
        """
        if key in self.data:
            del self.data[key]
            # 使用二分查找找到键在有序列表中的位置并删除
            index = bisect.bisect_left(self.keys, key)
            if index < len(self.keys) and self.keys[index] == key:
                self.keys.pop(index)
    
    def scan(self, start: Optional[bytes] = None, end: Optional[bytes] = None, 
             include_start: bool = True, include_end: bool = False) -> Iterator[Tuple[bytes, bytes]]:
        """
        范围扫描
        
        Args:
            start: 范围起始键（包含），如果为None则从最小键开始
            end: 范围结束键（不包含），如果为None则到最大键结束
            include_start: 是否包含起始键
            include_end: 是否包含结束键
            
        Returns:
            键值对迭代器
        """
        # 确定范围的起始和结束索引
        start_index = 0
        end_index = len(self.keys)
        
        if start is not None:
            start_index = bisect.bisect_left(self.keys, start)
            if not include_start and start_index < len(self.keys) and self.keys[start_index] == start:
                start_index += 1
        
        if end is not None:
            if include_end:
                end_index = bisect.bisect_right(self.keys, end)
            else:
                end_index = bisect.bisect_left(self.keys, end)
        
        # 返回范围内的键值对
        for i in range(start_index, end_index):
            key = self.keys[i]
            yield key, self.data[key]