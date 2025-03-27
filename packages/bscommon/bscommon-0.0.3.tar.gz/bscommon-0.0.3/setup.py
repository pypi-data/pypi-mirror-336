from setuptools import setup, find_packages

setup(
    name="bscommon",
    version="0.0.3",
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=["requests>=2.25", "numpy"],
    author="bs",
    description="冰鼠常用操作库"
)
