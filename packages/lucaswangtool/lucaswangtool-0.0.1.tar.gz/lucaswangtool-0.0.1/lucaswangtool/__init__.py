"""
lucaswangtool 主模块文件
正确导出核心功能
"""
from .core import MathOperations, MathError, __version__

# 显式声明导出内容（解决Pylance警告）
__all__ = [
    'MathOperations',  # 暴露类给外部访问
    'MathError',       # 暴露异常类型
    '__version__'      # 暴露版本号
]
