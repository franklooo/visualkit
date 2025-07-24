"""
模板管理器
管理图表模板和配置
"""
import json
import os
from typing import Dict, Any, List, Optional
from pathlib import Path


class TemplateManager:
    """模板管理器"""
    
    def __init__(self, template_dir: str = None):
        if template_dir is None:
            # 使用当前文件所在目录的templates子目录
            current_dir = Path(__file__).parent
            template_dir = current_dir / 'templates'
        
        self.template_dir = Path(template_dir)
        self.template_dir.mkdir(exist_ok=True)
        
        # 内置模板
        self.builtin_templates = {
            'seasonal_chart': self._get_seasonal_template(),
            'time_series_chart': self._get_time_series_template(),
            'grid_layout': self._get_grid_template(),
            'dashboard': self._get_dashboard_template()
        }
    
    def save_template(self, name: str, template: Dict[str, Any]) -> bool:
        """保存模板到文件"""
        try:
            template_file = self.template_dir / f"{name}.json"
            with open(template_file, 'w', encoding='utf-8') as f:
                json.dump(template, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存模板失败: {e}")
            return False
    
    def load_template(self, name: str) -> Optional[Dict[str, Any]]:
        """从文件加载模板"""
        try:
            template_file = self.template_dir / f"{name}.json"
            if template_file.exists():
                with open(template_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # 返回内置模板
                return self.builtin_templates.get(name)
        except Exception as e:
            print(f"加载模板失败: {e}")
            return None
    
    def list_templates(self) -> List[str]:
        """列出所有可用模板"""
        templates = list(self.builtin_templates.keys())
        
        # 添加用户自定义模板
        if self.template_dir.exists():
            for file in self.template_dir.glob("*.json"):
                name = file.stem
                if name not in templates:
                    templates.append(name)
        
        return templates
    
    def get_template_config(self, template_name: str) -> Dict[str, Any]:
        """获取模板配置"""
        template = self.load_template(template_name)
        if template is None:
            template = self.builtin_templates.get('seasonal_chart')
        return template
    
    def create_custom_template(
        self,
        base_template: str,
        custom_config: Dict[str, Any],
        new_name: str
    ) -> bool:
        """基于现有模板创建自定义模板"""
        try:
            base_config = self.load_template(base_template)
            if base_config is None:
                return False
            
            # 合并配置
            merged_config = self._deep_merge(base_config, custom_config)
            
            # 保存新模板
            return self.save_template(new_name, merged_config)
        except Exception as e:
            print(f"创建自定义模板失败: {e}")
            return False
    
    def _deep_merge(self, base: Dict, custom: Dict) -> Dict:
        """深度合并字典"""
        result = base.copy()
        
        for key, value in custom.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def _get_seasonal_template(self) -> Dict[str, Any]:
        """季节性图表模板"""
        return {
            "chart_type": "seasonal",
            "colors": [
                '#5470c6', '#91cc75', '#fac858', '#ee6666',
                '#73c0de', '#3ba272', '#fc8452', '#9a60b4'
            ],
            "layout": {
                "width": "100%",
                "height": "500px",
                "theme": "white"
            },
            "options": {
                "title": {
                    "text": "季节性分析",
                    "subtitle": "",
                    "left": "center"
                },
                "tooltip": {
                    "trigger": "axis",
                    "axis_pointer_type": "cross"
                },
                "legend": {
                    "type": "scroll",
                    "orient": "horizontal",
                    "top": "5%",
                    "left": "center"
                },
                "grid": {
                    "left": "3%",
                    "right": "4%",
                    "bottom": "3%",
                    "containLabel": True
                },
                "xAxis": {
                    "type": "category",
                    "boundary_gap": False
                },
                "yAxis": {
                    "type": "value"
                },
                "dataZoom": [
                    {
                        "type": "inside",
                        "start": 0,
                        "end": 100
                    },
                    {
                        "type": "slider",
                        "start": 0,
                        "end": 100
                    }
                ]
            }
        }
    
    def _get_time_series_template(self) -> Dict[str, Any]:
        """时间序列图表模板"""
        return {
            "chart_type": "time_series",
            "colors": [
                '#5470c6', '#91cc75', '#fac858', '#ee6666',
                '#73c0de', '#3ba272', '#fc8452', '#9a60b4'
            ],
            "layout": {
                "width": "100%",
                "height": "500px",
                "theme": "white"
            },
            "options": {
                "title": {
                    "text": "时间序列分析",
                    "subtitle": "",
                    "left": "center"
                },
                "tooltip": {
                    "trigger": "axis",
                    "axis_pointer_type": "cross"
                },
                "legend": {
                    "type": "scroll",
                    "orient": "horizontal",
                    "top": "5%",
                    "left": "center"
                },
                "grid": {
                    "left": "3%",
                    "right": "4%",
                    "bottom": "3%",
                    "containLabel": True
                },
                "xAxis": {
                    "type": "category",
                    "boundary_gap": False,
                    "axisLabel": {
                        "rotate": 45
                    }
                },
                "yAxis": {
                    "type": "value"
                },
                "dataZoom": [
                    {
                        "type": "inside",
                        "start": 0,
                        "end": 100
                    },
                    {
                        "type": "slider",
                        "start": 0,
                        "end": 100
                    }
                ]
            }
        }
    
    def _get_grid_template(self) -> Dict[str, Any]:
        """网格布局模板"""
        return {
            "chart_type": "grid",
            "layout": {
                "width": "100%",
                "height": "auto",
                "theme": "white"
            },
            "options": {
                "grid_spacing": 50,
                "chart_height": 350,
                "responsive": True
            }
        }
    
    def _get_dashboard_template(self) -> Dict[str, Any]:
        """仪表板模板"""
        return {
            "chart_type": "dashboard",
            "layout": {
                "width": "100%",
                "height": "100%",
                "theme": "white"
            },
            "options": {
                "title": {
                    "text": "数据仪表板",
                    "left": "center"
                },
                "grid": [
                    {
                        "top": 60,
                        "bottom": 60,
                        "left": 60,
                        "right": 60
                    }
                ],
                "responsive": True
            }
        }
    
    def export_template(self, template_name: str, export_path: str) -> bool:
        """导出模板到指定路径"""
        try:
            template = self.load_template(template_name)
            if template is None:
                return False
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(template, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"导出模板失败: {e}")
            return False
    
    def import_template(self, import_path: str, template_name: str) -> bool:
        """从文件导入模板"""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                template = json.load(f)
            
            return self.save_template(template_name, template)
        except Exception as e:
            print(f"导入模板失败: {e}")
            return False