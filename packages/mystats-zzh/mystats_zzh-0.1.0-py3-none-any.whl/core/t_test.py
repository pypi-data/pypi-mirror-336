import numpy as np
from scipy import stats

def t_tests(
    group1: list, 
    group2: list, 
    alpha: float = 0.05
) -> dict:
    """
    执行两组数据的独立样本t检验
    
    Args:
        group1 (list): 第一组数据
        group2 (list): 第二组数据
        alpha (float): 显著性水平（默认0.05）
    
    Returns:
        dict: 包含t统计量、p值、自由度、临界值、结论的字典
    """
    # 计算t统计量和p值
    t_stat, p_value = stats.ttest_ind(group1, group2)
    
    # 计算自由度
    n1, n2 = len(group1), len(group2)
    dof = n1 + n2 - 2
    
    # 获取临界值（双尾检验）
    critical_value = stats.t.ppf(1 - alpha/2, dof)
    
    # 判断结论
    reject_null = abs(t_stat) > critical_value or p_value < alpha
    
    rus={
        "t_statistic": round(t_stat, 4),
        "p_value": round(p_value, 4),
        "degrees_of_freedom": dof,
        "critical_value": '临界值为：'f'{round(critical_value, 4)}',
        "reject_null_hypothesis": reject_null,
        "description": f"当显著度为{alpha}时，怀疑两组之间存在系统误差" if reject_null else f"当显著度为{alpha}时，不能怀疑两组之间存在系统误差"
    }

    return f' 自由度为：{rus.get("degrees_of_freedom")}\n {rus.get("critical_value")}\n{rus.get("description")}'    
