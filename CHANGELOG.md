# 变更日志

所有显著的变更都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/),
并且本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [未发布]

### 新增
- 添加农历日历支持
- 集成Wind数据接口
- 模板管理系统
- 交互式图表功能

### 改进
- 优化数据处理性能
- 改进错误处理机制
- 增强文档和示例

### 修复
- 修复季节性分析中的边界条件问题
- 修复时间序列图表的缩放问题

## [1.2.0] - 2024-12-XX

### 新增
- 添加UV环境支持
- 添加GitHub Actions CI/CD
- 添加Docker部署支持
- 添加完整测试套件

### 改进
- 重构项目结构
- 优化包管理配置
- 更新依赖版本

### 修复
- 修复Windows路径问题
- 修复中文编码问题

## [1.1.0] - 2024-11-XX

### 新增
- 添加时间序列图表模块
- 添加K线图支持
- 添加成交量图表
- 添加数据格式化工具

### 改进
- 增强季节性分析算法
- 优化图表渲染性能
- 改进用户界面

### 修复
- 修复数据缺失值处理
- 修复图表标签重叠问题

## [1.0.0] - 2024-10-XX

### 新增
- 初始版本发布
- 季节性图表功能
- 公历/农历日历支持
- 基础图表模板
- 数据处理器
- 示例代码和文档

### 功能
- 创建季节性折线图
- 创建季节性网格图
- 支持多种日历类型
- 自定义图表样式
- 导出HTML格式

### 技术栈
- Python 3.8+
- pyecharts 2.0+
- pandas 1.3+
- numpy 1.20+

---

## 版本对比

| 版本 | Python支持 | 主要功能 | 备注 |
|------|------------|----------|------|
| 1.0.0 | 3.8+ | 基础季节性图表 | 初始版本 |
| 1.1.0 | 3.8+ | 时间序列图表 | 功能扩展 |
| 1.2.0 | 3.8-3.11 | UV支持、CI/CD | 现代化改进 |

## 升级指南

### 从1.1.x升级到1.2.x

1. 更新依赖：
   ```bash
   pip install --upgrade visualkit
   ```

2. 检查兼容性：
   - 所有1.1.x的API保持向后兼容
   - 新增功能需要Python 3.8+

3. 新功能使用：
   ```python
   # 新功能示例
   from visualkit import TemplateManager
   
   manager = TemplateManager()
   template = manager.get_template('seasonal')
   ```

## 路线图

### 即将发布 (v1.3.0)
- [ ] 实时数据支持
- [ ] Web界面
- [ ] 更多图表类型
- [ ] 性能优化

### 未来规划 (v2.0.0)
- [ ] 异步数据处理
- [ ] 机器学习集成
- [ ] 移动端支持
- [ ] 插件系统

---

## 历史版本下载

- [v1.2.0](https://github.com/your-franklooo/visualkit/releases/tag/v1.2.0)
- [v1.1.0](https://github.com/your-franklooo/visualkit/releases/tag/v1.1.0)
- [v1.0.0](https://github.com/your-franklooo/visualkit/releases/tag/v1.0.0)

## 兼容性说明

| 版本 | 兼容性 | 支持状态 |
|------|--------|----------|
| 1.2.x | Python 3.8-3.11 | ✅ 支持 |
| 1.1.x | Python 3.8-3.10 | ⚠️ 维护 |
| 1.0.x | Python 3.8-3.9 | ❌ 停止维护 |