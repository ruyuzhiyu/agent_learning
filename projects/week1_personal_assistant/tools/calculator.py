"""
计算器工具
"""

from langchain.tools import BaseTool
import ast
import operator


class CalculatorTool(BaseTool):
    """
    计算器工具
    执行数学计算
    """
    name = "calculator"
    description = "计算器工具，用于执行数学计算。输入数学表达式，返回计算结果。例如：2+2, 10*5, 100/4"
    
    # 支持的安全操作符
    _operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
    }
    
    def _safe_eval(self, node):
        """安全地评估数学表达式"""
        if isinstance(node, (ast.Num, ast.Constant)):  # 数字（兼容Python 3.8+）
            # ast.Constant用于Python 3.8+，ast.Num用于旧版本
            return node.n if isinstance(node, ast.Num) else node.value
        elif isinstance(node, ast.BinOp):  # 二元运算符
            op = self._operators.get(type(node.op))
            if op is None:
                raise ValueError(f"不支持的操作符: {type(node.op).__name__}")
            return op(self._safe_eval(node.left), self._safe_eval(node.right))
        elif isinstance(node, ast.UnaryOp):  # 一元运算符
            op = self._operators.get(type(node.op))
            if op is None:
                raise ValueError(f"不支持的操作符: {type(node.op).__name__}")
            return op(self._safe_eval(node.operand))
        else:
            raise ValueError(f"不支持的节点类型: {type(node).__name__}")
    
    def _run(self, expression: str) -> str:
        """执行计算"""
        try:
            # 清理输入
            expression = expression.strip()
            
            # 安全检查：只允许数字和基本运算符
            allowed_chars = set('0123456789+-*/(). ')
            if not all(c in allowed_chars for c in expression):
                return "错误：表达式包含不允许的字符。只支持数字和 +-*/() 运算符。"
            
            # 使用AST安全解析和执行
            tree = ast.parse(expression, mode='eval')
            result = self._safe_eval(tree.body)
            
            # 格式化结果
            if isinstance(result, float):
                # 如果是整数结果，不显示小数点
                if result.is_integer():
                    return f"{expression} = {int(result)}"
                else:
                    return f"{expression} = {result:.4f}"
            else:
                return f"{expression} = {result}"
                
        except ZeroDivisionError:
            return "错误：除数不能为零"
        except SyntaxError:
            return "错误：表达式格式不正确"
        except Exception as e:
            return f"计算错误：{str(e)}"
    
    async def _arun(self, expression: str) -> str:
        """异步执行"""
        return self._run(expression)
