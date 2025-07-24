import pytest
import pandas as pd
import numpy as np


@pytest.fixture
def sample_dataframe():
    """创建标准测试数据"""
    dates = pd.date_range('2021-01-01', '2023-12-31', freq='D')
    np.random.seed(42)  # 确保可重复
    
    data = pd.DataFrame({
        'date': dates,
        'open': 100 + np.random.randn(len(dates)).cumsum(),
        'high': 102 + np.random.randn(len(dates)).cumsum(),
        'low': 98 + np.random.randn(len(dates)).cumsum(),
        'close': 101 + np.random.randn(len(dates)).cumsum(),
        'volume': np.random.randint(1000, 10000, len(dates)),
        'price': 100 + np.random.randn(len(dates)).cumsum()
    })
    
    return data


@pytest.fixture
def missing_data_dataframe():
    """创建包含缺失值的数据"""
    dates = pd.date_range('2021-01-01', '2021-12-31', freq='D')
    np.random.seed(42)
    
    data = pd.DataFrame({
        'date': dates,
        'value': 100 + np.random.randn(len(dates)).cumsum()
    })
    
    # 添加一些缺失值
    mask = np.random.random(len(data)) < 0.1
    data.loc[mask, 'value'] = np.nan
    
    return data


@pytest.fixture
def small_dataframe():
    """创建小数据集用于快速测试"""
    dates = pd.date_range('2021-01-01', '2021-01-31', freq='D')
    data = pd.DataFrame({
        'date': dates,
        'value': range(31)
    })
    return data