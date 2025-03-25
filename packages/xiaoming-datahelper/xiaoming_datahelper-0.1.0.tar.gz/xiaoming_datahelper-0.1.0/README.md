# DataHelper

一个简单的数据处理工具包，帮助你轻松处理 CSV 文件数据。

## 安装

```bash
pip install datahelper
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

## 第四步：编写测试

```python
# tests/test_reader.py
import pytest
from datahelper import CSVReader

def test_csv_reader():
    reader = CSVReader("test_data.csv")
    data = reader.read()
    assert not data.empty
```

## 第五步：本地开发和测试

小明在本地进行开发时的操作：

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows 使用: venv\Scripts\activate

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest tests/

# 格式化代码
black src/ tests/
```

## 第六步：编写示例代码

```python
# examples/basic_usage.py
from datahelper import CSVReader, DataProcessor

def main():
    # 读取示例数据
    reader = CSVReader("sample_data.csv")
    data = reader.read()

    # 处理数据
    processor = DataProcessor(data)
    age_stats = processor.calculate_stats("age")
    salary_stats = processor.calculate_stats("salary")

    print("年龄统计:", age_stats)
    print("薪资统计:", salary_stats)

if __name__ == "__main__":
    main()
```

## 第七步：准备发布

### 1. 构建包

```bash
# 安装构建工具
pip install build

# 构建包
python -m build
```

### 2. 上传到 PyPI

```bash
# 安装上传工具
pip install twine

# 上传到 PyPI
python -m twine upload dist/*
```

## 第八步：持续维护

小明建立了一个维护清单：

1. **版本控制**：

   - 使用 Git 管理代码
   - 为每个版本打标签
   - 维护更新日志

2. **文档维护**：

   - 更新 README.md
   - 添加详细的使用文档
   - 添加代码注释

3. **质量控制**：
   - 运行自动化测试
   - 代码风格检查
   - 处理用户反馈和 bug 报告

## 使用示例

其他开发者可以这样使用小明的包：

```python
from datahelper import CSVReader, DataProcessor

# 读取 CSV 文件
reader = CSVReader("sales_data.csv")
data = reader.read()

# 分析数据
processor = DataProcessor(data)

# 计算销售额统计
sales_stats = processor.calculate_stats("sales_amount")
print("销售统计:", sales_stats)
```

## 小明的开发心得

1. **项目组织**：

   - 使用清晰的目录结构
   - 将相关功能组织在一起
   - 保持代码模块化

2. **开发流程**：

   - 先写测试，后写实现
   - 经常运行测试
   - 保持代码整洁

3. **文档编写**：

   - 编写清晰的文档
   - 提供使用示例
   - 记录重要决策

4. **版本管理**：
   - 语义化版本号
   - 记录更新日志
   - 定期发布更新

通过这个例子，我们可以看到开发一个 Python 包需要考虑的各个方面，从初始设计到最终发布。小明的经历展示了一个完整的包开发生命周期。
