"""
akshare数据接口模块
提供通过akshare获取金融和市场数据的便捷接口
"""

import pandas as pd
import akshare as ak
from typing import Dict, List, Optional, Union
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings('ignore')


class AkShareClient:
    """akshare数据客户端"""
    
    @staticmethod
    def get_stock_daily(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        获取股票日线数据
        
        Args:
            symbol: 股票代码 (如: 000001, 600000)
            start_date: 开始日期 (格式: YYYYMMDD)
            end_date: 结束日期 (格式: YYYYMMDD)
            
        Returns:
            DataFrame: 包含日期、开盘价、最高价、最低价、收盘价、成交量
        """
        try:
            # 根据股票代码前缀判断市场
            if symbol.startswith(('6', '5')):
                # 上证股票
                stock_zh_a_spot_df = ak.stock_zh_a_hist(
                    symbol=symbol,
                    period="daily",
                    start_date=start_date,
                    end_date=end_date,
                    adjust=""
                )
            else:
                # 深证股票
                stock_zh_a_spot_df = ak.stock_zh_a_hist(
                    symbol=symbol,
                    period="daily",
                    start_date=start_date,
                    end_date=end_date,
                    adjust=""
                )
            
            if stock_zh_a_spot_df.empty:
                raise ValueError(f"无法获取股票 {symbol} 的数据")
                
            # 重命名列以符合项目标准
            stock_zh_a_spot_df = stock_zh_a_spot_df.rename(columns={
                '日期': 'date',
                '开盘': 'open',
                '最高': 'high',
                '最低': 'low',
                '收盘': 'close',
                '成交量': 'volume'
            })
            
            # 确保日期格式正确
            stock_zh_a_spot_df['date'] = pd.to_datetime(stock_zh_a_spot_df['date'])
            
            return stock_zh_a_spot_df[['date', 'open', 'high', 'low', 'close', 'volume']]
            
        except Exception as e:
            raise RuntimeError(f"获取股票数据失败: {str(e)}")
    
    @staticmethod
    def get_index_daily(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        获取指数日线数据
        
        Args:
            symbol: 指数代码 (如: sh000001, sz399001)
            start_date: 开始日期 (格式: YYYYMMDD)
            end_date: 结束日期 (格式: YYYYMMDD)
            
        Returns:
            DataFrame: 包含日期、开盘价、最高价、最低价、收盘价、成交量
        """
        try:
            # 获取指数历史数据
            index_df = ak.index_zh_a_hist(
                symbol=symbol,
                period="daily",
                start_date=start_date,
                end_date=end_date
            )
            
            if index_df.empty:
                raise ValueError(f"无法获取指数 {symbol} 的数据")
                
            # 重命名列
            index_df = index_df.rename(columns={
                '日期': 'date',
                '开盘': 'open',
                '最高': 'high',
                '最低': 'low',
                '收盘': 'close',
                '成交量': 'volume'
            })
            
            index_df['date'] = pd.to_datetime(index_df['date'])
            
            return index_df[['date', 'open', 'high', 'low', 'close', 'volume']]
            
        except Exception as e:
            raise RuntimeError(f"获取指数数据失败: {str(e)}")
    
    @staticmethod
    def get_futures_daily(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        获取期货日线数据
        
        Args:
            symbol: 期货代码 (如: CU0, AL0)
            start_date: 开始日期 (格式: YYYYMMDD)
            end_date: 结束日期 (格式: YYYYMMDD)
            
        Returns:
            DataFrame: 包含日期、开盘价、最高价、最低价、收盘价、成交量
        """
        try:
            # 获取期货历史数据
            futures_df = ak.futures_zh_daily_sina(symbol=symbol)
            
            if futures_df.empty:
                raise ValueError(f"无法获取期货 {symbol} 的数据")
                
            # 筛选日期范围
            futures_df['date'] = pd.to_datetime(futures_df['date'])
            mask = (futures_df['date'] >= pd.to_datetime(start_date)) & \
                   (futures_df['date'] <= pd.to_datetime(end_date))
            futures_df = futures_df[mask]
            
            # 重命名列
            futures_df = futures_df.rename(columns={
                'open': 'open',
                'high': 'high',
                'low': 'low',
                'close': 'close',
                'volume': 'volume'
            })
            
            return futures_df[['date', 'open', 'high', 'low', 'close', 'volume']]
            
        except Exception as e:
            raise RuntimeError(f"获取期货数据失败: {str(e)}")
    
    @staticmethod
    def get_economic_indicator(indicator: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        获取经济指标数据
        
        Args:
            indicator: 指标名称 (如: CPI, PPI, GDP)
            start_date: 开始日期 (格式: YYYY-MM-DD)
            end_date: 结束日期 (格式: YYYY-MM-DD)
            
        Returns:
            DataFrame: 包含日期和指标值
        """
        try:
            if indicator.upper() == 'CPI':
                # 获取CPI数据
                data = ak.macro_china_cpi()
                data = data.rename(columns={
                    '日期': 'date',
                    '今值': 'value'
                })
            elif indicator.upper() == 'PPI':
                # 获取PPI数据
                data = ak.macro_china_ppi()
                data = data.rename(columns={
                    '日期': 'date',
                    '今值': 'value'
                })
            else:
                raise ValueError(f"不支持的经济指标: {indicator}")
            
            data['date'] = pd.to_datetime(data['date'])
            mask = (data['date'] >= pd.to_datetime(start_date)) & \
                   (data['date'] <= pd.to_datetime(end_date))
            
            return data[['date', 'value']]
            
        except Exception as e:
            raise RuntimeError(f"获取经济指标数据失败: {str(e)}")
    
    @staticmethod
    def get_demo_data(data_type: str = "stock", days: int = 365) -> pd.DataFrame:
        """
        获取演示数据
        
        Args:
            data_type: 数据类型 (stock, index, futures)
            days: 获取最近多少天的数据
            
        Returns:
            DataFrame: 演示数据
        """
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y%m%d')
        
        if data_type == "stock":
            return AkShareClient.get_stock_daily("000001", start_date, end_date)
        elif data_type == "index":
            return AkShareClient.get_index_daily("sh000001", start_date, end_date)
        elif data_type == "futures":
            return AkShareClient.get_futures_daily("CU0", start_date, end_date)
        else:
            raise ValueError(f"不支持的数据类型: {data_type}")
    
    @staticmethod
    def list_available_symbols(data_type: str) -> List[str]:
        """
        列出可用的数据代码
        
        Args:
            data_type: 数据类型 (stock, index, futures)
            
        Returns:
            List[str]: 可用的代码列表
        """
        try:
            if data_type == "stock":
                # 获取A股股票列表
                stock_list = ak.stock_zh_a_spot()
                return stock_list['代码'].tolist()[:50]  # 返回前50个
            elif data_type == "index":
                # 获取指数列表
                index_list = ak.index_stock_zh()
                return index_list['代码'].tolist()[:20]  # 返回前20个
            elif data_type == "futures":
                # 获取期货列表
                futures_list = ak.futures_display_main_sina()
                return futures_list['symbol'].tolist()[:30]  # 返回前30个
            else:
                return []
        except Exception:
            return []