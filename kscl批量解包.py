import os
import subprocess
import threading
import sys

def extract_file(kscl_file):
    try:
        # 假设命令行参数可以同时处理多个文件
        result = subprocess.run(['PJ5-KSCL-Unpacker.exe', kscl_file], check=True, text=True, capture_output=True)
        # 输出结果（可选）
        print(f"成功解压: {kscl_file}\n输出: {result.stdout}")
    except subprocess.CalledProcessError as e:
        # 打印错误信息
        print(f"解压失败: {kscl_file}, 错误: {e.stderr}")
        sys.exit(1)  # 使用非零状态码表示错误

def extract_kscl_files(directory):
    kscl_files = [os.path.join(root, file)
                  for root, dirs, files in os.walk(directory)
                  for file in files if file.endswith('.kscl')]
    
    threads = []
    for kscl_file in kscl_files:
        thread = threading.Thread(target=extract_file, args=(kscl_file,))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

# 获取输入的文件夹路径
directory = input("请输入包含.kscl文件的文件夹路径: ")

# 检查路径是否存在
if os.path.isdir(directory):
    extract_kscl_files(directory)
else:
    print("输入的路径不存在或不是一个目录。")
    sys.exit(1)  # 使用非零状态码表示错误