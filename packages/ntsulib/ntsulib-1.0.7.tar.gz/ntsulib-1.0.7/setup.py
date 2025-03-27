import os
import re
import shutil
import subprocess
from setuptools import setup, find_packages


def clean_dist_folder():
    """自动清理 dist 文件夹，避免旧文件干扰"""
    dist_dir = "dist"
    if os.path.exists(dist_dir):
        print(f"🧹 清理旧 dist 文件夹: {dist_dir}")
        shutil.rmtree(dist_dir)


def update_version(version_file="ntsulib/__init__.py"):
    """自动将版本号 +0.0.1，并返回新版本号"""
    try:
        with open(version_file, "r+", encoding="utf-8") as f:
            content = f.read()
            # 使用正则匹配版本号（格式：x.y.z）
            version_match = re.search(r'__version__\s*=\s*["\'](\d+\.\d+\.\d+)["\']', content)
            if not version_match:
                raise ValueError("无法找到版本号！请确保 __init__.py 中有 __version__='x.y.z'")

            old_version = version_match.group(1)
            major, minor, patch = map(int, old_version.split('.'))
            new_version = f"{major}.{minor}.{patch + 1}"  # 自动 +0.0.1

            # 替换为新版本号
            new_content = re.sub(
                r'__version__\s*=\s*["\'][^"\']*["\']',
                f'__version__ = "{new_version}"',
                content
            )
            f.seek(0)
            f.write(new_content)
            f.truncate()

            print(f"🆕 版本号从 {old_version} 更新为 {new_version}")
            return new_version
    except Exception as e:
        print(f"⚠️ 版本号更新失败: {e}")
        return None


def generate_pyproject_toml(version):
    """根据 setup.py 配置自动生成 pyproject.toml"""
    pyproject_content = f"""[build-system]
requires = ["setuptools>=42"]
build-backend = "setuptools.build_meta"

[project]
name = "{setup_params['name']}"
version = "{version}"
authors = [
    {{ name = "{setup_params['author']}", email = "{setup_params['author_email']}" }}
]
description = "{setup_params['description']}"
dependencies = {setup_params['install_requires']}
"""
    with open("pyproject.toml", "w", encoding="utf-8") as f:
        f.write(pyproject_content)
    print("✅ 已生成 pyproject.toml")


def get_install_requires():
    """从 requirements.txt 读取依赖（如果文件存在）"""
    if os.path.exists("requirements.txt"):
        with open("requirements.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return []


# 预执行清理
clean_dist_folder()

# 尝试自动更新版本号
current_version = update_version()
if current_version is None:
    current_version = "1.0.0"  # 默认版本（需手动修复）
    print(f"⚠️ 使用默认版本号: {current_version}")

# 定义 setup() 的参数
setup_params = {
    "name": "ntsulib",
    "version": current_version,  # 使用自动更新的版本号
    "author": "NTsukine",
    "author_email": "398339897@qq.com",
    "description": "ntsulib",
    "long_description": open("README.md", encoding="utf-8").read(),
    "long_description_content_type": "text/markdown",
    "url": "",
    "packages": find_packages(exclude=["测试", "命令"]),
    "install_requires": get_install_requires(),
    "classifiers": [
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    "python_requires": ">=3.8",
    "keywords": ['utility', 'library', 'python', 'tools', 'encryption', 'ntsulib'],
}

# 生成 pyproject.toml（使用更新后的版本号）
generate_pyproject_toml(current_version)

# 调用 setup()
setup(**setup_params)