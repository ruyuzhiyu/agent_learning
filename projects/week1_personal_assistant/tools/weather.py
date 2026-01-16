"""
天气查询工具
"""

from langchain.tools import BaseTool


class WeatherTool(BaseTool):
    """
    天气查询工具
    查询指定城市的天气信息
    """
    name = "weather"
    description = "查询城市天气。输入城市名称，返回天气信息。例如：北京、上海、深圳"
    
    def _run(self, city: str) -> str:
        """查询天气"""
        # 模拟天气数据（实际应接入真实天气API）
        weather_data = {
            "北京": {
                "weather": "晴天",
                "temperature": "15-25度",
                "quality": "空气质量良好",
                "humidity": "湿度50%"
            },
            "上海": {
                "weather": "多云",
                "temperature": "18-26度",
                "quality": "空气质量一般",
                "humidity": "湿度65%"
            },
            "深圳": {
                "weather": "阴天",
                "temperature": "22-28度",
                "quality": "空气质量优",
                "humidity": "湿度70%"
            },
            "广州": {
                "weather": "小雨",
                "temperature": "20-27度",
                "quality": "空气质量优",
                "humidity": "湿度75%"
            },
            "杭州": {
                "weather": "晴天",
                "temperature": "16-24度",
                "quality": "空气质量良好",
                "humidity": "湿度55%"
            }
        }
        
        city = city.strip()
        
        if city in weather_data:
            data = weather_data[city]
            return f"{city}天气：{data['weather']}，{data['temperature']}，{data['quality']}，{data['humidity']}"
        else:
            return f"抱歉，暂时没有{city}的天气信息。支持的城市：北京、上海、深圳、广州、杭州"
    
    async def _arun(self, city: str) -> str:
        """异步执行"""
        return self._run(city)
