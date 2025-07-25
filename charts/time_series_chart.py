"""
时间序列图表类
提供时间序列相关的图表功能
"""
import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from pyecharts.charts import Line, Bar
from pyecharts import options as opts
from .base_chart import BaseChart


class TimeSeriesChart(BaseChart):
    """时间序列图表类"""
    
    def __init__(self):
        super().__init__()
    
    def create_chart(self, df: pd.DataFrame, **kwargs) -> Line:
        """创建默认时间序列图表"""
        # 如果没有提供特定的参数，使用默认值
        date_col = kwargs.get('date_col', 'date')
        value_cols = kwargs.get('value_cols', [])
        title = kwargs.get('title', '时间序列图')
        
        # 如果没有指定value_cols，尝试使用所有数值列
        if not value_cols:
            value_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        # 调用现有的create_time_series_line方法
        return self.create_time_series_line(df, date_col, value_cols, title)
    
    def create_time_series_line(
        self,
        df: pd.DataFrame,
        date_col: str,
        value_cols: List[str],
        title: str = "时间序列图",
        subtitle: str = "",
        smooth: bool = False,
        mark_point: bool = False,
        mark_line: bool = False,
        area: bool = False
    ) -> Line:
        """创建时间序列折线图"""
        
        df = df.copy()
        df[date_col] = pd.to_datetime(df[date_col])
        df = df.sort_values(date_col)
        
        # 创建图表
        chart = Line(init_opts=opts.InitOpts(
            width=self.chart_config.get('width', '100%'),
            height=self.chart_config.get('height', '500px')
        ))
        
        # 如果需要面积图，设置面积样式
        if area:
            chart.set_series_opts(
                areastyle_opts=opts.AreaStyleOpts(opacity=0.5)
            )
        
        # 添加x轴数据
        x_data = df[date_col].dt.strftime('%Y-%m-%d').tolist()
        chart.add_xaxis(x_data)
        
        # 添加y轴数据
        for col in value_cols:
            chart.add_yaxis(
                series_name=col,
                y_axis=df[col].tolist(),
                is_smooth=smooth,
                is_symbol_show=True,
                symbol_size=4,
                linestyle_opts=opts.LineStyleOpts(width=2)
            )
        
        # 标记点和线
        mark_point_opts = []
        mark_line_opts = []
        
        if mark_point:
            mark_point_opts = [
                opts.MarkPointOpts(
                    data=[
                        opts.MarkPointItem(type_="max", name="最大值"),
                        opts.MarkPointItem(type_="min", name="最小值")
                    ]
                )
            ]
        
        if mark_line:
            mark_line_opts = [
                opts.MarkLineOpts(
                    data=[
                        opts.MarkLineItem(type_="average", name="平均值")
                    ]
                )
            ]
        
        # 设置全局配置
        chart.set_global_opts(
            title_opts=opts.TitleOpts(
                title=title,
                subtitle=subtitle,
                pos_left="center"
            ),
            tooltip_opts=opts.TooltipOpts(
                trigger="axis",
                axis_pointer_type="cross"
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
                axislabel_opts=opts.LabelOpts(rotate=45)
            ),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                splitline_opts=opts.SplitLineOpts(is_show=True)
            ),
            datazoom_opts=[
                opts.DataZoomOpts(type_="inside", range_start=0, range_end=100),
                opts.DataZoomOpts(type_="slider", range_start=0, range_end=100)
            ]
        )
        
        return chart
    
    def create_candlestick_chart(
        self,
        df: pd.DataFrame,
        date_col: str,
        open_col: str,
        close_col: str,
        low_col: str,
        high_col: str,
        title: str = "K线图",
        subtitle: str = ""
    ) -> Bar:
        """创建K线图（简化版，使用柱状图模拟）"""
        
        df = df.copy()
        df[date_col] = pd.to_datetime(df[date_col])
        df = df.sort_values(date_col)
        
        # 计算涨跌
        df['change'] = df[close_col] - df[open_col]
        df['color'] = np.where(df['change'] >= 0, '#ec0000', '#00da3c')
        
        # 创建图表
        chart = Bar(init_opts=opts.InitOpts(
            width=self.chart_config.get('width', '100%'),
            height=self.chart_config.get('height', '500px')
        ))
        
        x_data = df[date_col].dt.strftime('%Y-%m-%d').tolist()
        chart.add_xaxis(x_data)
        
        # 添加高低范围
        chart.add_yaxis(
            series_name="价格区间",
            y_axis=[[row[low_col], row[high_col]] for _, row in df.iterrows()],
            itemstyle_opts=opts.ItemStyleOpts(color='#ec0000')
        )
        
        self.set_global_opts(chart, title, subtitle)
        return chart
    
    def create_volume_chart(
        self,
        df: pd.DataFrame,
        date_col: str,
        volume_col: str,
        title: str = "成交量图",
        subtitle: str = ""
    ) -> Bar:
        """创建成交量柱状图"""
        
        df = df.copy()
        df[date_col] = pd.to_datetime(df[date_col])
        df = df.sort_values(date_col)
        
        chart = Bar(init_opts=opts.InitOpts(
            width=self.chart_config.get('width', '100%'),
            height=self.chart_config.get('height', '300px')
        ))
        
        x_data = df[date_col].dt.strftime('%Y-%m-%d').tolist()
        chart.add_xaxis(x_data)
        chart.add_yaxis(
            series_name=volume_col,
            y_axis=df[volume_col].tolist(),
            itemstyle_opts=opts.ItemStyleOpts(color='#5470c6')
        )
        
        self.set_global_opts(chart, title, subtitle)
        return chart