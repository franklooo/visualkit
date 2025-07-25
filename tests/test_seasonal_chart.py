import pytest
import pandas as pd
import numpy as np
from visualkit import SeasonalChart


class TestSeasonalChart:
    
    @pytest.fixture
    def sample_data(self):
        """创建测试数据"""
        dates = pd.date_range('2021-01-01', '2022-12-31', freq='D')
        data = pd.DataFrame({
            'date': dates,
            'value': np.random.randn(len(dates)).cumsum() + 100
        })
        return data
    
    @pytest.fixture
    def chart(self):
        """创建图表实例"""
        return SeasonalChart()
    
    def test_create_seasonal_line(self, chart, sample_data):
        """测试创建季节性折线图"""
        result = chart.create_seasonal_line(
            sample_data, 'value', '公历',
            title='测试图表'
        )
        
        assert result is not None
        assert '测试图表' in str(result)
    
    def test_create_seasonal_grid(self, chart, sample_data):
        """测试创建季节性网格图"""
        sample_data['value2'] = sample_data['value'] * 1.1
        
        result = chart.create_seasonal_grid(
            sample_data, ['value', 'value2'], '公历',
            title='测试网格图'
        )
        
        assert result is not None
        assert '测试网格图' in str(result)
    
    def test_invalid_calendar_type(self, chart, sample_data):
        """测试无效的日历类型"""
        with pytest.raises(ValueError):
            chart.create_seasonal_line(
                sample_data, 'value', '无效日历'
            )
    
    def test_missing_column(self, chart, sample_data):
        """测试缺失的列"""
        with pytest.raises(KeyError):
            chart.create_seasonal_line(
                sample_data, 'missing_column', '公历'
            )