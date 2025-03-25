# Xiaoming DataHelper

一个简单的数据处理工具包，帮助你轻松处理 CSV 文件数据。

## 功能特点

- 支持相对路径和绝对路径的 CSV 文件读取
- 提供基本的数据统计功能
- 简单易用的 API 设计
- 完整的类型提示支持

## 安装

```bash
pip install xiaoming-datahelper
```

## 快速开始

```python
from datahelper import CSVReader, DataProcessor

# 读取 CSV 文件
reader = CSVReader("data.csv")
data = reader.read()

# 处理数据
processor = DataProcessor(data)
stats = processor.calculate_stats("age")
print(stats)
```

## 使用示例

### 使用相对路径

```python
from datahelper import CSVReader

# 使用相对路径（基于当前工作目录）
reader = CSVReader("data/sales.csv")
data = reader.read()
```

### 使用绝对路径

```python
from datahelper import CSVReader

# 使用绝对路径
reader = CSVReader("/absolute/path/to/data.csv")
data = reader.read()
```

### 指定基准目录

```python
from datahelper import CSVReader

# 指定基准目录
reader = CSVReader("data/sales.csv", base_dir="/path/to/project")
data = reader.read()
```

### 数据统计

```python
from datahelper import CSVReader, DataProcessor

# 读取数据
reader = CSVReader("data.csv")
data = reader.read()

# 计算统计信息
processor = DataProcessor(data)
age_stats = processor.calculate_stats("age")
salary_stats = processor.calculate_stats("salary")

print("年龄统计:", age_stats)
print("薪资统计:", salary_stats)
```

## 开发指南

### 环境设置

1. 克隆仓库：

```bash
git clone https://github.com/yourusername/xiaoming-datahelper.git
cd xiaoming-datahelper
```

2. 创建虚拟环境：

```bash
python -m venv venv
source venv/bin/activate  # Windows 使用: venv\Scripts\activate
```

3. 安装开发依赖：

```bash
pip install -e ".[dev]"
```

### 开发工具

项目提供了多个便捷的脚本：

1. 清理项目：

```bash
./scripts/clean.sh
```

2. 构建包：

```bash
./scripts/build.sh
```

3. 上传到 PyPI：

```bash
./scripts/upload.sh
```

### 运行测试

```bash
pytest tests/
```

## 项目结构

```
datahelper/
├── src/
│   └── datahelper/
│       ├── __init__.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── reader.py
│       │   └── processor.py
│       └── utils/
│           ├── __init__.py
│           └── helpers.py
├── tests/
│   ├── __init__.py
│   ├── test_reader.py
│   └── test_processor.py
├── examples/
│   └── basic_usage.py
└── scripts/
    ├── clean.py
    ├── build.py
    └── upload.py
```

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 作者

- 小明 - [@xiaoming](https://github.com/xiaoming)

## 致谢

- 感谢所有贡献者的付出
- 特别感谢 pandas 和 numpy 团队
