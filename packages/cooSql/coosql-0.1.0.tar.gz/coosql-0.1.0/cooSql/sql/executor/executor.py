from typing import List, Dict, Optional, Callable, Any
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from sql.engine.base import Transaction
from sql.parser.ast import Statement, Condition, Expression, Consts
from sql.types.data_types import Row, Value
from sql.schema import TableSchema, ColumnSchema
from error import InternalError


class Executor:
    """SQL语句执行器"""
    
    @staticmethod
    def execute(stmt: Statement, txn: Transaction) -> Optional[List[Row]]:
        """
        执行SQL语句
        
        Args:
            stmt: SQL语句
            txn: 事务
            
        Returns:
            如果是查询语句，返回查询结果；否则返回None
            
        Raises:
            InternalError: 执行失败
        """
        if stmt.stmt_type == 'create_table':
            return Executor._execute_create_table(stmt, txn)
        elif stmt.stmt_type == 'insert':
            return Executor._execute_insert(stmt, txn)
        elif stmt.stmt_type == 'select':
            return Executor._execute_select(stmt, txn)
        elif stmt.stmt_type == 'update':
            return Executor._execute_update(stmt, txn)
        elif stmt.stmt_type == 'delete':
            return Executor._execute_delete(stmt, txn)
        else:
            raise InternalError(f"不支持的SQL语句类型: {stmt.stmt_type}")
    
    @staticmethod
    def _execute_create_table(stmt: Statement, txn: Transaction) -> None:
        """执行CREATE TABLE语句"""
        # 创建表模式
        table = TableSchema(name=stmt.name, columns=stmt.columns)
        txn.create_table(table)
        return None
    
    @staticmethod
    def _execute_insert(stmt: Statement, txn: Transaction) -> None:
        """执行INSERT语句"""
        # 获取表模式
        table = txn.must_get_table(stmt.table_name)
        
        # 处理每一行数据
        for expr_list in stmt.values:
            # 转换表达式为值
            row = []
            
            # 如果没有指定列名，则按顺序插入所有列
            if stmt.columns is None:
                # 检查值的数量与列数是否匹配
                if len(expr_list) > len(table.columns):
                    raise InternalError(f"插入的值太多，列数为 {len(table.columns)}")
                
                # 转换值
                for i, expr in enumerate(expr_list):
                    if expr.expr_type == 'consts':
                        const = expr.value
                        if const.const_type == 'null':
                            row.append(Value.null())
                        elif const.const_type == 'boolean':
                            row.append(Value.boolean(const.value))
                        elif const.const_type == 'integer':
                            row.append(Value.integer(const.value))
                        elif const.const_type == 'float':
                            row.append(Value.float(const.value))
                        elif const.const_type == 'string':
                            row.append(Value.string(const.value))
                        else:
                            raise InternalError(f"不支持的常量类型: {const.const_type}")
                    else:
                        raise InternalError(f"不支持的表达式类型: {expr.expr_type}")
                
                # 如果没有提供所有列的值，则使用默认值或NULL填充
                for i in range(len(expr_list), len(table.columns)):
                    col = table.columns[i]
                    if col.default is not None:
                        # 使用默认值
                        row.append(Executor._create_value_from_expression(col.default))
                    else:
                        if not col.nullable:
                            raise InternalError(f"列 {col.name} 不允许为空")
                        row.append(Value.null())
            else:
                # 指定了列名，初始化所有列为默认值或NULL
                column_values = {}
                
                # 验证列名有效性
                for col_name in stmt.columns:
                    found = False
                    for idx, col in enumerate(table.columns):
                        if col.name == col_name:
                            found = True
                            break
                    if not found:
                        raise InternalError(f"列 {col_name} 不存在")
                
                # 转换指定的列值
                for i, col_name in enumerate(stmt.columns):
                    expr = expr_list[i]
                    column_values[col_name] = Executor._create_value_from_expression(expr)
                
                # 构建完整的行，按表结构顺序
                for col in table.columns:
                    if col.name in column_values:
                        row.append(column_values[col.name])
                    elif col.default is not None:
                        # 使用默认值
                        row.append(Executor._create_value_from_expression(col.default))
                    else:
                        if not col.nullable:
                            raise InternalError(f"列 {col.name} 不允许为空")
                        row.append(Value.null())
            
            # 插入数据行
            txn.create_row(stmt.table_name, row)
        
        return None
    
    @staticmethod
    def _execute_select(stmt: Statement, txn: Transaction) -> List[Row]:
        """执行SELECT语句"""
        # 获取表模式
        table = txn.must_get_table(stmt.table_name)
        
        # 获取所有行
        rows = txn.scan_table(stmt.table_name)
        
        # 如果有WHERE条件，进行过滤
        if hasattr(stmt, 'where') and stmt.where is not None:
            condition_fn = Executor._build_condition_function(stmt.where, table)
            rows = [row for row in rows if condition_fn(row)]
        
        return rows
    
    @staticmethod
    def _execute_update(stmt: Statement, txn: Transaction) -> None:
        """执行UPDATE语句"""
        # 获取表模式
        table = txn.must_get_table(stmt.table_name)
        
        # 构建更新映射 {列索引: 新值}
        updates = {}
        for col_name, expr in stmt.updates.items():
            # 找到列索引
            col_idx = -1
            for idx, col in enumerate(table.columns):
                if col.name == col_name:
                    col_idx = idx
                    break
            
            if col_idx == -1:
                raise InternalError(f"列 {col_name} 不存在")
            
            # 获取新值
            new_value = Executor._create_value_from_expression(expr)
            updates[col_idx] = new_value
        
        # 构建条件函数
        condition_fn = None
        if hasattr(stmt, 'where') and stmt.where is not None:
            condition_fn = Executor._build_condition_function(stmt.where, table)
        
        # 执行更新
        updated_count = txn.update_rows(stmt.table_name, updates, condition_fn)
        
        return None
    
    @staticmethod
    def _execute_delete(stmt: Statement, txn: Transaction) -> None:
        """执行DELETE语句"""
        # 获取表模式
        table = txn.must_get_table(stmt.table_name)
        
        # 构建条件函数
        condition_fn = None
        if hasattr(stmt, 'where') and stmt.where is not None:
            condition_fn = Executor._build_condition_function(stmt.where, table)
        
        # 执行删除
        deleted_count = txn.delete_rows(stmt.table_name, condition_fn)
        
        return None
    
    @staticmethod
    def _create_value_from_expression(expr):
        """从表达式创建值"""
        # 导入必要的类
        from sql.types.data_types import Value
        
        # 如果已经是Value对象，直接返回
        if isinstance(expr, Value):
            return expr
            
        if hasattr(expr, 'expr_type') and expr.expr_type == 'consts':
            const = expr.value
            if const.const_type == 'null':
                return Value.null()
            elif const.const_type == 'boolean':
                return Value.boolean(const.value)
            elif const.const_type == 'integer':
                return Value.integer(const.value)
            elif const.const_type == 'float':
                return Value.float(const.value)
            elif const.const_type == 'string':
                return Value.string(const.value)
            else:
                raise InternalError(f"不支持的常量类型: {const.const_type}")
        else:
            raise InternalError(f"不支持的表达式类型: {type(expr)}")
    
    @staticmethod
    def _build_condition_function(condition: Condition, table: TableSchema) -> Callable[[Row], bool]:
        """构建条件函数"""
        # 获取列名到索引的映射
        col_name_to_idx = {}
        for idx, col in enumerate(table.columns):
            col_name_to_idx[col.name] = idx
        
        def condition_fn(row: Row) -> bool:
            return Executor._evaluate_condition(condition, row, col_name_to_idx)
        
        return condition_fn
    
    @staticmethod
    def _evaluate_condition(condition: Condition, row: Row, col_name_to_idx: Dict[str, int]) -> bool:
        """评估条件"""
        if condition.cond_type == 'equals':
            col_idx = col_name_to_idx.get(condition.column)
            if col_idx is None:
                raise InternalError(f"列 {condition.column} 不存在")
            col_value = row[col_idx]
            right_value = Executor._create_value_from_expression(condition.value)
            return col_value == right_value
        
        elif condition.cond_type == 'not_equals':
            col_idx = col_name_to_idx.get(condition.column)
            if col_idx is None:
                raise InternalError(f"列 {condition.column} 不存在")
            col_value = row[col_idx]
            right_value = Executor._create_value_from_expression(condition.value)
            return col_value != right_value
        
        elif condition.cond_type == 'gt':
            col_idx = col_name_to_idx.get(condition.column)
            if col_idx is None:
                raise InternalError(f"列 {condition.column} 不存在")
            col_value = row[col_idx].value
            right_value = Executor._create_value_from_expression(condition.value).value
            if col_value is None or right_value is None:
                return False
            return col_value > right_value
        
        elif condition.cond_type == 'gte':
            col_idx = col_name_to_idx.get(condition.column)
            if col_idx is None:
                raise InternalError(f"列 {condition.column} 不存在")
            col_value = row[col_idx].value
            right_value = Executor._create_value_from_expression(condition.value).value
            if col_value is None or right_value is None:
                return False
            return col_value >= right_value
        
        elif condition.cond_type == 'lt':
            col_idx = col_name_to_idx.get(condition.column)
            if col_idx is None:
                raise InternalError(f"列 {condition.column} 不存在")
            col_value = row[col_idx].value
            right_value = Executor._create_value_from_expression(condition.value).value
            if col_value is None or right_value is None:
                return False
            return col_value < right_value
        
        elif condition.cond_type == 'lte':
            col_idx = col_name_to_idx.get(condition.column)
            if col_idx is None:
                raise InternalError(f"列 {condition.column} 不存在")
            col_value = row[col_idx].value
            right_value = Executor._create_value_from_expression(condition.value).value
            if col_value is None or right_value is None:
                return False
            return col_value <= right_value
        
        elif condition.cond_type == 'and':
            left_result = Executor._evaluate_condition(condition.left, row, col_name_to_idx)
            if not left_result:
                return False
            return Executor._evaluate_condition(condition.right, row, col_name_to_idx)
        
        elif condition.cond_type == 'or':
            left_result = Executor._evaluate_condition(condition.left, row, col_name_to_idx)
            if left_result:
                return True
            return Executor._evaluate_condition(condition.right, row, col_name_to_idx)
        
        raise InternalError(f"不支持的条件类型: {condition.cond_type}")