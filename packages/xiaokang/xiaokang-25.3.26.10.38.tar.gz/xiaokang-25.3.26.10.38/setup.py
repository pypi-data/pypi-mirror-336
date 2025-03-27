from setuptools import setup, find_packages

setup(
    name="xiaokang",
    version="25.03.26.10.38",
    packages=find_packages(),
    setup_requires=["setuptools>=61.0", "wheel"],  # 添加此行
)


# pip install -e .
# pip install -e . -i https://pypi.tuna.tsinghua.edu.cn/simple
# setup.py bdist_wheel
