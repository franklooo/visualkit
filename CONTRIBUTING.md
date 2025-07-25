# 贡献指南

感谢您对数据可视化工具包的贡献！本指南将帮助您了解如何参与项目开发。

## 🚀 快速开始

### 开发环境设置

1. **克隆项目**
   ```bash
   git clone https://github.com/franklooo/visualkit.git
   cd visualkit
   ```

2. **创建虚拟环境**
   ```bash
   # 使用UV
   uv venv
   source .venv/bin/activate  # Linux/macOS
   # 或
   .venv\Scripts\activate     # Windows
   
   # 安装依赖
   uv pip install -e .[dev]
   ```

3. **验证安装**
   ```bash
   python scripts/validate_env.py
   ```

### 开发流程

1. **创建功能分支**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **编写代码**
   - 遵循PEP 8规范
   - 添加类型注解
   - 编写单元测试

3. **运行测试**
   ```bash
   pytest tests/ -v
   ```

4. **提交更改**
   ```bash
   git add .
   git commit -m "feat: 添加新功能描述"
   ```

5. **推送并创建PR**
   ```bash
   git push origin feature/your-feature-name
   ```

## 📋 代码规范

### Python代码风格

- **格式**: 使用Black格式化代码
  ```bash
  black visualkit tests
  ```

- **检查**: 使用flake8检查代码质量
  ```bash
  flake8 visualkit tests
  ```

- **类型**: 使用mypy进行类型检查
  ```bash
  mypy visualkit --ignore-missing-imports
  ```

### 提交消息规范

使用[Conventional Commits](https://www.conventionalcommits.org/)规范：

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**类型说明**:
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建/工具

**示例**:
```
feat: 添加农历日历支持

- 支持农历节气计算
- 添加农历节假日标记
- 更新文档说明

Closes #123
```

## 🧪 测试指南

### 测试结构

```
tests/
├── __init__.py
├── test_charts/
│   ├── test_seasonal_chart.py
│   └── test_time_series_chart.py
├── test_core/
│   ├── test_data_processor.py
│   └── test_calendar_manager.py
├── test_utils/
│   ├── test_data_formatter.py
│   └── test_template_manager.py
└── conftest.py
```

### 编写测试

#### 单元测试示例

```python
import pytest
import pandas as pd
from visualkit import SeasonalChart

class TestSeasonalChart:
    
    @pytest.fixture
    def sample_data(self):
        """测试数据fixture"""
        return pd.DataFrame({
            'date': pd.date_range('2021-01-01', periods=100),
            'value': range(100)
        })
    
    def test_create_seasonal_line(self, sample_data):
        """测试季节性折线图创建"""
        chart = SeasonalChart()
        result = chart.create_seasonal_line(sample_data, 'value')
        assert result is not None
```

#### 测试数据

使用`conftest.py`中的fixture提供测试数据：

```python
@pytest.fixture
def sample_dataframe():
    """标准测试数据"""
    dates = pd.date_range('2021-01-01', '2021-12-31', freq='D')
    return pd.DataFrame({
        'date': dates,
        'price': np.random.randn(len(dates)).cumsum() + 100
    })
```

### 运行测试

```bash
# 运行所有测试
pytest tests/

# 运行特定测试
pytest tests/test_charts/test_seasonal_chart.py::TestSeasonalChart::test_create_seasonal_line

# 带覆盖率测试
pytest tests/ --cov=visualkit --cov-report=html

# 并行测试
pytest tests/ -n auto
```

## 📚 文档编写

### API文档

使用Sphinx生成文档：

```bash
# 安装文档依赖
pip install -e .[docs]

# 构建文档
cd docs
make html
```

### 文档结构

```
docs/
├── api/
│   ├── charts.rst
│   ├── core.rst
│   └── utils.rst
├── tutorials/
│   ├── quickstart.rst
│   ├── seasonal_analysis.rst
│   └── time_series.rst
├── _static/
└── conf.py
```

### 代码文档

使用Google风格docstring：

```python
def create_seasonal_line(self, data, column, calendar_type='公历', **kwargs):
    """创建季节性折线图。
    
    Args:
        data: 输入数据DataFrame
        column: 要分析的列名
        calendar_type: 日历类型 ('公历' 或 '农历')
        **kwargs: 其他图表参数
        
    Returns:
        pyecharts.charts.Line: 季节性折线图实例
        
    Raises:
        ValueError: 当calendar_type不是'公历'或'农历'时
        KeyError: 当column不存在于data中时
    """
```

## 🔧 开发工具

### 预提交钩子

安装pre-commit：

```bash
pip install pre-commit
pre-commit install
```

### 代码格式化

```bash
# 格式化所有代码
black visualkit tests

# 检查格式
black --check visualkit tests
```

### 类型检查

```bash
# 运行类型检查
mypy visualkit --ignore-missing-imports
```

## 🐛 报告问题

### Bug报告模板

使用GitHub issue模板：

```markdown
**描述**
清晰描述遇到的问题

**重现步骤**
1. 步骤1
2. 步骤2
3. 步骤3

**期望行为**
描述期望的结果

**环境**
- Python版本: 
- 操作系统: 
- 包版本: 

**错误信息**
```
粘贴错误信息
```
```

## 🎯 贡献类型

### 新功能开发

1. **讨论**: 在issue中讨论新功能
2. **设计**: 提供设计文档
3. **实现**: 编写代码和测试
4. **文档**: 更新相关文档

### Bug修复

1. **复现**: 创建最小复现案例
2. **修复**: 提交修复代码
3. **测试**: 添加回归测试
4. **验证**: 确保问题已解决

### 文档改进

- 修复错别字
- 添加示例代码
- 更新API文档
- 改进教程

## 📋 Pull Request模板

### PR模板

```markdown
## 变更类型
- [ ] Bug修复
- [ ] 新功能
- [ ] 文档更新
- [ ] 代码重构
- [ ] 性能优化

## 变更描述
详细描述所做的更改

## 测试
- [ ] 添加了测试
- [ ] 所有测试通过
- [ ] 手动测试完成

## 文档
- [ ] 更新了文档
- [ ] 添加了示例
```

## 🔄 发布流程

### 发布检查清单

- [ ] 所有测试通过
- [ ] 代码覆盖率>80%
- [ ] 文档更新
- [ ] CHANGELOG.md更新
- [ ] 版本号更新
- [ ] GitHub Release创建

### 发布脚本

使用提供的发布脚本：

```bash
python scripts/publish.py --version 1.2.0 --test
python scripts/publish.py --version 1.2.0 --pypi
```

## 📞 联系信息

- **Issue**: [GitHub Issues](https://github.com/franklooo/visualkit/issues)
- **讨论**: [GitHub Discussions](https://github.com/franklooo/visualkit/discussions)
- **邮件**: your.email@example.com

## 📄 许可证

本项目采用MIT许可证，详见 [LICENSE](LICENSE) 文件。

---

感谢你的贡献！🎉