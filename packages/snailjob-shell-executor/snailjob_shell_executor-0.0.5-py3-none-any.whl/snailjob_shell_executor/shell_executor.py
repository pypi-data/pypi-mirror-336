from . import *
import subprocess
@job("shellCommandExecutor")
def shell_command_executor(args: JobArgs) -> ExecuteResult:
    # 获取命令参数
    command = args.job_params.strip()
    
    # 定义危险命令列表
    dangerous_commands = ["rm", "fdisk", "format", "shutdown", "reboot"]
    
    # 分割命令并检查第一个部分是否为危险命令
    command_parts = command.split()
    if command_parts and command_parts[0] in dangerous_commands:
        error_message = "拒绝执行危险命令: " + command
        SnailLog.REMOTE.error(error_message)
        return ExecuteResult.failure(error_message)
    
    # 执行 shell 命令并捕获输出
    result = subprocess.run(
        command, 
        shell=True, 
        capture_output=True, 
        text=True
    )
    
    # 记录标准输出和错误输出
    SnailLog.REMOTE.info(f"stdout: {result.stdout}")
    SnailLog.REMOTE.info(f"stderr: {result.stderr}")
    
    # 根据命令执行结果返回状态
    if result.returncode == 0:
        return ExecuteResult.success(result.stdout)
    else:
        return ExecuteResult.failure(result.stderr)
    
if __name__ == "__main__":
    ExecutorManager.register(shell_command_executor)
    client_main()
