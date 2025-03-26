
## snail-job-shell-executor

使用snail-job 项目的 python 客户端。[snail-job项目 java 后端](https://gitee.com/aizuda/snail-job)开发的Linux Shell 执行器，用于执行定时任务。具有以下特点

1. 执行器一旦运行，只需要在控制中心配置即可，不需要编写 Python 脚本
2. 同时可以作为普通snail-job-python包引入，编写自己的任务脚本
3. 支持结果上报，支持日志上报

## 开始使用

```shell
# 安装

# 配置


# 复制 `.env.example` 为 `.env`
cp .env.example .env # windows命令为 copy
# 创建虚拟环境
python -m venv venv
# 安装依赖
pip install -r requirements.txt
# 启动程序
python main.py
```

登录后台，能看到对应host-id 为 `py-xxxxxx` 的客户端

**注意: snail-job-python 支持 `pip` 包安装，包名为`snail-job-python`**

### 示例


### gRPC

开发者工具

```shell
pip install grpcio-tools==1.66.2

cd snailjob/grpc/
python -m grpc_tools.protoc --python_out=. --grpc_python_out=. -I. *.proto
```

HACK, 需要手动修改自动生成的文件 `snailjob/grpc/snailjob_pb2_grpc.py`

```diff
- import snailjob_pb2 as snailjob__pb2
+ from . import snailjob_pb2 as snailjob__pb2
```
