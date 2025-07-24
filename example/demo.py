"""
数据可视化工具包完整演示
展示所有功能的使用方法，包括akshare数据接口
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from visualization_toolkit import (
    SeasonalChart, TimeSeriesChart, DataFormatter,
    TemplateManager, WindClient, DataProcessor
)

# 导入akshare客户端
try:
    from core.akshare_client import AkShareClient
    AKSHARE_AVAILABLE = True
except ImportError:
    AKSHARE_AVAILABLE = False
    print("⚠️ akshare未安装，将使用模拟数据")


def generate_comprehensive_data():
    """生成综合演示数据"""
    np.random.seed(42)
    
    # 生成3年的日度数据
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2024, 12, 31)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # 模拟多种数据模式
    n_days = len(date_range)
    
    # 价格数据（带趋势和季节性）
    trend = np.linspace(100, 150, n_days)
    seasonal = 20 * np.sin(2 * np.pi * np.arange(n_days) / 365.25)
    noise = np.random.normal(0, 5, n_days)
    price = trend + seasonal + noise
    
    # 成交量数据
    volume_base = 1000000
    volume = volume_base * (1 + 0.5 * np.sin(2 * np.pi * np.arange(n_days) / 30))
    volume = volume * (1 + np.random.normal(0, 0.2, n_days))
    volume = np.maximum(volume, 100000)
    
    # 库存数据（强季节性）
    inventory_base = 5000
    inventory_seasonal = 1000 * np.sin(2 * np.pi * np.arange(n_days) / 365.25 + np.pi/2)
    inventory = inventory_base + inventory_seasonal + np.random.normal(0, 200, n_days)
    
    # 产量数据
    production_base = 8000
    production = production_base + 500 * np.sin(2 * np.pi * np.arange(n_days) / 365.25)
    production = production * (1 + np.random.normal(0, 0.1, n_days))
    
    df = pd.DataFrame({
        'date': date_range,
        'price': price,
        'volume': volume.astype(int),
        'inventory': inventory.astype(int),
        'production': production.astype(int)
    })
    
    # 添加一些缺失值
    mask = np.random.random(n_days) < 0.02
    df.loc[mask, 'price'] = np.nan
    
    return df


def demo_akshare_data():
    """演示akshare数据获取"""
    if not AKSHARE_AVAILABLE:
        print("\n=== akshare数据演示 (不可用) ===")
        print("请先安装akshare: pip install akshare")
        return None
    
    print("\n=== akshare数据演示 ===")
    
    try:
        # 获取股票数据示例
        print("正在获取股票数据...")
        stock_df = AkShareClient.get_demo_data("stock", 365)
        print(f"✓ 获取股票数据成功: {len(stock_df)}条记录")
        print(f"  数据范围: {stock_df['date'].min()} 到 {stock_df['date'].max()}")
        
        # 获取指数数据示例
        print("正在获取指数数据...")
        index_df = AkShareClient.get_demo_data("index", 365)
        print(f"✓ 获取指数数据成功: {len(index_df)}条记录")
        
        # 显示可用代码
        print("\n可用股票代码示例:")
        stock_symbols = AkShareClient.list_available_symbols("stock")
        print(f"  前10个股票代码: {stock_symbols[:10]}")
        
        print("\n可用指数代码示例:")
        index_symbols = AkShareClient.list_available_symbols("index")
        print(f"  主要指数代码: {index_symbols[:5]}")
        
        return stock_df
        
    except Exception as e:
        print(f"❌ akshare数据获取失败: {str(e)}")
        print("将使用模拟数据继续演示")
        return None


def demo_seasonal_analysis():
    """演示季节性分析"""
    print("=== 季节性分析演示 ===")
    
    # 生成数据
    df = generate_comprehensive_data()
    
    # 创建季节性图表
    chart = SeasonalChart()
    
    # 1. 公历季节性分析
    seasonal_line = chart.create_seasonal_line(
        df,
        date_col='date',
        value_col='inventory',
        title="库存季节性分析（公历）",
        subtitle="2022-2024年数据",
        calendar_type='gregorian',
        years=3
    )
    seasonal_line.render("demo_seasonal_gregorian.html")
    print("✓ 公历季节性图表已保存: demo_seasonal_gregorian.html")
    
    # 2. 农历春节对齐分析
    lunar_line = chart.create_seasonal_line(
        df,
        date_col='date',
        value_col='inventory',
        title="春节前后库存变化（农历）",
        subtitle="春节前后60天",
        calendar_type='lunar',
        spring_range=(-60, 60),
        years=3
    )
    lunar_line.render("demo_seasonal_lunar.html")
    print("✓ 农历季节性图表已保存: demo_seasonal_lunar.html")
    
    # 3. 多指标网格图
    grid_chart = chart.create_seasonal_grid(
        df,
        date_col='date',
        value_cols=['price', 'inventory', 'production'],
        title="多指标季节性对比",
        subtitle="综合数据分析",
        years=3
    )
    grid_chart.render("demo_seasonal_grid.html")
    print("✓ 多指标网格图已保存: demo_seasonal_grid.html")


def demo_time_series_analysis():
    """演示时间序列分析"""
    print("\n=== 时间序列分析演示 ===")
    
    # 生成数据
    df = generate_comprehensive_data()
    
    # 创建时间序列图表
    ts_chart = TimeSeriesChart()
    
    # 1. 基础时间序列图
    ts_line = ts_chart.create_time_series_line(
        df,
        date_col='date',
        value_cols=['price', 'inventory'],
        title="价格与库存时间序列",
        subtitle="2022-2024年",
        smooth=True,
        mark_point=True,
        mark_line=True
    )
    ts_line.render("demo_time_series.html")
    print("✓ 时间序列图表已保存: demo_time_series.html")
    
    # 2. 成交量图
    volume_chart = ts_chart.create_volume_chart(
        df,
        date_col='date',
        volume_col='volume',
        title="成交量分析",
        subtitle="日度成交量变化"
    )
    volume_chart.render("demo_volume.html")
    print("✓ 成交量图表已保存: demo_volume.html")


def demo_data_processing():
    """演示数据处理功能"""
    print("\n=== 数据处理演示 ===")
    
    # 生成原始数据
    df = generate_comprehensive_data()
    
    # 使用DataFormatter处理数据
    formatter = DataFormatter()
    
    # 1. 处理缺失值
    df_cleaned = formatter.handle_missing_values(
        df,
        method='interpolate'
    )
    print(f"✓ 数据清洗完成，处理前: {len(df)}, 处理后: {len(df_cleaned)}")
    
    # 2. 创建衍生特征
    df_features = formatter.create_derived_features(
        df_cleaned,
        date_col='date',
        value_col='price'
    )
    print(f"✓ 衍生特征创建完成，新增特征: {len(df_features.columns) - len(df_cleaned.columns)}")
    
    # 3. 数据归一化
    df_normalized = formatter.normalize_data(
        df_features,
        columns=['price', 'volume', 'inventory', 'production']
    )
    print("✓ 数据归一化完成")
    
    return df_normalized


def demo_template_system():
    """演示模板系统"""
    print("\n=== 模板系统演示 ===")
    
    template_manager = TemplateManager()
    
    # 1. 列出所有模板
    templates = template_manager.list_templates()
    print(f"✓ 可用模板: {templates}")
    
    # 2. 获取模板配置
    seasonal_config = template_manager.get_template_config('seasonal_chart')
    print(f"✓ 季节性模板配置已加载，包含 {len(seasonal_config)} 个配置项")
    
    # 3. 创建自定义模板
    custom_config = {
        "colors": ['#FF6B6B', '#4ECDC4', '#45B7D1'],
        "layout": {
            "width": "1200px",
            "height": "600px"
        }
    }
    
    success = template_manager.create_custom_template(
        'seasonal_chart',
        custom_config,
        'my_custom_seasonal'
    )
    
    if success:
        print("✓ 自定义模板已创建: my_custom_seasonal")
    else:
        print("✗ 自定义模板创建失败")


def demo_wind_client():
    """演示Wind客户端功能"""
    print("\n=== Wind客户端演示 ===")
    
    # 创建Wind客户端（模拟模式）
    wind_client = WindClient()
    
    # 连接（模拟）
    if wind_client.connect():
        print("✓ Wind API连接成功")
        
        # 获取模拟历史数据
        df_wind = wind_client.get_history_data(
            codes=['000001.SZ', '000002.SZ'],
            fields=['CLOSE', 'VOLUME'],
            start_date='2024-01-01',
            end_date='2024-12-31'
        )
        
        if not df_wind.empty:
            print(f"✓ 获取到模拟数据: {len(df_wind)} 条记录")
            print("前5行数据:")
            print(df_wind.head())
        else:
            print("✗ 未获取到数据")
    else:
        print("✗ Wind API连接失败")


def demo_data_processor():
    """演示数据处理器功能"""
    print("\n=== 数据处理器演示 ===")
    
    processor = DataProcessor()
    
    # 生成数据
    df = generate_comprehensive_data()
    
    # 计算统计指标
    stats = processor.calculate_yoy_ytd(
        df.sort_values('date'),
        'price',
        'date'
    )
    
    print("✓ 统计指标计算完成:")
    print(f"  最新值: {stats['latest_value']:.2f}")
    print(f"  同比: {stats['yoy']:.2f}%")
    print(f"  累计同比: {stats['ytd']:.2f}%")
    
    # 创建透视表
    pivot = processor.pivot_for_seasonal(
        df,
        date_col='date',
        value_col='price',
        group_by='year'
    )
    
    print("✓ 透视表创建完成")
    print("透视表形状:", pivot.shape)


def demo_akshare_seasonal():
    """使用akshare数据进行季节性分析演示"""
    if not AKSHARE_AVAILABLE:
        print("akshare不可用，使用模拟数据")
        return generate_comprehensive_data()
    
    try:
        # 获取平安银行股票数据
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=730)).strftime('%Y%m%d')
        
        df = AkShareClient.get_stock_daily("000001", start_date, end_date)
        
        # 为演示添加更多字段
        df['inventory'] = df['close'] * 100 + np.random.normal(0, 100, len(df))
        df['production'] = df['close'] * 80 + np.random.normal(0, 50, len(df))
        
        print(f"✓ 使用akshare真实数据: {len(df)}条记录")
        return df
        
    except Exception as e:
        print(f"akshare数据获取失败，使用模拟数据: {e}")
        return generate_comprehensive_data()


def main():
    """主函数：运行所有演示"""
    print("🚀 数据可视化工具包完整演示开始")
    print("=" * 50)
    
    try:
        # 选择数据源
        use_akshare = True if AKSHARE_AVAILABLE else False
        
        # 获取数据
        if use_akshare:
            df = demo_akshare_seasonal()
        else:
            df = generate_comprehensive_data()
            print("使用模拟数据进行演示")
        
        # 运行演示
        demo_seasonal_analysis()
        demo_time_series_analysis()
        demo_data_processing()
        demo_template_system()
        demo_wind_client()
        demo_data_processor()
        
        print("\n" + "=" * 50)
        print("✅ 所有演示完成！")
        print("\n生成的文件:")
        files = [
            "demo_seasonal_gregorian.html",
            "demo_seasonal_lunar.html",
            "demo_seasonal_grid.html",
            "demo_time_series.html",
            "demo_volume.html"
        ]
        for file in files:
            print(f"  - {file}")
            
    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()