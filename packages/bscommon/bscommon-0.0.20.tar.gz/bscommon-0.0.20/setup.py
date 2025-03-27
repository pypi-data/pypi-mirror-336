from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="bscommon",
    version="0.0.20",
    packages=find_packages(where="src"),
    package_dir={'': 'src'},
    install_requires=requirements,
    author="bs",
    description="冰鼠常用操作库"
)
