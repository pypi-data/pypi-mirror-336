from abc import ABC, abstractmethod
from typing import List, Optional, Callable, Any

from ..schema import TableSchema
from ..types.data_types import Row, Value


class Transaction(ABC):
    """SQL事务接口定义"""
    
    @abstractmethod
    def commit(self) -> None:
        """提交事务"""
        pass
    
    @abstractmethod
    def rollback(self) -> None:
        """回滚事务"""
        pass
    
    @abstractmethod
    def create_table(self, table: TableSchema) -> None:
        """创建表"""
        pass
    
    @abstractmethod
    def get_table(self, table_name: str) -> Optional[TableSchema]:
        """获取表模式"""
        pass
    
    @abstractmethod
    def must_get_table(self, table_name: str) -> TableSchema:
        """获取表模式，如果不存在则抛出异常"""
        pass
    
    @abstractmethod
    def create_row(self, table_name: str, row: Row) -> None:
        """创建行"""
        pass
    
    @abstractmethod
    def scan_table(self, table_name: str) -> List[Row]:
        """扫描表中所有行"""
        pass
    
    @abstractmethod
    def update_rows(self, table_name: str, updates: dict, condition: Optional[Callable[[Row], bool]] = None) -> int:
        """
        更新表中的行
        
        Args:
            table_name: 表名
            updates: 要更新的列和值的字典 {列索引: 新值}
            condition: 用于筛选行的条件函数
            
        Returns:
            更新的行数
        """
        pass
    
    @abstractmethod
    def delete_rows(self, table_name: str, condition: Optional[Callable[[Row], bool]] = None) -> int:
        """
        删除表中的行
        
        Args:
            table_name: 表名
            condition: 用于筛选行的条件函数
            
        Returns:
            删除的行数
        """
        pass


class Engine(ABC):
    """SQL引擎接口定义"""
    
    @abstractmethod
    def begin(self) -> Transaction:
        """开始一个事务"""
        pass