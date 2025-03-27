import os
import subprocess
from setuptools import setup, find_packages

# 自动生成 requirements.txt 并返回安装的依赖
def generate_requirements():
    # 执行 pip freeze 并将输出写入 requirements.txt
    with open("requirements.txt", "w", encoding="utf-8") as f:
        subprocess.run(["pip", "freeze"], stdout=f)

# 自动从 requirements.txt 读取库并返回
def get_install_requires():
    generate_requirements()  # 生成 requirements.txt
    if os.path.exists("requirements.txt"):
        with open("requirements.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    return []

setup(
    name="ntsulib",
    version="1.0.3",
    author="NTsukine",
    author_email="398339897@qq.com",
    description="ntsulib",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(exclude=["测试", "命令"]),
    install_requires=get_install_requires(),  # 自动填充依赖库
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    keywords=['utility', 'library', 'python', 'tools', 'encryption']
)
