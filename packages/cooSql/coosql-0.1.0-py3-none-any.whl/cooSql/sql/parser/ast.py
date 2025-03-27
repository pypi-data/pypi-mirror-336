from dataclasses import dataclass
from typing import List, Optional, Union, Dict, Tuple
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from sql.types.data_types import DataType


class Consts:
    """常量表达式"""
    def __init__(self, const_type: str, value=None):
        self.const_type = const_type
        self.value = value
    
    @classmethod
    def null(cls):
        """创建空值常量"""
        return cls('null')
    
    @classmethod
    def boolean(cls, value: bool):
        """创建布尔值常量"""
        return cls('boolean', value)
    
    @classmethod
    def integer(cls, value: int):
        """创建整数常量"""
        return cls('integer', value)
    
    @classmethod
    def float(cls, value: float):
        """创建浮点数常量"""
        return cls('float', value)
    
    @classmethod
    def string(cls, value: str):
        """创建字符串常量"""
        return cls('string', value)
    
    def __eq__(self, other):
        if not isinstance(other, Consts):
            return False
        return self.const_type == other.const_type and self.value == other.value
    
    def __repr__(self):
        if self.const_type == 'null':
            return "Consts.null()"
        return f"Consts.{self.const_type}({self.value!r})"


class Expression:
    """表达式定义，目前只支持常量表达式"""
    def __init__(self, expr_type: str, value):
        self.expr_type = expr_type
        self.value = value
    
    @classmethod
    def consts(cls, const: Consts):
        """从常量创建表达式"""
        return cls('consts', const)
    
    def __eq__(self, other):
        if not isinstance(other, Expression):
            return False
        return self.expr_type == other.expr_type and self.value == other.value
    
    def __repr__(self):
        return f"Expression.{self.expr_type}({self.value!r})"


@dataclass
class Column:
    """列定义"""
    name: str
    datatype: DataType
    nullable: Optional[bool] = None
    default: Optional[Expression] = None
    
    def __eq__(self, other):
        if not isinstance(other, Column):
            return False
        return (self.name == other.name and 
                self.datatype == other.datatype and 
                self.nullable == other.nullable and 
                self.default == other.default)


class Condition:
    """条件表达式，用于WHERE子句"""
    def __init__(self, cond_type: str, **kwargs):
        self.cond_type = cond_type
        self.__dict__.update(kwargs)
    
    @classmethod
    def equals(cls, column: str, value: Expression):
        """等于条件"""
        return cls('equals', column=column, value=value)
    
    @classmethod
    def not_equals(cls, column: str, value: Expression):
        """不等于条件"""
        return cls('not_equals', column=column, value=value)
    
    @classmethod
    def gt(cls, column: str, value: Expression):
        """大于条件"""
        return cls('gt', column=column, value=value)
    
    @classmethod
    def gte(cls, column: str, value: Expression):
        """大于等于条件"""
        return cls('gte', column=column, value=value)
    
    @classmethod
    def lt(cls, column: str, value: Expression):
        """小于条件"""
        return cls('lt', column=column, value=value)
    
    @classmethod
    def lte(cls, column: str, value: Expression):
        """小于等于条件"""
        return cls('lte', column=column, value=value)
    
    @classmethod
    def and_op(cls, left, right):
        """AND操作"""
        return cls('and', left=left, right=right)
    
    @classmethod
    def or_op(cls, left, right):
        """OR操作"""
        return cls('or', left=left, right=right)
    
    def __eq__(self, other):
        if not isinstance(other, Condition):
            return False
        if self.cond_type != other.cond_type:
            return False
        
        if self.cond_type in ['equals', 'not_equals', 'gt', 'gte', 'lt', 'lte']:
            return self.column == other.column and self.value == other.value
        elif self.cond_type in ['and', 'or']:
            return self.left == other.left and self.right == other.right
        
        return False
    
    def __repr__(self):
        if self.cond_type in ['equals', 'not_equals', 'gt', 'gte', 'lt', 'lte']:
            return f"Condition.{self.cond_type}({self.column!r}, {self.value!r})"
        elif self.cond_type in ['and', 'or']:
            return f"Condition.{self.cond_type}_op({self.left!r}, {self.right!r})"
        return f"Condition({self.cond_type!r}, ...)"


class Statement:
    """SQL语句定义"""
    def __init__(self, stmt_type: str, **kwargs):
        self.stmt_type = stmt_type
        self.__dict__.update(kwargs)
    
    @classmethod
    def create_table(cls, name: str, columns: List[Column]):
        """创建表语句"""
        return cls('create_table', name=name, columns=columns)
    
    @classmethod
    def insert(cls, table_name: str, columns: Optional[List[str]], values: List[List[Expression]]):
        """插入数据语句"""
        return cls('insert', table_name=table_name, columns=columns, values=values)
    
    @classmethod
    def select(cls, table_name: str, where: Optional[Condition] = None):
        """查询语句"""
        return cls('select', table_name=table_name, where=where)
    
    @classmethod
    def update(cls, table_name: str, updates: Dict[str, Expression], where: Optional[Condition] = None):
        """更新语句"""
        return cls('update', table_name=table_name, updates=updates, where=where)
    
    @classmethod
    def delete(cls, table_name: str, where: Optional[Condition] = None):
        """删除语句"""
        return cls('delete', table_name=table_name, where=where)
    
    def __eq__(self, other):
        if not isinstance(other, Statement):
            return False
        if self.stmt_type != other.stmt_type:
            return False
            
        if self.stmt_type == 'create_table':
            return self.name == other.name and self.columns == other.columns
        elif self.stmt_type == 'insert':
            return (self.table_name == other.table_name and 
                    self.columns == other.columns and 
                    self.values == other.values)
        elif self.stmt_type == 'select':
            return self.table_name == other.table_name and self.where == other.where
        elif self.stmt_type == 'update':
            return (self.table_name == other.table_name and 
                    self.updates == other.updates and 
                    self.where == other.where)
        elif self.stmt_type == 'delete':
            return self.table_name == other.table_name and self.where == other.where
        
        return False
    
    def __repr__(self):
        if self.stmt_type == 'create_table':
            return f"Statement.create_table({self.name!r}, {self.columns!r})"
        elif self.stmt_type == 'insert':
            return f"Statement.insert({self.table_name!r}, {self.columns!r}, {self.values!r})"
        elif self.stmt_type == 'select':
            return f"Statement.select({self.table_name!r}, {getattr(self, 'where', None)!r})"
        elif self.stmt_type == 'update':
            return f"Statement.update({self.table_name!r}, {self.updates!r}, {getattr(self, 'where', None)!r})"
        elif self.stmt_type == 'delete':
            return f"Statement.delete({self.table_name!r}, {getattr(self, 'where', None)!r})"
        return f"Statement({self.stmt_type!r}, ...)"