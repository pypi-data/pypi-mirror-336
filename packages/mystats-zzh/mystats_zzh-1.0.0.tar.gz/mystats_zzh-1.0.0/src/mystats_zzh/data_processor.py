# mystats/core/data_processor.py
"""
数据预处理工具模块
包含用于统计检验的数据合并、排序和秩分配功能
"""

def merge_groups(group1, group2):
    """合并两组数据并标记来源组别
    Args:
        group1: 实验组数据(值列表)
        group2: 对照组数据(值列表)
    Returns:
        元组列表: [(值, 是否实验组), ...]
    """
    return [(v, True) for v in group1] + [(v, False) for v in group2]

def assign_ranks(sorted_data):
    """为相同值分配平均秩
    Args:
        sorted_data: 已排序的(值, 是否实验组)元组列表
    Returns:
        每个数据点对应的平均秩列表
    """
    ranks = []
    i = 0
    while i < len(sorted_data):
        j = i
        while j < len(sorted_data) and sorted_data[j][0] == sorted_data[i][0]:
            j += 1
        avg_rank = (i + j + 1) / 2
        ranks.extend([avg_rank] * (j - i))
        i = j
    return ranks

def process_and_rank(group1, group2):
    """完整数据处理流程：合并、排序和分配秩
    Args:
        group1: 实验组数据
        group2: 对照组数据
    Returns:
        tuple: (sorted_data, ranks) 其中:
            sorted_data: 合并并排序后的数据
            ranks: 每个数据点对应的秩
    """
    merged_data = merge_groups(group1, group2)
    sorted_data = sorted(merged_data, key=lambda x: x[0])
    ranks = assign_ranks(sorted_data)
    return sorted_data, ranks