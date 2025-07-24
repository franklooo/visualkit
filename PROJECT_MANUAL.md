# 数据可视化工具包 - 完整项目手册

## 📋 项目生命周期指南

本手册涵盖从开发到发布的完整流程：
- ✅ 项目编程调试
- ✅ GitHub项目发布
- ✅ PyPI包发布
- ✅ 持续集成/部署

---

## 🛠️ 开发环境调试指南

### 1. 环境验证脚本

创建 `scripts/validate_env.py`：
```python
#!/usr/bin/env python3
"""环境验证脚本"""

import sys
import importlib
import platform
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    print(f"✅ Python版本: {version.major}.{version.minor}.{version.micro}")
    if version < (3, 8):
        print("❌ 需要Python 3.8+")
        return False
    return True

def check_dependencies():
    """检查关键依赖"""
    packages = [
        'pandas', 'numpy', 'pyecharts', 'python-dateutil', 'chinese_calendar'
    ]
    
    for package in packages:
        try:
            mod = importlib.import_module(package)
            print(f"✅ {package}: {mod.__version__}")
        except ImportError as e:
            print(f"❌ 缺少依赖: {package} - {e}")
            return False
    return True

def check_project_structure():
    """检查项目结构"""
    required_files = [
        'visualization_toolkit/__init__.py',
        'visualization_toolkit/charts/__init__.py',
        'visualization_toolkit/core/__init__.py',
        'visualization_toolkit/utils/__init__.py',
    ]
    
    for file in required_files:
        if not Path(file).exists():
            print(f"❌ 缺少文件: {file}")
            return False
    print("✅ 项目结构完整")
    return True

if __name__ == "__main__":
    print("=== 环境验证 ===")
    checks = [
        check_python_version(),
        check_dependencies(),
        check_project_structure()
    ]
    
    if all(checks):
        print("🎉 环境验证通过！")
    else:
        print("⚠️  请修复上述问题")
        sys.exit(1)
```

### 2. 调试配置

#### VS Code调试配置
创建 `.vscode/launch.json`：
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Demo",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/example/demo.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}",
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        },
        {
            "name": "Python: 测试",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": ["tests/", "-v"],
            "console": "integratedTerminal"
        }
    ]
}
```

#### VS Code设置
创建 `.vscode/settings.json`：
```json
{
    "python.defaultInterpreterPath": ".venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.mypyEnabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "python.testing.pytestPath": "pytest",
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        ".pytest_cache": true,
        ".mypy_cache": true
    }
}
```

### 3. 调试技巧

#### 日志调试
```python
# 在代码中添加调试日志
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)

# 使用示例
logger = logging.getLogger(__name__)
logger.debug("数据形状: %s", df.shape)
```

#### 交互式调试
```python
# 使用IPython嵌入调试
from IPython import embed

def create_chart(data):
    # 在关键位置插入调试
    embed()
    return process_data(data)
```

---

## 🚀 GitHub项目发布指南

### 1. 项目初始化

```bash
# 初始化git仓库
git init
git add .
git commit -m "Initial commit: Data Visualization Toolkit"

# 创建GitHub仓库
git remote add origin https://github.com/your-username/visualization-toolkit.git
git push -u origin main
```

### 2. 项目结构标准化

```
visualization-toolkit/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml
│   │   └── release.yml
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md
│       └── feature_request.md
├── docs/
│   ├── api/
│   ├── tutorials/
│   └── _static/
├── tests/
│   ├── __init__.py
│   ├── test_charts/
│   ├── test_core/
│   └── conftest.py
├── scripts/
│   ├── validate_env.py
│   └── build_docs.py
├── visualization_toolkit/
├── example/
├── requirements/
├── .gitignore
├── LICENSE
├── README.md
├── CONTRIBUTING.md
└── CHANGELOG.md
```

### 3. GitHub Actions配置

#### CI/CD工作流
创建 `.github/workflows/ci.yml`：
```yaml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: [3.8, 3.9, "3.10", "3.11"]

    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install UV
      run: |
        curl -LsSf https://astral.sh/uv/install.sh | sh
        echo "$HOME/.cargo/bin" >> $GITHUB_PATH
    
    - name: Install dependencies
      run: |
        uv pip install -e .[dev]
    
    - name: Lint with flake8
      run: |
        flake8 visualization_toolkit tests
    
    - name: Type check with mypy
      run: |
        mypy visualization_toolkit
    
    - name: Test with pytest
      run: |
        pytest tests/ -v --cov=visualization_toolkit --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

#### 发布工作流
创建 `.github/workflows/release.yml`：
```yaml
name: Release

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install UV
      run: |
        curl -LsSf https://astral.sh/uv/install.sh | sh
        echo "$HOME/.cargo/bin" >> $GITHUB_PATH
    
    - name: Install dependencies
      run: |
        uv pip install -e .[dev]
    
    - name: Build package
      run: |
        python -m build
    
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: |
        twine upload dist/*
```

### 4. 文档模板

#### README.md模板
```markdown
# 数据可视化工具包

[![CI](https://github.com/your-username/visualization-toolkit/workflows/CI/badge.svg)](https://github.com/your-username/visualization-toolkit/actions)
[![codecov](https://codecov.io/gh/your-username/visualization-toolkit/branch/main/graph/badge.svg)](https://codecov.io/gh/your-username/visualization-toolkit)
[![PyPI version](https://badge.fury.io/py/visualization-toolkit.svg)](https://badge.fury.io/py/visualization-toolkit)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

基于pyecharts的高级数据可视化工具包...

## 快速开始

```bash
pip install visualization-toolkit
```

## 特性
- 季节性分析图表
- 时间序列可视化
- Wind数据集成
- 模板系统

## 示例

```python
from visualization_toolkit import SeasonalChart

# 创建季节性图表
chart = SeasonalChart()
chart.create_seasonal_line(data, 'price', '公历')
```

## 文档
- [完整文档](https://visualization-toolkit.readthedocs.io)
- [API参考](https://visualization-toolkit.readthedocs.io/en/latest/api.html)

## 贡献
参见 [CONTRIBUTING.md](CONTRIBUTING.md)
```

---

## 📦 PyPI包发布指南

### 1. 包配置检查

#### 验证setup.py/pyproject.toml
```bash
# 检查包配置
python -m build

# 检查包内容
twine check dist/*
```

#### 测试安装
```bash
# 在虚拟环境中测试
python -m venv test_env
source test_env/bin/activate
pip install dist/*.whl

# 验证导入
python -c "import visualization_toolkit; print('OK')"
```

### 2. 版本管理

#### 版本号规范
使用语义化版本号：MAJOR.MINOR.PATCH

```python
# 在 __init__.py 中
__version__ = "1.2.0"

# 使用bump2version管理
bump2version patch  # 1.2.0 -> 1.2.1
bump2version minor  # 1.2.0 -> 1.3.0
bump2version major  # 1.2.0 -> 2.0.0
```

#### 创建版本标签
```bash
git tag -a v1.2.0 -m "Release version 1.2.0"
git push origin v1.2.0
```

### 3. 发布流程

#### 手动发布
```bash
# 1. 清理旧构建
rm -rf dist/ build/ *.egg-info/

# 2. 构建包
python -m build

# 3. 上传到测试PyPI
twine upload --repository testpypi dist/*

# 4. 测试安装
pip install -i https://test.pypi.org/simple/ visualization-toolkit

# 5. 上传到正式PyPI
twine upload dist/*
```

#### 自动发布
GitHub Actions会自动在创建Release时发布到PyPI。

### 4. PyPI配置

#### 创建API Token
1. 访问 https://pypi.org/manage/account/
2. 创建API Token
3. 在GitHub仓库设置中添加 `PYPI_API_TOKEN` 密钥

#### 配置twine
创建 `~/.pypirc`：
```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 📖 项目使用手册

### 1. 安装指南

#### 从PyPI安装
```bash
# 基础安装
pip install visualization-toolkit

# 完整安装（含Wind支持）
pip install visualization-toolkit[wind]

# 开发环境
pip install visualization-toolkit[dev]
```

#### 从源码安装
```bash
git clone https://github.com/your-username/visualization-toolkit.git
cd visualization-toolkit
pip install -e .
```

### 2. 快速入门

#### 基础使用
```python
import pandas as pd
from visualization_toolkit import SeasonalChart, TimeSeriesChart

# 创建示例数据
dates = pd.date_range('2021-01-01', '2023-12-31', freq='D')
data = pd.DataFrame({
    'date': dates,
    'price': np.random.randn(len(dates)).cumsum() + 100,
    'volume': np.random.randint(1000, 10000, len(dates))
})

# 季节性分析
seasonal = SeasonalChart()
chart1 = seasonal.create_seasonal_line(
    data, 'price', '公历',
    title='价格季节性分析'
)
chart1.render('seasonal.html')

# 时间序列分析
ts = TimeSeriesChart()
chart2 = ts.create_time_series_line(
    data, 'price',
    title='价格趋势',
    smooth=True
)
chart2.render('timeseries.html')
```

#### 高级功能
```python
from visualization_toolkit import DataProcessor, TemplateManager

# 数据处理
df = DataProcessor.create_sample_data(
    start_date='2020-01-01',
    end_date='2023-12-31',
    columns=['open', 'high', 'low', 'close', 'volume']
)

# 使用模板
manager = TemplateManager()
template = manager.get_template('seasonal')
chart = template.create_chart(df, 'close')
```

### 3. API参考

#### SeasonalChart类
```python
class SeasonalChart(BaseChart):
    def create_seasonal_line(self, data, column, calendar_type='公历', **kwargs)
    def create_seasonal_grid(self, data, columns, calendar_type='公历', **kwargs)
```

#### TimeSeriesChart类
```python
class TimeSeriesChart(BaseChart):
    def create_time_series_line(self, data, column, **kwargs)
    def create_candlestick_chart(self, data, **kwargs)
    def create_volume_chart(self, data, column, **kwargs)
```

### 4. 配置选项

#### 全局配置
```python
from visualization_toolkit import DEFAULT_CONFIG

# 修改默认配置
DEFAULT_CONFIG.update({
    'theme': 'chalk',
    'width': 1200,
    'height': 600,
    'colors': ['#c23531', '#2f4554', '#61a0a8']
})
```

#### 环境变量
```bash
# 设置环境变量
export VIZ_TOOLKIT_THEME=dark
export VIZ_TOOLKIT_WIDTH=1400
export VIZ_TOOLKIT_HEIGHT=800
```

---

## 🔧 故障排除

### 常见问题

#### 1. 安装问题
```bash
# 权限问题
pip install --user visualization-toolkit

# 网络问题
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple visualization-toolkit
```

#### 2. 运行问题
```python
# 内存不足
import gc
gc.collect()

# 图表不显示
chart.render_notebook()  # Jupyter环境
```

#### 3. 数据问题
```python
# 缺失值处理
df = DataProcessor.handle_missing_values(df, method='fill')

# 数据类型转换
df = DataProcessor.format_numeric_columns(df)
```

### 支持渠道

- **GitHub Issues**: https://github.com/your-username/visualization-toolkit/issues
- **文档**: https://visualization-toolkit.readthedocs.io
- **邮件**: support@your-domain.com
- **微信群**: 扫描二维码加入

---

## 📊 项目状态监控

### 徽章
```markdown
[![CI](https://github.com/your-username/visualization-toolkit/workflows/CI/badge.svg)](https://github.com/your-username/visualization-toolkit/actions)
[![codecov](https://codecov.io/gh/your-username/visualization-toolkit/branch/main/graph/badge.svg)](https://codecov.io/gh/your-username/visualization-toolkit)
[![PyPI version](https://badge.fury.io/py/visualization-toolkit.svg)](https://badge.fury.io/py/visualization-toolkit)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
```

### 发布检查清单

- [ ] 所有测试通过
- [ ] 代码覆盖率 > 80%
- [ ] 文档完整
- [ ] 版本号更新
- [ ] CHANGELOG.md更新
- [ ] README.md更新
- [ ] PyPI测试环境验证
- [ ] GitHub Release创建
- [ ] 社区公告发布

---

*最后更新: 2024年12月*
*版本: v1.2.0*