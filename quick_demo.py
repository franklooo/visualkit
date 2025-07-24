#!/usr/bin/env python3
"""
快速演示脚本 - 使用akshare数据
一键运行可视化工具包演示
"""

import sys
import os
from datetime import datetime, timedelta

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_akshare_demo():
    """运行akshare数据演示"""
    print("🚀 启动akshare数据演示...")
    
    try:
        from core.akshare_client import AkShareClient
        from charts.seasonal_chart import SeasonalChart
        from charts.time_series_chart import TimeSeriesChart
        
        # 获取平安银行股票数据
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=730)).strftime('%Y%m%d')
        
        print(f"📊 获取平安银行(000001)数据...")
        df = AkShareClient.get_stock_daily("000001", start_date, end_date)
        
        # 添加演示字段
        import numpy as np
        df['inventory'] = df['close'] * 100 + np.random.normal(0, 100, len(df))
        df['production'] = df['close'] * 80 + np.random.normal(0, 50, len(df))
        
        print(f"✅ 获取数据成功: {len(df)}条记录")
        print(f"📅 数据范围: {df['date'].min()} 到 {df['date'].max()}")
        
        # 创建季节性图表
        print("📈 生成季节性分析图表...")
        chart = SeasonalChart()
        
        # 公历季节性分析
        seasonal_chart = chart.create_seasonal_line(
            df,
            date_col='date',
            value_col='close',
            title="平安银行股价季节性分析",
            subtitle=f"数据范围: {df['date'].min().strftime('%Y-%m-%d')} - {df['date'].max().strftime('%Y-%m-%d')}",
            calendar_type='gregorian',
            years=2
        )
        seasonal_chart.render("akshare_seasonal_demo.html")
        print("✅ 季节性图表已保存: akshare_seasonal_demo.html")
        
        # 时间序列图
        print("📊 生成时间序列图表...")
        ts_chart = TimeSeriesChart()
        ts_line = ts_chart.create_time_series_line(
            df,
            date_col='date',
            value_cols=['close', 'volume'],
            title="平安银行股价与成交量",
            subtitle="基于akshare真实数据",
            smooth=True,
            mark_point=True
        )
        ts_line.render("akshare_timeseries_demo.html")
        print("✅ 时间序列图表已保存: akshare_timeseries_demo.html")
        
        print("\n🎉 akshare数据演示完成！")
        print("\n生成的文件:")
        print("- akshare_seasonal_demo.html")
        print("- akshare_timeseries_demo.html")
        
        return True
        
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请安装akshare: pip install akshare")
        return False
    except Exception as e:
        print(f"❌ 运行失败: {e}")
        return False

def show_available_data():
    """显示可用的akshare数据"""
    try:
        from core.akshare_client import AkShareClient
        
        print("\n📋 可用的akshare数据源:")
        
        # 股票代码
        stock_symbols = AkShareClient.list_available_symbols("stock")
        print(f"\n📈 股票代码示例:")
        for symbol in stock_symbols[:10]:
            print(f"  {symbol}")
        
        # 指数代码
        index_symbols = AkShareClient.list_available_symbols("index")
        print(f"\n📊 指数代码示例:")
        for symbol in index_symbols[:5]:
            print(f"  {symbol}")
            
        print("\n💡 使用示例:")
        print("  python -c \"from core.akshare_client import AkShareClient; df = AkShareClient.get_stock_daily('000001', '20230101', '20231231'); print(df.head())\"")
        
    except ImportError:
        print("请先安装akshare: pip install akshare")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "list":
        show_available_data()
    else:
        success = run_akshare_demo()
        if not success:
            print("\n📚 快速开始指南:")
            print("1. 安装akshare: pip install akshare")
            print("2. 运行演示: python quick_demo.py")
            print("3. 查看可用数据: python quick_demo.py list")