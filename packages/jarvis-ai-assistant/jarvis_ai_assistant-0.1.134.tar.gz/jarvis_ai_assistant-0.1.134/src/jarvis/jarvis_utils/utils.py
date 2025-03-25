import os
import time
import hashlib
from pathlib import Path
from typing import Dict
import psutil
from jarvis.jarvis_utils.config import get_max_token_count
from jarvis.jarvis_utils.embedding import get_context_token_count
from jarvis.jarvis_utils.input import get_single_line_input
from jarvis.jarvis_utils.output import PrettyOutput, OutputType
def init_env():
    """初始化环境变量从~/.jarvis/env文件
    
    功能：
    1. 创建不存在的.jarvis目录
    2. 加载环境变量到os.environ
    3. 处理文件读取异常
    """
    jarvis_dir = Path.home() / ".jarvis"
    env_file = jarvis_dir / "env"
    
    # Check if ~/.jarvis directory exists
    if not jarvis_dir.exists():
        jarvis_dir.mkdir(parents=True)
    if env_file.exists():
        try:
            with open(env_file, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith(("#", ";")):
                        try:
                            key, value = line.split("=", 1)
                            os.environ[key.strip()] = value.strip().strip("'").strip('"')
                        except ValueError:
                            continue
        except Exception as e:
            PrettyOutput.print(f"警告: 读取 {env_file} 失败: {e}", OutputType.WARNING)
def while_success(func, sleep_time: float = 0.1):
    """循环执行函数直到成功
    
    参数：
    func -- 要执行的函数
    sleep_time -- 每次失败后的等待时间（秒）
    
    返回：
    函数执行结果
    """
    while True:
        try:
            return func()
        except Exception as e:
            PrettyOutput.print(f"执行失败: {str(e)}, 等待 {sleep_time}s...", OutputType.ERROR)
            time.sleep(sleep_time)
            continue
def while_true(func, sleep_time: float = 0.1):
    """Loop execution function, until the function returns True"""
    while True:
        ret = func()
        if ret:
            break
        PrettyOutput.print(f"执行失败, 等待 {sleep_time}s...", OutputType.WARNING)
        time.sleep(sleep_time)
    return ret
def get_file_md5(filepath: str)->str:    
    """Calculate the MD5 hash of a file's content.
    
    Args:
        filepath: Path to the file to hash
        
    Returns:
        str: MD5 hash of the file's content
    """
    return hashlib.md5(open(filepath, "rb").read(100*1024*1024)).hexdigest()
def user_confirm(tip: str, default: bool = True) -> bool:
    """Prompt the user for confirmation with a yes/no question.
    
    Args:
        tip: The message to show to the user
        default: The default response if user hits enter
        
    Returns:
        bool: True if user confirmed, False otherwise
    """
    suffix = "[Y/n]" if default else "[y/N]"
    ret = get_single_line_input(f"{tip} {suffix}: ")
    return default if ret == "" else ret.lower() == "y"
def get_file_line_count(filename: str) -> int:
    """Count the number of lines in a file.
    
    Args:
        filename: Path to the file to count lines for
        
    Returns:
        int: Number of lines in the file, 0 if file cannot be read
    """
    try:
        return len(open(filename, "r", encoding="utf-8", errors="ignore").readlines())
    except Exception as e:
        return 0
def init_gpu_config() -> Dict:
    """初始化GPU配置
    
    功能：
    1. 检测CUDA可用性
    2. 计算设备内存和共享内存
    3. 设置CUDA内存分配策略
    4. 处理异常情况
    
    返回：
    包含GPU配置信息的字典
    """
    config = {
        "has_gpu": False,
        "shared_memory": 0,
        "device_memory": 0,
        "memory_fraction": 0.8  # 默认使用80%的可用内存
    }

    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
    
    try:
        import torch
        if torch.cuda.is_available():
            # 获取GPU信息
            gpu_mem = torch.cuda.get_device_properties(0).total_memory
            config["has_gpu"] = True
            config["device_memory"] = gpu_mem
            
            # 估算共享内存 (通常是系统内存的一部分)
            system_memory = psutil.virtual_memory().total
            config["shared_memory"] = min(system_memory * 0.5, gpu_mem * 2)  # 取系统内存的50%或GPU内存的2倍中的较小值
            
            # 设置CUDA内存分配
            torch.cuda.set_per_process_memory_fraction(config["memory_fraction"])
            torch.cuda.empty_cache()
            
            PrettyOutput.print(
                f"GPU已初始化: {torch.cuda.get_device_name(0)}\n"
                f"设备内存: {gpu_mem / 1024**3:.1f}GB\n"
                f"共享内存: {config['shared_memory'] / 1024**3:.1f}GB", 
                output_type=OutputType.SUCCESS
            )
        else:
            PrettyOutput.print("没有GPU可用, 使用CPU模式", output_type=OutputType.WARNING)
    except Exception as e:
        PrettyOutput.print(f"GPU初始化失败: {str(e)}", output_type=OutputType.WARNING)
        
    return config


def is_long_context(files: list) -> bool:
    """检查文件列表是否属于长上下文
    
    判断标准：
    当总token数超过最大上下文长度的80%时视为长上下文
    
    参数：
    files -- 要检查的文件路径列表
    
    返回：
    布尔值表示是否属于长上下文
    """
    max_token_count = get_max_token_count()
    threshold = max_token_count * 0.8
    total_tokens = 0
    
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8', errors="ignore") as f:
                content = f.read()
                total_tokens += get_context_token_count(content)
                
                if total_tokens > threshold:
                    return True
        except Exception as e:
            PrettyOutput.print(f"读取文件 {file_path} 失败: {e}", OutputType.WARNING)
            continue
            
    return total_tokens > threshold


def ot(tag_name: str) -> str:
    """生成HTML标签开始标记
    
    参数：
    tag_name -- HTML标签名称
    
    返回：
    格式化的开始标签字符串
    """
    return f"<{tag_name}>"

def ct(tag_name: str) -> str:
    """生成HTML标签结束标记
    
    参数：
    tag_name -- HTML标签名称
    
    返回：
    格式化的结束标签字符串
    """
    return f"</{tag_name}>"
