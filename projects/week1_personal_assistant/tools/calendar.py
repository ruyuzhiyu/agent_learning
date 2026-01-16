"""
日程管理工具
"""

from typing import Optional
from langchain.tools import BaseTool
from datetime import datetime


class CalendarTool(BaseTool):
    """
    日程管理工具
    支持添加、查询和删除日程
    """
    name = "calendar"
    description = """日程管理工具。用于管理日程安排。
    支持的操作：
    - 添加日程：格式为 "add: 时间 事项"，例如 "add: 明天下午3点 开会"
    - 查询日程：格式为 "query: 日期"，例如 "query: 明天" 或 "query: all"
    - 删除日程：格式为 "delete: 事项关键词"
    """
    
    def __init__(self):
        super().__init__()
        # 使用简单的内存存储（实际项目应使用数据库）
        self.events = []
    
    def _run(self, query: str) -> str:
        """执行日程管理操作"""
        query = query.strip()
        
        # 添加日程
        if query.startswith("add:"):
            event_info = query.replace("add:", "").strip()
            self.events.append({
                "info": event_info,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            return f"已添加日程：{event_info}"
        
        # 查询日程
        elif query.startswith("query:"):
            date_query = query.replace("query:", "").strip()
            if date_query == "all" or not date_query:
                if not self.events:
                    return "暂无日程安排"
                result = "所有日程：\n"
                for i, event in enumerate(self.events, 1):
                    result += f"{i}. {event['info']}\n"
                return result.strip()
            else:
                # 简单匹配（实际应该更智能）
                matched = [e for e in self.events if date_query in e['info']]
                if not matched:
                    return f"未找到包含'{date_query}'的日程"
                result = f"找到 {len(matched)} 个相关日程：\n"
                for i, event in enumerate(matched, 1):
                    result += f"{i}. {event['info']}\n"
                return result.strip()
        
        # 删除日程
        elif query.startswith("delete:"):
            keyword = query.replace("delete:", "").strip()
            original_count = len(self.events)
            self.events = [e for e in self.events if keyword not in e['info']]
            deleted_count = original_count - len(self.events)
            if deleted_count > 0:
                return f"已删除 {deleted_count} 个包含'{keyword}'的日程"
            else:
                return f"未找到包含'{keyword}'的日程"
        
        else:
            return "请使用正确的格式：add/query/delete: 内容"
    
    async def _arun(self, query: str) -> str:
        """异步执行"""
        return self._run(query)
