"""
数据可视化工具包
基于pyecharts的现代季节性分析工具
"""

__version__ = "1.0.0"
__author__ = "Data Visualization Team"
__description__ = "基于pyecharts的现代季节性分析工具包"

# 导入核心模块
from .core.data_processor import DataProcessor
from .core.calendar_manager import CalendarManager
from .core.wind_client import WindClient, WindDataProcessor

# 导入图表模块
from .charts.base_chart import BaseChart, ChartConfig
from .charts.seasonal_chart import SeasonalChart
from .charts.time_series_chart import TimeSeriesChart

# 导入工具模块
from .utils.data_formatter import DataFormatter
from .utils.template_manager import TemplateManager

# 设置默认配置
DEFAULT_CONFIG = {
    'colors': [
        '#5470c6', '#91cc75', '#fac858', '#ee6666',
        '#73c0de', '#3ba272', '#fc8452', '#9a60b4'
    ],
    'chart_width': '100%',
    'chart_height': '500px',
    'theme': 'white'
}

__all__ = [
    # 核心类
    'DataProcessor',
    'CalendarManager',
    'WindClient',
    'WindDataProcessor',
    
    # 图表类
    'BaseChart',
    'ChartConfig',
    'SeasonalChart',
    'TimeSeriesChart',
    
    # 工具类
    'DataFormatter',
    'TemplateManager',
    
    # 配置
    'DEFAULT_CONFIG'
]