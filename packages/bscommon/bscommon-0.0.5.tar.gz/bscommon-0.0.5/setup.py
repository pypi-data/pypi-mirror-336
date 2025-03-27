from setuptools import setup, find_packages

setup(
    name="bscommon",
    version="0.0.5",
    packages=find_packages(),
    install_requires=["requests>=2.25", "numpy"],
    author="bs",
    description="冰鼠常用操作库"
)
