import pandas as pd
from datetime import datetime
from typing import Tuple

class CalendarManager:
    """日历管理器（处理农历春节对齐等）"""
    
    SPRING_FESTIVAL_DATES = {
        2016: '2016-02-08', 2017: '2017-01-28', 2018: '2018-02-16',
        2019: '2019-02-04', 2020: '2020-01-25', 2021: '2021-02-12',
        2022: '2022-02-01', 2023: '2023-01-22', 2024: '2024-02-10',
        2025: '2025-01-29',
    }
    
    def get_lunar_aligned_data(
        self, 
        df: pd.DataFrame, 
        date_col: str, 
        value_col: str,
        spring_range: Tuple[int, int]
    ) -> pd.DataFrame:
        """获取春节对齐的数据"""
        
        df = df.copy()
        df[date_col] = pd.to_datetime(df[date_col])
        
        # 获取有效年份
        valid_years = [y for y in df['date'].dt.year.unique() 
                      if y in self.SPRING_FESTIVAL_DATES]
        
        processed_data = []
        
        for year in valid_years:
            festival_date = pd.to_datetime(self.SPRING_FESTIVAL_DATES[year])
            
            # 计算日期范围
            date_range = pd.date_range(
                festival_date + pd.Timedelta(days=spring_range[0]),
                festival_date + pd.Timedelta(days=spring_range[1])
            )
            
            # 创建临时DataFrame
            temp_df = pd.DataFrame({
                date_col: date_range,
                'year': year,
                'lunar_day': (date_range - festival_date).days
            })
            
            # 合并数据
            merged = pd.merge(
                temp_df,
                df[[date_col, value_col]],
                on=date_col,
                how='left'
            )
            
            processed_data.append(merged)
        
        # 合并所有年份数据
        result = pd.concat(processed_data)
        result = result.sort_values(date_col)
        
        # 插值处理缺失值
        return result.interpolate(limit_area='inside')