from setuptools import find_packages, setup

setup(
    name="snailjob-shell-executor",  # 项目名称
    version="0.0.1",  # 项目版本
    packages=find_packages(),  # 自动发现项目中的包
    install_requires=[  # 项目依赖包
        "pydantic",
        "python-dotenv",
        "aiohttp",
        "protobuf",
        "grpcio",
    ],
    python_requires=">=3.9",
    long_description=open("README.md").read(),  # 读取 README.md 文件作为长描述
    long_description_content_type="text/markdown",  # 长描述格式
    author="rhinux",
    author_email="rhinux.x@gmail.com",
    description="SnailJob python客户端开发的Shell执行器",
    url="https://github.com/rhinuxx/snail-job",  # 项目主页
    classifiers=[  # 项目的分类信息
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
