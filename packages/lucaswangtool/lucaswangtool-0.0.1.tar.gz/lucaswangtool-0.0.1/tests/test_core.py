"""
单元测试示例（使用unittest）
运行命令：python -m unittest discover -v
"""
import sys
import os
import unittest
# 关键路径处理：将项目根目录加入Python路径
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lucaswangtool.core import MathOperations, MathError

class TestMathOperations(unittest.TestCase):
    def setUp(self):
        self.calc = MathOperations()
    
    def test_add_normal(self):
        self.assertEqual(self.calc.add(3, 5), 8)
        self.assertAlmostEqual(self.calc.add(2.5, 3.1), 5.6)
    
    def test_add_invalid_type(self):
        with self.assertRaises(MathError):
            self.calc.add("3", 5)

if __name__ == '__main__':
    unittest.main()
