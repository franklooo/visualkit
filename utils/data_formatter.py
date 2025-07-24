"""
数据格式化工具
提供各种数据格式化和处理功能
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
import warnings


class DataFormatter:
    """数据格式化类"""
    
    @staticmethod
    def format_date_column(
        df: pd.DataFrame,
        date_col: str,
        format_str: str = '%Y-%m-%d'
    ) -> pd.DataFrame:
        """格式化日期列"""
        df = df.copy()
        
        # 尝试解析日期
        try:
            df[date_col] = pd.to_datetime(df[date_col])
            df[date_col] = df[date_col].dt.strftime(format_str)
        except Exception as e:
            warnings.warn(f"日期格式化失败: {e}")
        
        return df
    
    @staticmethod
    def format_numeric_columns(
        df: pd.DataFrame,
        columns: List[str],
        decimals: int = 2,
        thousands_sep: bool = True
    ) -> pd.DataFrame:
        """格式化数值列"""
        df = df.copy()
        
        for col in columns:
            if col in df.columns:
                # 确保列为数值类型
                df[col] = pd.to_numeric(df[col], errors='coerce')
                
                # 格式化数值
                if thousands_sep:
                    df[col] = df[col].apply(lambda x: f"{x:,.{decimals}f}" if pd.notna(x) else "")
                else:
                    df[col] = df[col].apply(lambda x: f"{x:.{decimals}f}" if pd.notna(x) else "")
        
        return df
    
    @staticmethod
    def handle_missing_values(
        df: pd.DataFrame,
        method: str = 'forward_fill',
        fill_value: Any = None
    ) -> pd.DataFrame:
        """处理缺失值"""
        df = df.copy()
        
        if method == 'forward_fill':
            df = df.fillna(method='ffill')
        elif method == 'backward_fill':
            df = df.fillna(method='bfill')
        elif method == 'interpolate':
            df = df.interpolate()
        elif method == 'mean':
            df = df.fillna(df.mean())
        elif method == 'median':
            df = df.fillna(df.median())
        elif method == 'zero':
            df = df.fillna(0)
        elif method == 'custom':
            df = df.fillna(fill_value)
        else:
            # 默认前向填充
            df = df.fillna(method='ffill')
        
        return df
    
    @staticmethod
    def remove_outliers(
        df: pd.DataFrame,
        columns: List[str],
        method: str = 'iqr',
        threshold: float = 1.5
    ) -> pd.DataFrame:
        """移除异常值"""
        df = df.copy()
        
        for col in columns:
            if col in df.columns:
                if method == 'iqr':
                    Q1 = df[col].quantile(0.25)
                    Q3 = df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - threshold * IQR
                    upper_bound = Q3 + threshold * IQR
                    
                    mask = (df[col] >= lower_bound) & (df[col] <= upper_bound)
                    df = df[mask]
                
                elif method == 'zscore':
                    z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
                    df = df[z_scores < threshold]
        
        return df
    
    @staticmethod
    def normalize_data(
        df: pd.DataFrame,
        columns: List[str],
        method: str = 'min_max'
    ) -> pd.DataFrame:
        """数据归一化"""
        df = df.copy()
        
        for col in columns:
            if col in df.columns:
                if method == 'min_max':
                    min_val = df[col].min()
                    max_val = df[col].max()
                    if max_val != min_val:
                        df[col] = (df[col] - min_val) / (max_val - min_val)
                
                elif method == 'z_score':
                    mean_val = df[col].mean()
                    std_val = df[col].std()
                    if std_val != 0:
                        df[col] = (df[col] - mean_val) / std_val
        
        return df
    
    @staticmethod
    def create_derived_features(
        df: pd.DataFrame,
        date_col: str,
        value_col: str
    ) -> pd.DataFrame:
        """创建衍生特征"""
        df = df.copy()
        
        # 确保日期列为datetime类型
        df[date_col] = pd.to_datetime(df[date_col])
        
        # 时间特征
        df['year'] = df[date_col].dt.year
        df['month'] = df[date_col].dt.month
        df['day'] = df[date_col].dt.day
        df['weekday'] = df[date_col].dt.weekday
        df['quarter'] = df[date_col].dt.quarter
        
        # 移动平均
        df['ma_7'] = df[value_col].rolling(window=7).mean()
        df['ma_30'] = df[value_col].rolling(window=30).mean()
        df['ma_90'] = df[value_col].rolling(window=90).mean()
        
        # 价格变化
        df['change'] = df[value_col].diff()
        df['change_pct'] = df[value_col].pct_change() * 100
        
        # 波动率
        df['volatility'] = df[value_col].rolling(window=30).std()
        
        return df
    
    @staticmethod
    def aggregate_by_period(
        df: pd.DataFrame,
        date_col: str,
        value_cols: List[str],
        period: str = 'M'
    ) -> pd.DataFrame:
        """按时间段聚合数据"""
        df = df.copy()
        
        # 确保日期列为datetime类型
        df[date_col] = pd.to_datetime(df[date_col])
        df.set_index(date_col, inplace=True)
        
        # 聚合
        if period == 'D':
            df_agg = df[value_cols].resample('D').mean()
        elif period == 'W':
            df_agg = df[value_cols].resample('W').mean()
        elif period == 'M':
            df_agg = df[value_cols].resample('M').mean()
        elif period == 'Q':
            df_agg = df[value_cols].resample('Q').mean()
        elif period == 'Y':
            df_agg = df[value_cols].resample('Y').mean()
        else:
            df_agg = df[value_cols].resample('M').mean()
        
        df_agg.reset_index(inplace=True)
        return df_agg
    
    @staticmethod
    def filter_by_date_range(
        df: pd.DataFrame,
        date_col: str,
        start_date: str,
        end_date: str
    ) -> pd.DataFrame:
        """按日期范围过滤数据"""
        df = df.copy()
        
        # 确保日期列为datetime类型
        df[date_col] = pd.to_datetime(df[date_col])
        
        # 过滤
        mask = (df[date_col] >= pd.to_datetime(start_date)) & \
               (df[date_col] <= pd.to_datetime(end_date))
        
        return df[mask]
    
    @staticmethod
    def convert_frequency(
        df: pd.DataFrame,
        date_col: str,
        value_cols: List[str],
        from_freq: str = 'D',
        to_freq: str = 'M'
    ) -> pd.DataFrame:
        """转换数据频率"""
        return DataFormatter.aggregate_by_period(df, date_col, value_cols, to_freq)
    
    @staticmethod
    def create_lag_features(
        df: pd.DataFrame,
        columns: List[str],
        lags: List[int]
    ) -> pd.DataFrame:
        """创建滞后特征"""
        df = df.copy()
        
        for col in columns:
            if col in df.columns:
                for lag in lags:
                    df[f'{col}_lag_{lag}'] = df[col].shift(lag)
        
        return df
    
    @staticmethod
    def calculate_rolling_stats(
        df: pd.DataFrame,
        columns: List[str],
        window: int = 30,
        stats: List[str] = ['mean', 'std', 'min', 'max']
    ) -> pd.DataFrame:
        """计算滚动统计量"""
        df = df.copy()
        
        for col in columns:
            if col in df.columns:
                for stat in stats:
                    col_name = f'{col}_rolling_{stat}_{window}'
                    if stat == 'mean':
                        df[col_name] = df[col].rolling(window=window).mean()
                    elif stat == 'std':
                        df[col_name] = df[col].rolling(window=window).std()
                    elif stat == 'min':
                        df[col_name] = df[col].rolling(window=window).min()
                    elif stat == 'max':
                        df[col_name] = df[col].rolling(window=window).max()
        
        return df