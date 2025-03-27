from setuptools import setup, find_packages
import os

# 多种路径尝试读取README.txt
readme_paths = [
    "README.md",     # 从当前目录
    os.path.join(os.path.dirname(__file__), "README.md")  # 使用__file__
]

long_description = ""
for path in readme_paths:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            long_description = fh.read()
            break
    except:
        continue

# 如果无法读取任何README文件，提供默认描述
if not long_description:
    long_description = "cooSql - Python implementation of a lightweight SQL database system for educational purposes."

setup(
    name="cooSql",
    version="0.1.0",
    python_requires=">=3.7",
    install_requires=[
        "typing;python_version<'3.5'",  # 为低版本Python提供typing
    ],
    author="cooSql Contributors",
    author_email="your.email@example.com",  # 更新为实际的邮箱地址
    description="Python implementation of a lightweight SQL database system for educational purposes",
    long_description=long_description,
    long_description_content_type="text/markdown",  # 修改为markdown格式
    license="MIT",
    license_files=("LICENSE",),  # 修复许可证文件路径
    url="https://github.com/yourusername/cooSql",  # 更新为实际的GitHub存储库URL
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests", "**.__pycache__", "*.__pycache__"]),
    include_package_data=True,  # 添加include_package_data以包含MANIFEST.in中的文件
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Database",
        "Topic :: Education",
        "Topic :: Software Development :: Libraries",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
    ],
    keywords="database, sql, education, learning, kv-store, lightweight-database",  # 增加更相关的关键词
    project_urls={  # 添加更多项目相关链接
        "Bug Tracker": "https://github.com/yourusername/cooSql/issues",
        "Documentation": "https://github.com/yourusername/cooSql/blob/main/README.md",
        "Source Code": "https://github.com/yourusername/cooSql",
    },
)