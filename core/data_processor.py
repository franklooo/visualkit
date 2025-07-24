import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime

class DataProcessor:
    """数据处理核心类"""
    
    @staticmethod
    def validate_dataframe(df: pd.DataFrame, required_cols: List[str]) -> bool:
        """验证DataFrame格式"""
        return all(col in df.columns for col in required_cols)
    
    @staticmethod
    def calculate_yoy_ytd(df: pd.DataFrame, value_col: str, date_col: str) -> Dict[str, float]:
        """计算同比和累计同比"""
        df = df.sort_values(date_col)
        latest = df.iloc[-1][value_col]
        prev_year = df.iloc[-2][value_col] if len(df) >= 2 else np.nan
        
        # 计算同比
        yoy = ((latest - prev_year) / prev_year * 100) if not pd.isna(prev_year) else np.nan
        
        # 计算累计同比
        ytd_current = df[value_col].sum()
        ytd_prev = df.iloc[:-1][value_col].sum() if len(df) > 1 else np.nan
        ytd = ((ytd_current - ytd_prev) / ytd_prev * 100) if ytd_prev else np.nan
        
        return {
            'latest_value': latest,
            'yoy': yoy,
            'ytd': ytd
        }
    
    @staticmethod
    def pivot_for_seasonal(df: pd.DataFrame, date_col: str, value_col: str, 
                          group_by: str = 'year') -> pd.DataFrame:
        """为季节性分析准备透视表"""
        df = df.copy()
        df[date_col] = pd.to_datetime(df[date_col])
        df[group_by] = df[date_col].dt.year
        
        # 按月份分组
        df['month'] = df[date_col].dt.month
        
        pivot = df.pivot_table(
            index='month',
            columns=group_by,
            values=value_col,
            aggfunc='mean'
        ).interpolate(limit_area='inside')
        
        return pivot