# CooSQL 示例程序

本目录包含了CooSQL数据库的使用示例，展示了其主要功能和API的使用方法。

## 目录结构

```
examples/
├── README.md                 - 本文件
├── run_all_examples.py       - 运行所有示例的脚本
└── basic_usage/              - 基本使用示例
    ├── memory_example.py     - 内存存储引擎示例
    ├── disk_example.py       - 磁盘存储引擎示例
    └── transaction_example.py - 事务处理示例
```

## 快速开始

你可以使用以下命令运行所有示例：

```bash
python -m examples.run_all_examples
```

或者单独运行特定示例：

```bash
# 运行内存存储引擎示例
python -m examples.basic_usage.memory_example

# 运行磁盘存储引擎示例
python -m examples.basic_usage.disk_example

# 运行事务处理示例
python -m examples.basic_usage.transaction_example
```

## 示例说明

### 基本使用示例 (basic_usage)

1. **内存存储引擎示例** (memory_example.py)
   - 展示如何使用内存存储引擎创建表、插入数据和查询数据
   - 内存存储引擎适用于临时数据处理和测试场景

2. **磁盘存储引擎示例** (disk_example.py)
   - 展示如何使用磁盘存储引擎进行持久化存储
   - 验证数据持久性，重新连接数据库后仍能读取数据

3. **事务处理示例** (transaction_example.py)
   - 展示如何使用事务进行数据操作
   - 包含成功提交和失败回滚两个场景，模拟银行转账操作

## 自定义示例

你可以基于这些示例创建自己的测试程序。最简单的方法是复制一个现有示例，然后根据需要修改SQL语句和业务逻辑。

## 注意事项

- 示例默认使用相对导入，确保你从项目根目录运行它们
- 磁盘存储示例会创建临时数据库文件，程序结束时会自动清理
- 确保运行程序的用户对示例目录有写入权限(用于磁盘存储示例) 