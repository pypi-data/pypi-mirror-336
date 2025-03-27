from typing import List, Optional, Dict

from sql.parser.ast import Statement, Column, Expression
from sql.schema import TableSchema, ColumnSchema
from sql.types.data_types import Value, DataType
from .plan import (
    Plan, Node, CreateTableNode, InsertNode, ScanNode, UpdateNode, DeleteNode
)


class Planner:
    """SQL计划构建器"""
    
    def __init__(self):
        pass
    
    def build(self, stmt: Statement) -> Plan:
        """从语句构建计划"""
        node = self._build_statement(stmt)
        return Plan(node)
    
    def _build_statement(self, stmt: Statement) -> Node:
        """构建具体的节点"""
        if stmt.stmt_type == 'create_table':
            # 创建表节点
            table_schema = TableSchema(
                name=stmt.name,
                columns=[self._build_column(col) for col in stmt.columns]
            )
            return CreateTableNode(schema=table_schema)
        
        elif stmt.stmt_type == 'insert':
            # 插入节点
            columns = stmt.columns if hasattr(stmt, 'columns') else None
            return InsertNode(
                table_name=stmt.table_name,
                columns=columns if columns else [],
                values=stmt.values
            )
        
        elif stmt.stmt_type == 'select':
            # 扫描节点
            where = stmt.where if hasattr(stmt, 'where') else None
            return ScanNode(
                table_name=stmt.table_name,
                where=where
            )
        
        elif stmt.stmt_type == 'update':
            # 更新节点
            where = stmt.where if hasattr(stmt, 'where') else None
            return UpdateNode(
                table_name=stmt.table_name,
                updates=stmt.updates,
                where=where
            )
        
        elif stmt.stmt_type == 'delete':
            # 删除节点
            where = stmt.where if hasattr(stmt, 'where') else None
            return DeleteNode(
                table_name=stmt.table_name,
                where=where
            )
        
        else:
            raise ValueError(f"不支持的语句类型: {stmt.stmt_type}")
    
    def _build_column(self, col: Column) -> ColumnSchema:
        """从AST列定义构建列模式"""
        # 处理默认值
        default = None
        if col.default is not None:
            if col.default.expr_type == 'consts':
                const = col.default.value
                if const.const_type == 'null':
                    default = Value.null()
                elif const.const_type == 'boolean':
                    default = Value.boolean(const.value)
                elif const.const_type == 'integer':
                    default = Value.integer(const.value)
                elif const.const_type == 'float':
                    default = Value.float(const.value)
                elif const.const_type == 'string':
                    default = Value.string(const.value)
        
        # 处理可空性
        nullable = True if col.nullable is None else col.nullable
        
        return ColumnSchema(
            name=col.name,
            datatype=col.datatype,
            nullable=nullable,
            default=default
        )