from enum import Enum
from typing import List, Optional, Union


class DataType(Enum):
    """数据类型定义"""
    BOOLEAN = 'BOOLEAN'
    INTEGER = 'INTEGER'
    FLOAT = 'FLOAT'
    STRING = 'STRING'


class Value:
    """数据值定义"""
    def __init__(self, value: Optional[Union[bool, int, float, str]] = None):
        self.value = value
    
    @classmethod
    def null(cls):
        """创建空值"""
        return cls(None)
    
    @classmethod
    def boolean(cls, value: bool):
        """创建布尔值"""
        return cls(value)
    
    @classmethod
    def integer(cls, value: int):
        """创建整数值"""
        return cls(value)
    
    @classmethod
    def float(cls, value: float):
        """创建浮点值"""
        return cls(value)
    
    @classmethod
    def string(cls, value: str):
        """创建字符串值"""
        return cls(value)
    
    def from_expression(cls, expr):
        """从表达式创建值"""
        from sql.parser.ast import Expression, Consts
        
        if isinstance(expr, Expression):
            if expr.expr_type == 'consts':
                consts = expr.value
                if consts.const_type == 'null':
                    return cls.null()
                elif consts.const_type == 'boolean':
                    return cls.boolean(consts.value)
                elif consts.const_type == 'integer':
                    return cls.integer(consts.value)
                elif consts.const_type == 'float':
                    return cls.float(consts.value)
                elif consts.const_type == 'string':
                    return cls.string(consts.value)
        raise ValueError(f"无法从表达式创建值: {expr}")
    
    def datatype(self) -> Optional[DataType]:
        """获取数据类型"""
        if self.value is None:
            return None
        elif isinstance(self.value, bool):
            return DataType.BOOLEAN
        elif isinstance(self.value, int):
            return DataType.INTEGER
        elif isinstance(self.value, float):
            return DataType.FLOAT
        elif isinstance(self.value, str):
            return DataType.STRING
        return None
    
    def __eq__(self, other):
        if not isinstance(other, Value):
            return False
        return self.value == other.value
    
    def __repr__(self):
        return f"Value({self.value!r})"


# 定义行类型
Row = List[Value]