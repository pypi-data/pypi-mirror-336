"""
标准模块封装模板
版本: 1.0.0
文件结构：
lucaswangtool/
├── __init__.py
└── core.py
"""

__all__ = ['MathOperations', 'MathError']  # 控制导出内容
__version__ = '0.0.1'

class MathError(Exception):
    """自定义数学异常基类"""
    pass

class MathOperations:
    """
    数学操作核心类

    示例用法：
    >>> from lucaswangtool.core import MathOperations
    >>> calc = MathOperations()
    >>> calc.add(3, 5)
    8
    """

    def __init__(self, logger=None):
        """初始化时可注入日志对象"""
        self.logger = logger

    @staticmethod
    def add(a: float, b: float) -> float:
        """
        加法操作
        参数类型验证和异常处理演示
        """
        if not (isinstance(a, (int, float))) or not (isinstance(b, (int, float))):
            raise MathError("Invalid input types")
        return a + b

    # 扩展其他数学方法
    @classmethod
    def subtract(cls, a: float, b: float) -> float:
        """类方法实现减法"""
        return a - b

# 模块自测试
if __name__ == '__main__':
    import doctest
    doctest.testmod()
