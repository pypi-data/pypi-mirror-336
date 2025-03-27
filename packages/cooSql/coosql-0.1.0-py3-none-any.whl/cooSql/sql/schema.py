from dataclasses import dataclass
from typing import List, Optional
from .types import DataType, Value


@dataclass
class ColumnSchema:
    """列模式定义"""
    name: str
    datatype: DataType
    nullable: bool
    default: Optional[Value] = None


@dataclass
class TableSchema:
    """表模式定义"""
    name: str
    columns: List[ColumnSchema]