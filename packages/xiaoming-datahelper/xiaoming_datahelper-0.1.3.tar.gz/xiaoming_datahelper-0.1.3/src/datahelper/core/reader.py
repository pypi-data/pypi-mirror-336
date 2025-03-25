import os
import pandas as pd


class CSVReader:
    def __init__(self, filepath, base_dir=None):
        """
        初始化 CSVReader

        Args:
            filepath (str): CSV 文件路径，可以是相对路径或绝对路径
            base_dir (str, optional): 相对路径的基准目录。如果为 None，则使用当前工作目录
        """
        self.filepath = filepath
        self.base_dir = base_dir or os.getcwd()

    def read(self):
        """
        读取 CSV 文件

        Returns:
            pd.DataFrame: 读取的数据
        """
        # 如果是绝对路径，直接使用
        if os.path.isabs(self.filepath):
            return pd.read_csv(self.filepath)

        # 如果是相对路径，则基于 base_dir 构建完整路径
        full_path = os.path.join(self.base_dir, self.filepath)
        return pd.read_csv(full_path)
