"""
核心模块
提供数据处理、日历管理和数据获取功能
"""

from .data_processor import DataProcessor
from .calendar_manager import CalendarManager
from .wind_client import WindClient

# 新增akshare客户端支持
try:
    from .akshare_client import AkShareClient
    __all__ = ['DataProcessor', 'CalendarManager', 'WindClient', 'AkShareClient']
except ImportError:
    # akshare未安装时跳过
    __all__ = ['DataProcessor', 'CalendarManager', 'WindClient']