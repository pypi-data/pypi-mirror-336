import os
import pytest
from datahelper import CSVReader


def test_csv_reader():
    # 获取测试数据文件的路径
    test_dir = os.path.dirname(os.path.abspath(__file__))

    # 测试相对路径
    reader = CSVReader("test_data/test_data.csv", base_dir=test_dir)
    data = reader.read()
    assert not data.empty
    assert len(data) == 3  # 验证数据行数
    assert "age" in data.columns  # 验证列名存在

    # 测试绝对路径
    abs_path = os.path.join(test_dir, "test_data", "test_data.csv")
    reader_abs = CSVReader(abs_path)
    data_abs = reader_abs.read()
    assert not data_abs.empty
    assert len(data_abs) == 3

    # 测试当前工作目录的相对路径
    os.chdir(test_dir)  # 切换到测试目录
    reader_cwd = CSVReader("test_data/test_data.csv")
    data_cwd = reader_cwd.read()
    assert not data_cwd.empty
    assert len(data_cwd) == 3
