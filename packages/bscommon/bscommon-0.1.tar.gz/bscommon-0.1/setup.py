from setuptools import setup, find_packages

setup(
    name="bscommon",
    version="0.1",
    packages=find_packages(),
    install_requires=["requests>=2.25", "numpy"],
    author="bs",
    description="冰鼠常用操作库"
)
