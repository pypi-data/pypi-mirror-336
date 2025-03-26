from .data_processor import process_and_rank  # 导入数据处理和秩分配函数
from pathlib import Path  # 用于处理文件路径
import os  # 用于操作系统相关功能

class RankSumTest:
    """
    RankSumTest 类用于执行秩和检验，包括小样本和大样本的处理。
    """

    def __init__(self, config_path=None):
        """
        初始化 RankSumTest 类，加载秩和表和 z 分布表。
        :param config_path: 配置文件路径，默认为 None。
        """
        if config_path is None:
            # 默认配置路径为 data_tables 文件夹
            config_path = str(Path(__file__).parent.parent.parent / "data_tables") + os.sep
            # 加载秩和表和 z 分布表
            self.rank_table = self._load_table(os.path.join(config_path, "rank_table.json"))
            self.z_table = self._load_table(os.path.join(config_path, "z_table.json"))

    def execute(self, group1, group2, alpha=None):
        """
        执行秩和检验。
        :param group1: 第一组数据（实验组）。
        :param group2: 第二组数据（对照组）。
        :param alpha: 显著性水平，默认为 None。
        :return: 检验结果。
        """
        # 合并数据并分配秩
        sorted_data, ranks = process_and_rank(group1, group2)
        
        # 计算实验组的秩和
        sum_rank = sum(rank for (value, is_group1), rank in zip(sorted_data, ranks) if is_group1)
        print(f"实验组的秩和: {sum_rank}")
        
        # 获取两组样本大小
        m, n = len(group1), len(group2)
        print(f"样本大小: m={m}, n={n}")
        
        # 根据样本大小选择检验方法
        if m <= 10 and n <= 10:
            # 小样本检验
            result = self._table_lookup(m, n, sum_rank)
        else:
            # 大样本正态近似检验
            result = self._normal_approx(m, n, sum_rank, alpha)
        print(result)
        return result

    def _load_table(self, file_path):
        """
        加载 JSON 格式的表格文件。
        :param file_path: 文件路径。
        :return: 加载的表格数据（字典）。
        """
        import json
        with open(file_path, "r") as f:
            return json.load(f)

    def _table_lookup(self, m, n, sum_rank):
        """
        小样本检验：从秩和表中查找临界值。
        :param m: 第一组样本大小。
        :param n: 第二组样本大小。
        :param sum_rank: 实验组的秩和。
        :return: 检验结果。
        """
        print(f"小样本检验: 查找秩和表 m={m}, n={n}")
        # 从秩和表中查找对应的条目
        entry = self.rank_table.get(f"{m},{n}")
        if not entry:
            raise ValueError(f"秩和表中未找到 {m},{n} 的临界值，请检查数据表或使用大样本正态近似")
        
        # 获取上下临界值
        t_lower = entry.get("T_lower")
        t_upper = entry.get("T_upper")
        print(f"临界值: T_lower={t_lower}, T_upper={t_upper}")
        
        if t_lower is None or t_upper is None:
            raise ValueError(f"秩和表中 {m},{n} 的 T_lower/T_upper 值缺失")
        
        # 判断秩和是否超出临界值范围
        if sum_rank <= t_lower or sum_rank >= t_upper:
            print(f"秩和 {sum_rank} 超出临界值范围，两组间不存在系统误差")
            return "两组间不存在系统误差"
        
        print(f"秩和 {sum_rank} 在临界值范围内，两组间存在系统误差")
        return "两组间存在系统误差"

    def _normal_approx(self, m, n, sum_rank, alpha=None):
        """
        大样本正态近似检验。
        :param m: 第一组样本大小。
        :param n: 第二组样本大小。
        :param sum_rank: 实验组的秩和。
        :param alpha: 显著性水平，默认为 None。
        :return: 检验结果。
        """
        print(f"大样本正态近似检验: m={m}, n={n}")

        # 计算均值和标准差
        mean_rank = m * (m + n + 1) / 2
        std_rank = ((m * n * (m + n + 1)) / 12) ** 0.5
        print(f"均值: {mean_rank}, 标准差: {std_rank}")

        # 计算 t 值
        t = abs((sum_rank - mean_rank) / std_rank)
        print(f"计算得到的 t 值: {t}")

        # 如果未指定 alpha，则根据 t 值选择最接近的概率值
        if alpha is None:
            try:
                # 从 z_table 中找到最接近 t 值的概率值
                closest_alpha = min(
                    self.z_table.keys(),
                    key=lambda a: abs(float(a) - t)  # 使用 z_table 的键作为 alpha
                )
                alpha = closest_alpha
                print(f"自动选择的 alpha: {alpha}")
            except Exception as e:
                raise ValueError(f"无法自动选择 alpha: {e}")

        # 查找 alpha 对应的概率值
        try:
            probability = self.z_table.get(alpha)
            if probability is None:
                raise ValueError(f"z_table 中未找到 alpha={alpha} 对应的概率值")
        except Exception as e:
            raise ValueError(f"无法从 z_table 中获取概率值: {e}")

        print(f"alpha={alpha} 对应的概率值: {probability}")

        # 判断 t 值是否超出临界值范围
        if t > probability:
            print(f"t 值 {t} 超出 alpha={alpha} 的范围")
            return f"存在系统误差的概率为 {1 - probability:.4f},两组之间不存在系统误差"

        print(f"t 值 {t} 在 alpha={alpha} 的范围内")
        return f"存在系统误差的概率为 {probability:.4f}，两组之间存在系统误差"