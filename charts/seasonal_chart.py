from pyecharts import options as opts
from pyecharts.charts import Line, Grid, Page
from pyecharts.commons.utils import JsCode
from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np
from datetime import datetime

from ..core.data_processor import DataProcessor

class SeasonalChart:
    """季节性图表生成器（基于pyecharts）"""
    
    DEFAULT_COLORS = [
        '#5470c6', '#91cc75', '#fac858', '#ee6666', 
        '#73c0de', '#3ba272', '#fc8452', '#9a60b4'
    ]
    
    def __init__(self):
        self.data_processor = DataProcessor()
    
    def create_seasonal_line(
        self,
        df: pd.DataFrame,
        date_col: str = 'date',
        value_col: str = 'value',
        title: str = "季节性分析",
        subtitle: str = "",
        years: int = 5,
        calendar_type: str = 'gregorian',  # 'gregorian' or 'lunar'
        spring_range: Tuple[int, int] = (-70, 70),
        show_yoy: bool = True,
        width: str = "100%",
        height: str = "500px"
    ) -> Line:
        """创建季节性折线图"""
        
        # 数据准备
        if calendar_type == 'lunar':
            processed_df = self._prepare_lunar_data(df, date_col, value_col, spring_range)
            x_col = 'lunar_day'
            x_label = "距离春节天数"
        else:
            processed_df = self._prepare_gregorian_data(df, date_col, value_col)
            x_col = 'month'
            x_label = "月份"
        
        # 选择最近N年
        latest_years = sorted(processed_df['year'].unique())[-years:]
        chart_data = processed_df[processed_df['year'].isin(latest_years)]
        
        # 计算统计值
        stats = self.data_processor.calculate_yoy_ytd(
            df.sort_values(date_col), 
            value_col, 
            date_col
        )
        
        # 创建图表
        line = Line(init_opts=opts.InitOpts(width=width, height=height))
        
        # 添加x轴数据
        x_data = chart_data[x_col].unique().tolist()
        x_data.sort()
        
        for year in latest_years:
            year_data = chart_data[chart_data['year'] == year]
            y_data = year_data.set_index(x_col).reindex(x_data)[value_col].tolist()
            
            # 高亮最新年份
            is_latest = year == latest_years[-1]
            line.add_yaxis(
                series_name=str(year),
                y_axis=y_data,
                is_symbol_show=is_latest,
                symbol_size=6 if is_latest else 0,
                linestyle_opts=opts.LineStyleOpts(
                    width=3 if is_latest else 2,
                    color=self.DEFAULT_COLORS[latest_years.index(year) % len(self.DEFAULT_COLORS)]
                ),
                itemstyle_opts=opts.ItemStyleOpts(
                    color=self.DEFAULT_COLORS[latest_years.index(year) % len(self.DEFAULT_COLORS)]
                ),
                label_opts=opts.LabelOpts(is_show=is_latest)
            )
        
        # 全局配置
        line.set_global_opts(
            title_opts=opts.TitleOpts(
                title=title,
                subtitle=f"{subtitle} | 最新值: {stats['latest_value']:.2f} | YoY: {stats['yoy']:.1f}% | YTD: {stats['ytd']:.1f}%",
                pos_left="center"
            ),
            tooltip_opts=opts.TooltipOpts(
                trigger="axis",
                axis_pointer_type="cross",
                formatter=JsCode("""
                    function(params) {
                        let result = params[0].axisValue + '<br/>';
                        params.forEach(param => {
                            result += param.marker + param.seriesName + ': ' + param.value.toFixed(2) + '<br/>';
                        });
                        return result;
                    }
                """)
            ),
            legend_opts=opts.LegendOpts(
                type_="scroll",
                orient="horizontal",
                pos_top="5%",
                pos_left="center"
            ),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                boundary_gap=False,
                name=x_label,
                name_location="middle",
                name_gap=30,
                axislabel_opts=opts.LabelOpts(rotate=0)
            ),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                splitline_opts=opts.SplitLineOpts(is_show=True),
                axislabel_opts=opts.LabelOpts(formatter="{value}")
            ),
            datazoom_opts=[
                opts.DataZoomOpts(type_="inside", range_start=0, range_end=100),
                opts.DataZoomOpts(type_="slider", range_start=0, range_end=100)
            ]
        )
        
        line.add_xaxis(x_data)
        
        return line
    
    def create_seasonal_grid(
        self,
        df: pd.DataFrame,
        date_col: str = 'date',
        value_cols: List[str] = None,
        **kwargs
    ) -> Grid:
        """创建多指标季节性网格图"""
        
        if value_cols is None:
            value_cols = [col for col in df.columns if col != date_col]
        
        charts = []
        for col in value_cols:
            chart = self.create_seasonal_line(
                df[[date_col, col]].rename(columns={col: 'value'}),
                date_col=date_col,
                value_col='value',
                title=col,
                **kwargs
            )
            charts.append(chart)
        
        # 创建网格布局
        grid = Grid(init_opts=opts.InitOpts(width="100%", height=f"{400 * len(charts)}px"))
        
        for idx, chart in enumerate(charts):
            grid.add(
                chart,
                grid_opts=opts.GridOpts(
                    pos_top=f"{idx * 400 + 50}px",
                    height="350px"
                )
            )
        
        return grid
    
    def _prepare_gregorian_data(self, df: pd.DataFrame, date_col: str, value_col: str) -> pd.DataFrame:
        """准备公历数据"""
        df = df.copy()
        df[date_col] = pd.to_datetime(df[date_col])
        df['year'] = df[date_col].dt.year
        df['month'] = df[date_col].dt.month
        return df
    
    def _prepare_lunar_data(
        self, 
        df: pd.DataFrame, 
        date_col: str, 
        value_col: str,
        spring_range: Tuple[int, int]
    ) -> pd.DataFrame:
        """准备农历数据（春节对齐）"""
        from ..core.calendar_manager import CalendarManager
        
        calendar = CalendarManager()
        return calendar.get_lunar_aligned_data(df, date_col, value_col, spring_range)