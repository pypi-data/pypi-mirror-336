from typing import List, Optional, Any, Dict
import sys
import os

from error import InternalError
from sql.parser import Parser
from sql.parser.ast import Statement
from sql.engine import Transaction
from sql.types.data_types import Value, Row
from sql.plan import Plan


class Session:
    """SQL会话，管理SQL解析和执行"""
    
    def __init__(self, transaction: Transaction):
        """
        初始化
        
        Args:
            transaction: 事务实例
        """
        self.transaction = transaction
    
    def execute(self, sql: str) -> Optional[List[Row]]:
        """
        执行SQL语句
        
        Args:
            sql: SQL语句
            
        Returns:
            查询结果，如果不是查询语句则返回None
            
        Raises:
            InternalError: 如果SQL执行失败
        """
        # 解析SQL
        parser = Parser(sql)
        stmt = parser.parse()
        
        try:
            # 构建计划
            plan = Plan.build(stmt)
            
            # 执行计划
            result = plan.execute(self.transaction)
            
            # 只有SELECT语句才返回结果
            if stmt.stmt_type == 'select':
                return result
            return None
        except Exception as e:
            # 捕获所有异常，转换为InternalError
            raise InternalError(f"执行SQL失败: {e}") from e