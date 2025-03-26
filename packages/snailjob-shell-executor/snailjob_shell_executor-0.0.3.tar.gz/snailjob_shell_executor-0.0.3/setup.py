from setuptools import find_packages, setup

setup(
    name="snailjob-shell-executor",  # 项目名称
    version="0.0.3",  # 项目版本
    packages=find_packages(),  # 自动发现项目中的包
    install_requires=[  # 项目依赖包
        "pydantic==2.7.4",
        "python-dotenv==1.0.1",
        "aiohttp==3.10.9",
        "protobuf==5.27.2",
        "grpcio==1.66.2",
    ],
    python_requires=">=3.8",
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
    entry_points={
        'console_scripts': [
            'start-snailjob=src.start_service:main',
        ],
    },
    include_package_data=True,  # 确保包含包数据
    package_data={
        '': ['.env'],  # 指定要包含的 .env 文件
    },
)
