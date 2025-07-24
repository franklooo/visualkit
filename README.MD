以下是重构后的可视化工具包文档，以Markdown格式呈现：

# 📊 数据可视化工具包重构文档

*基于pyecharts的现代季节性分析工具，集成akshare数据接口*

## 🎯 功能特性

- **🚀 akshare数据集成**：内置akshare数据接口，无需准备数据即可运行
- **模块化设计**：清晰的代码架构，易于维护和扩展
- **双日历支持**：公历和农历（春节对齐）两种季节性分析模式
- **交互式图表**：基于pyecharts的响应式HTML图表
- **批量处理**：支持多指标批量生成图表
- **智能统计**：自动计算同比、环比和累计同比
- **一键演示**：提供快速演示脚本，直接体验所有功能

## 📁 项目结构

```
visualization_toolkit/
├── 📋 __init__.py
├── 🔧 core/
│   ├── __init__.py
│   ├── akshare_client.py     # akshare数据接口
│   ├── data_processor.py     # 数据处理核心
│   ├── calendar_manager.py   # 农历/公历处理
│   └── wind_client.py        # Wind数据获取
├── 📊 charts/
│   ├── __init__.py
│   ├── base_chart.py         # 基础图表类
│   ├── seasonal_chart.py     # 季节性图表(pyecharts版)
│   └── time_series_chart.py  # 时间序列图表
├── 🛠️ utils/
│   ├── __init__.py
│   ├── data_formatter.py     # 数据格式化
│   └── template_manager.py   # 模板管理
├── 📖 examples/
│   ├── __init__.py
│   └── demo.py              # 使用示例
└── 🚀 quick_demo.py         # akshare一键演示
```

## 🚀 快速开始

### 1. 安装依赖

```bash
# 基础安装
pip install visualization-toolkit

# 完整安装（含akshare数据接口）
pip install visualization-toolkit[akshare]

# 开发安装
pip install -e .
```

### 2. 零数据门槛体验

#### 一键akshare演示（推荐）
```bash
# 无需准备数据，直接体验
python quick_demo.py

# 生成的文件：
# - akshare_seasonal_demo.html  季节性分析
# - akshare_timeseries_demo.html  时间序列分析
```

#### 编程使用akshare数据

```python
from core.akshare_client import AkShareClient
from charts.seasonal_chart import SeasonalChart

# 获取任意股票数据（无需准备）
df = AkShareClient.get_stock_daily("000001", "20230101", "20231231")

# 立即创建图表
chart = SeasonalChart()
seasonal_line = chart.create_seasonal_line(
    df,
    date_col='date',
    value_col='close',
    title="平安银行股价季节性分析",
    calendar_type='lunar'  # 农历春节对齐
)
seasonal_line.render("seasonal_analysis.html")
```

#### 使用本地数据（传统方式）

```python
from charts.seasonal_chart import SeasonalChart
import pandas as pd

# 读取本地数据
df = pd.read_csv('your_data.csv')

# 创建季节性图表
chart = SeasonalChart()
seasonal_line = chart.create_seasonal_line(
    df,
    date_col='date',
    value_col='price',
    title="铁矿石价格季节性分析",
    calendar_type='lunar'  # 农历春节对齐
)

# 保存为交互式HTML
seasonal_line.render("seasonal_analysis.html")
```

## 📈 核心功能详解

### 季节性折线图

#### 公历模式（按月份）

```python
chart = SeasonalChart()
line = chart.create_seasonal_line(
    df,
    date_col='date',
    value_col='value',
    title="月度库存季节性分析",
    calendar_type='gregorian',
    years=5  # 显示最近5年
)
```

#### 农历模式（春节对齐）

```python
chart = SeasonalChart()
line = chart.create_seasonal_line(
    df,
    date_col='date',
    value_col='inventory',
    title="春节前后库存变化",
    calendar_type='lunar',
    spring_range=(-60, 60)  # 春节前后60天
)
```

### 多指标批量生成

```python
# 同时分析多个指标
chart = SeasonalChart()
grid = chart.create_seasonal_grid(
    df,
    date_col='date',
    value_cols=['产量', '库存', '价格', '需求'],
    title="黑色产业链季节性对比",
    years=4
)
grid.render("multi_indicator_analysis.html")
```

## 📊 图表效果展示

### 1. 单指标季节性图

- 高亮最新年份数据
- 自动计算同比/环比
- 交互式图例和缩放

### 2. 多指标对比图

- 网格布局展示
- 统一配色方案
- 响应式设计

### 3. 春节对齐模式

- 以春节为基准点
- 支持自定义时间范围
- 适用于中国特有的季节性分析

[📥 下载完整示例代码](examples/demo.py)

## 🎨 高级配置

### 自定义样式

```python
chart = SeasonalChart()
line = chart.create_seasonal_line(
    df,
    date_col='date',
    value_col='price',
    title="自定义样式示例",
    width="1200px",
    height="600px",
    colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57']
)
```

### 动态数据更新

```python
# 实时数据更新示例
def update_seasonal_chart(new_data):
    chart = SeasonalChart()
    updated_line = chart.create_seasonal_line(
        new_data,
        date_col='date',
        value_col='price'
    )
    updated_line.render("live_seasonal.html")
```

## 📊 akshare数据支持

### 支持的数据类型

| 数据类型 | 示例代码 | 说明 |
| -------- | -------- | ---- |
| **股票** | `000001`, `600000` | A股股票日线数据 |
| **指数** | `sh000001`, `sz399001` | 主要指数数据 |
| **期货** | `CU0`, `AL0` | 期货主力合约数据 |
| **经济指标** | `CPI`, `PPI` | 宏观经济数据 |

### 快速获取数据

```python
from core.akshare_client import AkShareClient

# 获取股票数据
df = AkShareClient.get_stock_daily("000001", "20230101", "20231231")

# 获取指数数据
df = AkShareClient.get_index_daily("sh000001", "20230101", "20231231")

# 获取演示数据（最近365天）
df = AkShareClient.get_demo_data("stock", 365)

# 查看可用股票代码
symbols = AkShareClient.list_available_symbols("stock")
```

### 一键演示

```bash
# 运行完整的akshare数据演示
python quick_demo.py

# 查看可用数据源
python quick_demo.py list
```

## 📖 API参考

### AkShareClient类

#### 主要方法

| 方法 | 参数 | 说明 |
| ---- | ---- | ---- |
| `get_stock_daily` | symbol, start_date, end_date | 获取股票日线数据 |
| `get_index_daily` | symbol, start_date, end_date | 获取指数日线数据 |
| `get_demo_data` | data_type, days | 获取演示数据 |
| `list_available_symbols` | data_type | 列出可用代码 |

#### 数据格式

所有方法返回的DataFrame格式统一：
- **股票/指数/期货**: `date`, `open`, `high`, `low`, `close`, `volume`
- **经济指标**: `date`, `value`

### SeasonalChart类

#### 主要方法

| 方法                     | 参数                           | 说明             |
| ------------------------ | ------------------------------ | ---------------- |
| `create_seasonal_line` | df, date_col, value_col, title | 创建季节性折线图 |
| `create_seasonal_grid` | df, date_cols, value_cols      | 创建多指标网格图 |

#### 关键参数

| 参数              | 类型  | 默认值      | 说明                           |
| ----------------- | ----- | ----------- | ------------------------------ |
| `calendar_type` | str   | 'gregorian' | 日历类型 ('gregorian'/'lunar') |
| `spring_range`  | tuple | (-70, 70)   | 农历分析时间范围               |
| `years`         | int   | 5           | 显示年份数量                   |
| `width`         | str   | "100%"      | 图表宽度                       |
| `height`        | str   | "500px"     | 图表高度                       |

## 🔧 数据处理工具

### 数据预处理器

```python
from visualization_toolkit.core.data_processor import DataProcessor

processor = DataProcessor()

# 计算统计指标
stats = processor.calculate_yoy_ytd(df, 'price', 'date')
print(f"最新值: {stats['latest_value']}")
print(f"同比: {stats['yoy']:.2f}%")
print(f"累计同比: {stats['ytd']:.2f}%")

# 准备透视表
pivot = processor.pivot_for_seasonal(df, 'date', 'value')
```

## 📱 部署和使用

### 1. 生成交互式网页

```python
# 创建完整的分析报告
page = Page()
chart = SeasonalChart()

for metric in ['库存', '产量', '价格']:
    line = chart.create_seasonal_line(
        df,
        date_col='date',
        value_col=metric,
        title=f"{metric}季节性分析"
    )
    page.add(line)

page.render("analysis_report.html")
```

### 2. 集成到Web应用

```python
from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/seasonal/<metric>')
def seasonal_analysis(metric):
    chart = SeasonalChart()
    line = chart.create_seasonal_line(
        df,
        date_col='date',
        value_col=metric
    )
    return line.dump_options_with_quotes()
```

## 🎯 最佳实践

### 1. 数据准备建议

- 确保日期列格式为datetime
- 处理缺失值和异常值
- 按时间升序排列数据

### 2. 图表优化

- 根据数据特点选择日历类型
- 合理设置显示年份数量
- 使用有意义的标题和副标题

### 3. 性能优化

- 大数据集使用采样处理
- 缓存生成的图表
- 使用CDN加速资源加载

## 🆘 常见问题

### Q: 如何处理缺失数据？

A: 系统会自动进行线性插值处理，但建议先进行数据清洗。

### Q: 支持哪些日期格式？

A: 支持所有pandas可识别的日期格式，推荐使用ISO格式(YYYY-MM-DD)。

### Q: 如何自定义颜色？

A: 通过colors参数传入颜色列表，或使用默认配色方案。

## 📖 总结

本工具包提供了**零数据门槛**的季节性分析解决方案，通过集成akshare数据接口，用户无需准备任何数据即可体验完整的可视化分析功能。

### 🚀 核心优势
- **零数据门槛**：内置akshare接口，无需准备数据
- **一键体验**：`python quick_demo.py` 直接运行
- **真实数据**：使用A股、指数等真实金融数据
- **即装即用**：pip安装后立即使用

### 📊 适用场景
- 📈 **金融市场分析**：股票、期货、商品价格季节性研究
- 📊 **企业数据分析**：销售、库存、生产数据季节性分析
- 📉 **宏观经济研究**：GDP、CPI、PPI等经济指标分析

### 🎯 快速开始
```bash
# 安装
pip install visualization-toolkit

# 立即体验（无需数据准备）
python quick_demo.py

# 查看可用数据源
python quick_demo.py list
```

### 💡 开发友好
- **模块化设计**：易于扩展和定制
- **完整文档**：详细API和使用示例
- **社区支持**：欢迎贡献代码和想法

---

**立即体验**：`pip install visualization-toolkit && python quick_demo.py`

<div align="center">


</div>

<script>
// 添加下载功能
function downloadFile(filename, content) {
    const element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(content));
    element.setAttribute('download', filename);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}


