from distutils.core import setup
from setuptools import find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="zhiwowo",  # 包名，PyPI上将显示的名称
    version="1.0.11",            # 版本号
    author="wowohr#middleend",  # 作者信息
    description="人力窝-智窝助手sdk",  # 简要描述
    long_description=long_description,  # 详细描述（从 README.md 中读取）
    long_description_content_type="text/markdown",
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries'
    ],
    python_requires='>=3.6',
)
