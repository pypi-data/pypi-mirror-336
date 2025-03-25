from setuptools import setup, find_packages

setup(
    name="JmDownloader",  # 包的名称，唯一且不与现有包冲突
    version="0.1.0",           # 版本号，建议遵循语义化版本规范 (如 0.1.0)
    author="Maksie",        # 作者姓名
    author_email="makise@crazyforcode.org",  # 作者邮箱
    description="A nonebot plugin used to download JmComics and upload",  # 简短描述
    long_description_content_type="text/markdown",  # README 文件格式
    url="https://github.com/MakiseCrise/jmDownloader.git",  # 项目主页（如 GitHub 链接）
    packages=find_packages(),  # 自动查找包
    install_requires=[         # 依赖的第三方库
        "requests>=2.25.1",
    ],
    classifiers=[              # 分类信息，帮助用户发现你的包
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",   # 支持的 Python 版本
)