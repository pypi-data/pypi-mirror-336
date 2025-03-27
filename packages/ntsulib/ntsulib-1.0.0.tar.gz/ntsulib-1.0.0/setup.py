import os
import codecs
from setuptools import setup, find_packages

# here = os.path.abspath(os.path.dirname(__file__))
#
# with open(os.path.join(here, 'README.md'), encoding='utf-8') as fh:
#     long_description = "\n" + fh.read()
#
#

setup(
    name="ntsulib",  # 你的库名称，上传到 PyPI 后 pip install 用这个名字
    version="1.0.0",  # 版本号，遵循语义化版本
    author="NTsukine",
    author_email="398339897@qq.com",
    description="ntsulib",  # 你的库的简要描述
    long_description=open("README.md", encoding="utf-8").read(),  # 读取 README 作为详细描述
    long_description_content_type="text/markdown",  # README 格式
    url="",  # 你的 GitHub 地址或项目主页
    packages=find_packages(exclude=["测试", "命令"]),  # 自动查找包，不包括 tests 和 docs
    install_requires=[
    ],
    classifiers=[
        "Development Status :: 4 - Beta",  # 4-Beta 表示测试阶段，可以改成 5-Production/Stable
        "License :: OSI Approved :: MIT License",  # 许可证类型，例如 MIT
        "Programming Language :: Python :: 3",  # 支持的 Python 版本
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",  # 要求的最低 Python 版本
    keywords=[]
)
