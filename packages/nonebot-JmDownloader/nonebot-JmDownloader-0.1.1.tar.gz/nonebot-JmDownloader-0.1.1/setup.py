from setuptools import setup, find_packages

setup(
    name="nonebot-JmDownloader",  # 包的名称，唯一且不与现有包冲突
    version="0.1.1",      # 版本号，建议遵循语义化版本规范 (如 0.1.0)
    author="Maksie",      # 作者姓名
    author_email="makise@crazyforcode.org",  # 作者邮箱
    description="A NoneBot plugin to download JmComics and upload",  # 优化描述，明确插件用途
    long_description_content_type="text/markdown",  # README 文件格式
    url="https://github.com/MakiseCrise/jmDownloader",  # 项目主页（移除 .git 后缀，通常不需要）
    packages=find_packages(),  # 自动查找包
    install_requires=[         # 依赖的第三方库
        "nonebot2>=2.0.0",     # 添加 NoneBot2 依赖（假设使用 NoneBot2，版本可调整）
        "requests>=2.25.1",
        "jmcomic",
        "img2pdf",
    ],
    classifiers=[              # 分类信息，帮助用户发现你的包
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",  # 添加具体支持的版本
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",   # 建议将最低版本提升至 3.8，NoneBot2 推荐此版本
)