import os
import subprocess

def extract_fmsg_files(directory):
    # 获取所有.fmsg文件的路径
    fmsg_files = [os.path.join(root, file)
                  for root, dirs, files in os.walk(directory)
                  for file in files if file.endswith('.fmsg')]
    
    total_files = len(fmsg_files)
    print(f"总共找到 {total_files} 个 .fmsg 文件。")

    # 遍历.fmsg文件并解压
    for index, fmsg_file in enumerate(fmsg_files, start=1):
        # 设置输入和输出文件名
        output_file = fmsg_file[:-5] + '.txt'
        
        # 调用PJ5-FMSG-Extractor.exe进行解压
        result = subprocess.run(['PJ5-FMSG-Extractor.exe', '-e', fmsg_file, output_file], capture_output=True)
        
        if result.returncode == 0:
            print(f"[{index}/{total_files}] 已解压 '{fmsg_file}' 为 '{output_file}'")
        else:
            print(f"解压失败: {result.stderr}")
        
        # 显示进度
        progress = (index / total_files) * 100
        print(f"已完成 {index}/{total_files} ({progress:.2f}%)")

if __name__ == "__main__":
    directory_path = input("请输入一个有效的路径: ")
    if os.path.isdir(directory_path):
        extract_fmsg_files(directory_path)
    else:
        print("输入的不是一个有效的路径。")
