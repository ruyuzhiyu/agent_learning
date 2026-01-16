"""
备忘录工具
"""

from langchain.tools import BaseTool
from datetime import datetime


class MemoTool(BaseTool):
    """
    备忘录工具
    记录和查询备忘事项
    """
    name = "memo"
    description = """备忘录工具，用于记录和查询备忘事项。
    支持的操作：
    - 添加备忘录：格式为 "add: 内容"，例如 "add: 记得买牛奶"
    - 查询备忘录：格式为 "query" 或 "query: 关键词"
    - 删除备忘录：格式为 "delete: 关键词"
    """
    
    def __init__(self):
        super().__init__()
        # 使用简单的内存存储
        self.memos = []
    
    def _run(self, query: str) -> str:
        """执行备忘录操作"""
        query = query.strip()
        
        # 添加备忘录
        if query.startswith("add:"):
            content = query.replace("add:", "").strip()
            if not content:
                return "错误：备忘录内容不能为空"
            
            memo = {
                "content": content,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.memos.append(memo)
            return f"已添加备忘录：{content}"
        
        # 查询备忘录
        elif query.startswith("query"):
            # 提取关键词
            keyword = query.replace("query:", "").replace("query", "").strip()
            
            if not self.memos:
                return "暂无备忘录"
            
            if keyword:
                # 按关键词搜索
                matched = [m for m in self.memos if keyword in m['content']]
                if not matched:
                    return f"未找到包含'{keyword}'的备忘录"
                result = f"找到 {len(matched)} 条相关备忘录：\n"
                for i, memo in enumerate(matched, 1):
                    result += f"{i}. {memo['content']} ({memo['created_at']})\n"
                return result.strip()
            else:
                # 显示所有备忘录
                result = f"共有 {len(self.memos)} 条备忘录：\n"
                for i, memo in enumerate(self.memos, 1):
                    result += f"{i}. {memo['content']} ({memo['created_at']})\n"
                return result.strip()
        
        # 删除备忘录
        elif query.startswith("delete:"):
            keyword = query.replace("delete:", "").strip()
            if not keyword:
                return "错误：请指定要删除的关键词"
            
            original_count = len(self.memos)
            self.memos = [m for m in self.memos if keyword not in m['content']]
            deleted_count = original_count - len(self.memos)
            
            if deleted_count > 0:
                return f"已删除 {deleted_count} 条包含'{keyword}'的备忘录"
            else:
                return f"未找到包含'{keyword}'的备忘录"
        
        else:
            return "请使用正确的格式：add/query/delete: 内容"
    
    async def _arun(self, query: str) -> str:
        """异步执行"""
        return self._run(query)
