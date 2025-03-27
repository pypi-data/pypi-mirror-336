# 从子模块 your_code.py 中导入 hello 函数

from .ChangYing import BaoCuoXingxi,xk

# 定义外部可访问的内容（非必须，但推荐）
__all__ = ["BaoCuoXingxi","hello","xk"]