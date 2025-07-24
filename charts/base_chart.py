"""
基础图表类
提供通用的图表功能和配置
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import pandas as pd
from pyecharts.charts import Line, Bar, Scatter
from pyecharts import options as opts


class BaseChart(ABC):
    """所有图表类的基类"""
    
    def __init__(self):
        self.chart_config = {}
        self.default_colors = [
            '#5470c6', '#91cc75', '#fac858', '#ee6666', 
            '#73c0de', '#3ba272', '#fc8452', '#9a60b4'
        ]
    
    @abstractmethod
    def create_chart(self, df: pd.DataFrame, **kwargs) -> Any:
        """创建图表的抽象方法"""
        pass
    
    def set_global_opts(self, chart: Any, title: str, subtitle: str = "") -> None:
        """设置图表的全局配置"""
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
            datazoom_opts=[
                opts.DataZoomOpts(type_="inside", range_start=0, range_end=100),
                opts.DataZoomOpts(type_="slider", range_start=0, range_end=100)
            ]
        )
    
    def save_chart(self, chart: Any, filename: str) -> None:
        """保存图表为HTML文件"""
        chart.render(filename)
    
    def get_chart_options(self, chart: Any) -> Dict[str, Any]:
        """获取图表配置"""
        return chart.dump_options_with_quotes()


class ChartConfig:
    """图表配置管理器"""
    
    def __init__(self):
        self.config = {
            'width': '100%',
            'height': '500px',
            'theme': 'white',
            'animation': True,
            'renderer': 'canvas'
        }
    
    def update_config(self, **kwargs) -> None:
        """更新配置"""
        self.config.update(kwargs)
    
    def get_config(self) -> Dict[str, Any]:
        """获取当前配置"""
        return self.config.copy()