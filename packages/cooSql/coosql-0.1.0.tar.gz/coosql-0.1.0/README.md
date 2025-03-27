# cooSql

Python implementation of a lightweight SQL database system for educational purposes. cooSql is designed to help understand database internals with a clean, modular architecture focusing on SQL parsing, query execution, and storage management.

## 项目结构

```
cooSql/
├── error.py                # 错误定义
├── sql/                    # SQL 模块
│   ├── parser/             # SQL 解析器
│   │   ├── ast.py          # 抽象语法树定义
│   │   ├── lexer.py        # 词法分析器
│   │   └── parser.py       # 语法分析器
│   ├── types/              # 数据类型定义
│   │   └── data_types.py   # 数据类型和值
│   └── schema.py           # 表模式定义
├── storage/                # 存储模块
│   ├── engine.py           # 存储引擎接口
│   └── memory.py           # 内存存储引擎实现
└── tests/                  # 测试
    ├── test_lexer.py       # 词法分析器测试
    └── test_parser.py      # 语法分析器测试
```

## 安装

```bash
# 从源码安装
git clone https://github.com/yourusername/cooSql.git
cd cooSql
pip install -e .
```

## 快速开始

```python
from storage.disk import DiskEngine
from sql.engine.kv import KVEngine
from sql.session import Session

# 创建数据库连接
storage_engine = DiskEngine("test.db")
kv_engine = KVEngine(storage_engine)
transaction = kv_engine.begin()
session = Session(transaction)

# 创建表
session.execute("""
CREATE TABLE users (
    id INTEGER NOT NULL,
    name STRING NOT NULL,
    age INTEGER,
    email STRING
);
""")

# 插入数据
session.execute("INSERT INTO users VALUES (1, 'Alice', 30, 'alice@example.com');")

# 查询数据
results = session.execute("SELECT * FROM users;")
for row in results:
    print([col.value for col in row])

# 提交事务
transaction.commit()

# 关闭连接
storage_engine.close()
```

## 功能特性

目前支持的 SQL 语法：

1. Create Table
```sql
CREATE TABLE table_name (
    [ column_name data_type [ column_constraint [...] ] ]
    [, ... ]
);
```

其中 data_type 可以是：
- BOOLEAN(BOOL): true | false
- FLOAT(DOUBLE)
- INTEGER(INT)
- STRING(TEXT, VARCHAR)

列约束可以是：
[ NOT NULL | NULL | DEFAULT expr ]

2. Insert Into
```sql
INSERT INTO table_name
[ ( column_name [, ...] ) ]
VALUES ( expr [, ...] );
```

3. Select * From
```sql
SELECT * FROM table_name;
```

## 测试

运行测试：
```bash
# 单元测试
python -m tests.test_lexer
python -m tests.test_parser

# 或者使用pytest运行所有测试
pytest
```

## 示例

查看 `examples/` 目录了解更多用法示例:

- `examples/basic_usage/`: 基本使用方法示例，包括简单查询、事务处理等
- 批量操作示例: 展示如何进行批量数据操作和压力测试

## 贡献

欢迎为cooSql做出贡献！请参考以下步骤：

1. Fork项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

## 许可证

该项目采用MIT许可证 - 详细信息请参阅LICENSE文件