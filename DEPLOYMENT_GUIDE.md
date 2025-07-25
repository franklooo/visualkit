# 数据可视化工具包 - UV环境部署指南

## 技术栈
- **Python**: 3.8+
- **包管理**: UV (高性能Python包管理工具)
- **可视化**: pyecharts
- **数据处理**: pandas, numpy
- **时间处理**: python-dateutil, chinese-calendar

## 系统要求
- Windows 10/11 或 Linux/macOS
- Python 3.8-3.13 (推荐3.12+)
- 8GB+ RAM (处理大数据集时建议16GB+)
- 500MB+ 磁盘空间

## 安装步骤

### 1. 安装UV

#### Windows (PowerShell)
```powershell
# 使用官方安装脚本
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 验证安装
uv --version
```

#### Linux/macOS
```bash
# 使用官方安装脚本
curl -LsSf https://astral.sh/uv/install.sh | sh

# 或者使用Homebrew (macOS)
brew install uv

# 验证安装
uv --version
```

### 2. 克隆项目
```bash
git clone <your-repo-url>
cd visualkit
```

### 3. 创建项目环境

#### 初始化UV项目
```bash
# 如果项目已有pyproject.toml
uv sync

# 或者创建新的虚拟环境
uv venv
source .venv/bin/activate  # Linux/macOS
# 或
.venv\Scripts\activate     # Windows
```

#### 安装依赖
```bash
# 从requirements.txt安装
uv pip install -r requirements.txt

# 或者使用pyproject.toml
uv add pandas numpy pyecharts python-dateutil chinese-calendar

# 可选：WindPy数据接口
uv add WindPy

# 开发依赖
uv add --dev pytest black flake8 mypy
```

### 4. 验证安装
```bash
# 检查Python版本
python --version

# 检查关键包
python -c "import pandas; print('pandas:', pandas.__version__)"
python -c "import pyecharts; print('pyecharts:', pyecharts.__version__)"
```

## 快速开始

### 1. 基础使用
```bash
# 激活环境
source .venv/bin/activate  # Linux/macOS
# 或
.venv\Scripts\activate     # Windows

# 运行演示
python example/demo.py
```

### 2. 使用示例

#### 创建季节性分析图表
```python
from visualkit import SeasonalChart, DataProcessor

# 准备数据
df = DataProcessor.create_sample_data(
    start_date='2021-01-01',
    end_date='2023-12-31',
    columns=['price', 'volume']
)

# 创建图表
chart = SeasonalChart()
seasonal_chart = chart.create_seasonal_line(
    df, 'price', '公历',
    title='价格季节性分析'
)
seasonal_chart.render('seasonal_analysis.html')
```

#### 时间序列分析
```python
from visualkit import TimeSeriesChart

# 创建时间序列图表
ts_chart = TimeSeriesChart()
line_chart = ts_chart.create_time_series_line(
    df, 'price',
    title='价格趋势图',
    smooth=True,
    mark_point=True
)
line_chart.render('time_series.html')
```

## 高级配置

### 1. 环境变量配置
创建 `.env` 文件：
```bash
# Wind数据配置 (可选)
WIND_ACCOUNT=your_account
WIND_PASSWORD=your_password

# 图表配置
DEFAULT_THEME=chalk
CHART_WIDTH=1200
CHART_HEIGHT=600

# 数据路径
DATA_PATH=./data
OUTPUT_PATH=./output
```

### 2. 性能优化
```bash
# 安装高性能依赖
uv add numba scipy

# 启用JIT编译
export NUMBA_CACHE_DIR=./.numba_cache
```

### 3. 缓存配置
```python
# 在代码中启用缓存
from visualkit import set_cache_dir
set_cache_dir('./.cache')
```

## 部署选项

### 1. 本地开发部署
```bash
# 启动开发服务器
uv run python -m http.server 8000

# 访问生成的HTML文件
# http://localhost:8000/output/
```

### 2. Docker部署
创建 `Dockerfile`：
```dockerfile
FROM python:3.10-slim

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 安装UV
RUN pip install uv

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY . .

# 安装依赖
RUN uv pip install -r requirements.txt

# 暴露端口
EXPOSE 8000

# 运行应用
CMD ["python", "example/demo.py"]
```

构建和运行：
```bash
docker build -t visualkit .
docker run -p 8000:8000 visualkit
```

### 3. 云端部署

#### AWS EC2
```bash
# 连接到EC2实例
ssh -i your-key.pem ec2-user@your-instance-ip

# 安装UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# 克隆和运行项目
git clone your-repo
cd visualkit
uv pip install -r requirements.txt
nohup python example/demo.py &
```

#### 阿里云ECS
```bash
# 使用阿里云镜像加速
export UV_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/
uv pip install -r requirements.txt
```

## 故障排除

### 常见问题

#### 1. UV安装失败
```bash
# 检查网络连接
ping astral.sh

# 使用代理
export HTTPS_PROXY=http://your-proxy:port
uv pip install -r requirements.txt
```

#### 2. 包冲突
```bash
# 清理缓存
uv cache clean

# 重新创建环境
uv venv --clear
uv pip install -r requirements.txt
```

#### 3. 内存不足
```bash
# 减少数据量
export CHUNK_SIZE=10000

# 使用内存映射
export USE_MEMORY_MAP=true
```

#### 4. 中文乱码
```bash
# 设置环境变量
export LANG=zh_CN.UTF-8
export LC_ALL=zh_CN.UTF-8
```

## 监控和维护

### 1. 日志配置
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### 2. 性能监控
```bash
# 使用UV的统计功能
uv pip list --outdated

# 内存使用监控
python -c "
import psutil
print(f'Memory usage: {psutil.virtual_memory().percent}%')
"
```

### 3. 自动更新
```bash
# 创建更新脚本
#!/bin/bash
uv lock --upgrade
uv sync
git add uv.lock
git commit -m "Update dependencies"
```

## 扩展开发

### 1. 添加新图表类型
```python
from visualkit import BaseChart

class CustomChart(BaseChart):
    def create_custom_chart(self, data, **kwargs):
        # 实现自定义图表逻辑
        pass
```

### 2. 数据源扩展
```python
from visualkit.core import BaseDataSource

class CustomDataSource(BaseDataSource):
    def fetch_data(self, **params):
        # 实现自定义数据源
        pass
```

## 支持

- **文档**: [项目Wiki](https://github.com/your-repo/wiki)
- **问题报告**: [GitHub Issues](https://github.com/your-repo/issues)
- **邮件**: support@your-domain.com
- **微信群**: 扫描二维码加入技术支持群

## 版本历史

- v1.0.0: 初始版本，支持基础图表功能
- v1.1.0: 添加UV支持，优化性能
- v1.2.0: 增加Docker部署支持

---

*最后更新: 2024年12月*