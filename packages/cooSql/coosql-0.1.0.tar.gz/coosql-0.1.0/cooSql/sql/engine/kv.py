import pickle
from typing import List, Optional, Tuple, Dict, Any, Callable
from enum import Enum
import json

from .base import Engine, Transaction
from ..schema import TableSchema
from ..types.data_types import Row, Value
from storage.engine import Engine as StorageEngine
from storage.mvcc import Transaction as MvccTransaction
from error import InternalError


class Key:
    """键定义，用于在存储引擎中标识不同类型的数据"""
    
    class Type(Enum):
        """键类型"""
        TABLE = 0   # 表元数据
        ROW = 1     # 表数据行
    
    @staticmethod
    def table(table_name: str) -> bytes:
        """
        生成表元数据键
        
        Args:
            table_name: 表名
            
        Returns:
            表元数据键字节序列
        """
        return pickle.dumps((Key.Type.TABLE, table_name))
    
    @staticmethod
    def row(table_name: str, row_id: Value) -> bytes:
        """
        生成行数据键
        
        Args:
            table_name: 表名
            row_id: 行ID（通常为主键值）
            
        Returns:
            行数据键字节序列
        """
        return pickle.dumps((Key.Type.ROW, table_name, row_id))


class KeyPrefix:
    """键前缀定义，用于扫描操作"""
    
    @staticmethod
    def table() -> bytes:
        """
        生成表元数据键前缀
        
        Returns:
            表元数据键前缀字节序列
        """
        return pickle.dumps((Key.Type.TABLE,))
    
    @staticmethod
    def row(table_name: str) -> bytes:
        """
        生成行数据键前缀
        
        Args:
            table_name: 表名
            
        Returns:
            行数据键前缀字节序列
        """
        return pickle.dumps((Key.Type.ROW, table_name))


class KVTransaction(Transaction):
    """KV事务实现"""
    
    def __init__(self, txn: MvccTransaction):
        """
        初始化
        
        Args:
            txn: MVCC事务
        """
        self.txn = txn
    
    def commit(self) -> None:
        """提交事务"""
        self.txn.commit()
    
    def rollback(self) -> None:
        """回滚事务"""
        self.txn.rollback()
    
    def create_table(self, table: TableSchema) -> None:
        """
        创建表
        
        Args:
            table: 表模式
            
        Raises:
            InternalError: 如果表已存在或表定义无效
        """
        # 检查表是否已存在
        if self.get_table(table.name) is not None:
            raise InternalError(f"表 {table.name} 已经存在")
        
        # 检查表定义有效性
        if not table.columns:
            raise InternalError(f"表 {table.name} 没有定义列")
        
        # 序列化并存储表定义
        key = Key.table(table.name)
        value = pickle.dumps(table)
        self.txn.set(key, value)
    
    def get_table(self, table_name: str) -> Optional[TableSchema]:
        """
        获取表模式
        
        Args:
            table_name: 表名
            
        Returns:
            表模式，如果表不存在则返回None
        """
        key = Key.table(table_name)
        value = self.txn.get(key)
        if value is None:
            return None
        return pickle.loads(value)
    
    def must_get_table(self, table_name: str) -> TableSchema:
        """
        获取表模式，如果不存在则抛出异常
        
        Args:
            table_name: 表名
            
        Returns:
            表模式
            
        Raises:
            InternalError: 如果表不存在
        """
        table = self.get_table(table_name)
        if table is None:
            raise InternalError(f"表 {table_name} 不存在")
        return table
    
    def create_row(self, table_name: str, row: Row) -> None:
        """
        创建行
        
        Args:
            table_name: 表名
            row: 行数据
            
        Raises:
            InternalError: 如果行数据和表模式不匹配
        """
        # 获取表模式
        table = self.must_get_table(table_name)
        
        # 验证行数据有效性
        if len(row) != len(table.columns):
            raise InternalError(f"行数据列数 ({len(row)}) 与表 {table_name} 的列数 ({len(table.columns)}) 不匹配")
        
        # 校验数据类型
        for i, col in enumerate(table.columns):
            data_type = row[i].datatype()
            if data_type is None:
                # 处理NULL值
                if not col.nullable:
                    raise InternalError(f"列 {col.name} 不允许为空")
            elif data_type != col.datatype:
                raise InternalError(f"列 {col.name} 类型不匹配，期望 {col.datatype}，实际 {data_type}")
        
        # 使用第一列的值作为行ID（暂时的简化方案，实际系统中应该使用真正的主键）
        row_id = row[0]
        key = Key.row(table_name, row_id)
        value = pickle.dumps(row)
        self.txn.set(key, value)
    
    def scan_table(self, table_name: str) -> List[Row]:
        """
        扫描表中所有行
        
        Args:
            table_name: 表名
            
        Returns:
            所有行数据
        """
        # 获取表模式（验证表存在）
        self.must_get_table(table_name)
        
        # 获取所有键
        all_keys = []
        for key, _ in self.txn.scan():
            all_keys.append(key)
        
        # 手动过滤符合前缀的键
        filtered_keys = []
        for key in all_keys:
            try:
                unpickled_key = pickle.loads(key)
                if isinstance(unpickled_key, tuple) and len(unpickled_key) >= 2:
                    if unpickled_key[0] == Key.Type.ROW and unpickled_key[1] == table_name:
                        filtered_keys.append(key)
            except:
                pass  # 跳过无法解码的键
        
        # 获取值并反序列化
        rows = []
        for key in filtered_keys:
            value = self.txn.get(key)
            if value:
                try:
                    row = pickle.loads(value)
                    rows.append(row)
                except:
                    pass  # 跳过无法解码的值
        
        return rows
    
    def update_rows(self, table_name: str, updates: dict, condition: Optional[Callable[[Row], bool]] = None) -> int:
        """
        更新表中的行
        
        Args:
            table_name: 表名
            updates: 要更新的列和值的字典 {列索引: 新值}
            condition: 用于筛选行的条件函数
            
        Returns:
            更新的行数
            
        Raises:
            InternalError: 如果表不存在或更新操作无效
        """
        # 获取表模式（验证表存在）
        table = self.must_get_table(table_name)
        
        # 验证更新操作的有效性
        for col_idx in updates:
            if col_idx < 0 or col_idx >= len(table.columns):
                raise InternalError(f"列索引 {col_idx} 超出范围")
            
            # 校验数据类型
            new_value = updates[col_idx]
            col = table.columns[col_idx]
            data_type = new_value.datatype()
            
            if data_type is None:
                # 处理NULL值
                if not col.nullable:
                    raise InternalError(f"列 {col.name} 不允许为空")
            elif data_type != col.datatype:
                raise InternalError(f"列 {col.name} 类型不匹配，期望 {col.datatype}，实际 {data_type}")
        
        # 获取所有行
        rows = self.scan_table(table_name)
        updated_count = 0
        
        # 对每一行应用更新
        for row in rows:
            # 检查条件
            if condition is None or condition(row):
                # 创建更新后的行
                updated_row = list(row)
                for col_idx, new_value in updates.items():
                    updated_row[col_idx] = new_value
                
                # 使用第一列作为行ID
                row_id = row[0]
                key = Key.row(table_name, row_id)
                value = pickle.dumps(updated_row)
                self.txn.set(key, value)
                updated_count += 1
        
        return updated_count
    
    def delete_rows(self, table_name: str, condition: Optional[Callable[[Row], bool]] = None) -> int:
        """
        删除表中的行
        
        Args:
            table_name: 表名
            condition: 用于筛选行的条件函数
            
        Returns:
            删除的行数
            
        Raises:
            InternalError: 如果表不存在
        """
        # 获取表模式（验证表存在）
        self.must_get_table(table_name)
        
        # 获取所有行
        rows = self.scan_table(table_name)
        deleted_count = 0
        
        # 对每一行应用删除
        for row in rows:
            # 检查条件
            if condition is None or condition(row):
                # 使用第一列作为行ID
                row_id = row[0]
                key = Key.row(table_name, row_id)
                self.txn.delete(key)
                deleted_count += 1
        
        return deleted_count


class KVEngine(Engine):
    """KV引擎实现"""
    
    def __init__(self, storage_engine: StorageEngine):
        """
        初始化
        
        Args:
            storage_engine: 存储引擎
        """
        self.storage_engine = storage_engine
    
    def begin(self) -> Transaction:
        """
        开始一个事务
        
        Returns:
            KV事务
        """
        mvcc_txn = self.storage_engine.begin(False)
        mvcc_txn.begin()  # 确保MVCC事务已经开始
        return KVTransaction(mvcc_txn)