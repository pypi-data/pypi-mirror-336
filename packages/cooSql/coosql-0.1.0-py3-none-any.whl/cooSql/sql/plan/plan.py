from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass

from sql.parser.ast import Statement, Expression, Condition
from sql.types.data_types import Row
from sql.schema import TableSchema
from sql.engine.base import Transaction
from error import InternalError


class Node(ABC):
    """SQL执行计划节点"""
    
    @abstractmethod
    def execute(self, txn: Transaction) -> Optional[List[Row]]:
        """执行节点"""
        pass


@dataclass
class CreateTableNode(Node):
    """创建表节点"""
    schema: TableSchema
    
    def execute(self, txn: Transaction) -> Optional[List[Row]]:
        txn.create_table(self.schema)
        return None


@dataclass
class InsertNode(Node):
    """插入数据节点"""
    table_name: str
    columns: List[str]
    values: List[List[Expression]]
    
    def execute(self, txn: Transaction) -> Optional[List[Row]]:
        from sql.executor.executor import Executor
        
        # 创建一个临时的Statement对象，重用插入逻辑
        stmt = Statement('insert', table_name=self.table_name, 
                        columns=self.columns if self.columns else None, 
                        values=self.values)
        
        # 执行插入
        return Executor._execute_insert(stmt, txn)


@dataclass
class ScanNode(Node):
    """扫描表节点"""
    table_name: str
    where: Optional[Condition] = None
    
    def execute(self, txn: Transaction) -> Optional[List[Row]]:
        from sql.executor.executor import Executor
        
        # 创建一个临时的Statement对象，重用查询逻辑
        stmt = Statement('select', table_name=self.table_name, where=self.where)
        
        # 执行查询
        return Executor._execute_select(stmt, txn)


@dataclass
class UpdateNode(Node):
    """更新数据节点"""
    table_name: str
    updates: Dict[str, Expression]
    where: Optional[Condition] = None
    
    def execute(self, txn: Transaction) -> Optional[List[Row]]:
        from sql.executor.executor import Executor
        
        # 创建一个临时的Statement对象，重用更新逻辑
        stmt = Statement('update', table_name=self.table_name, 
                        updates=self.updates, where=self.where)
        
        # 执行更新
        return Executor._execute_update(stmt, txn)


@dataclass
class DeleteNode(Node):
    """删除数据节点"""
    table_name: str
    where: Optional[Condition] = None
    
    def execute(self, txn: Transaction) -> Optional[List[Row]]:
        from sql.executor.executor import Executor
        
        # 创建一个临时的Statement对象，重用删除逻辑
        stmt = Statement('delete', table_name=self.table_name, where=self.where)
        
        # 执行删除
        return Executor._execute_delete(stmt, txn)


class Plan:
    """SQL执行计划"""
    
    def __init__(self, node: Node):
        self.node = node
    
    @classmethod
    def build(cls, stmt: Statement) -> 'Plan':
        """从语句构建计划"""
        from .planner import Planner
        
        # 使用Planner构建执行计划
        return Planner().build(stmt)
    
    def execute(self, txn: Transaction) -> Optional[List[Row]]:
        """执行计划"""
        return self.node.execute(txn)