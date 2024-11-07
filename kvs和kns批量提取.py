import os

def 提取内容(文件路径, 目录路径, 起始序列, 文件扩展名, 序列名称):
    try:
        with open(文件路径, 'rb') as 文件:
            内容 = 文件.read()
            计数 = 0
            起始索引 = 0

            while True:
                起始索引 = 内容.find(起始序列, 起始索引)
                if 起始索引 == -1:
                    break

                # 寻找下一个起始序列以确定当前段落的结束位置
                下一个起始索引 = 内容.find(起始序列, 起始索引 + len(起始序列))
                if 下一个起始索引 == -1:
                    结束索引 = len(内容)
                else:
                    结束索引 = 下一个起始索引

                # 提取当前起始序列和下一个起始序列之间的数据
                提取的数据 = 内容[起始索引:结束索引]
                新文件名 = f"{os.path.splitext(os.path.basename(文件路径))[0]}_{计数}{文件扩展名}"
                新文件路径 = os.path.join(目录路径, 新文件名)
                with open(新文件路径, 'wb') as 新文件:
                    新文件.write(提取的数据)
                print(f"导出的文件名: {新文件名}")
                计数 += 1
                起始索引 = 下一个起始索引
    except Exception as e:
        print(f"处理 {文件路径} 时发生错误: {e}")

def main():
    目录路径 = input("请输入要处理的文件夹路径: ")
    if not os.path.isdir(目录路径):
        print(f"错误: {目录路径} 不是一个有效的目录。")
        return

    kvs起始序列 = b'\x4B\x4F\x56\x53'
    kns起始序列 = b'\x4B\x54\x53\x53'

    提取序列选择 = input("请选择要提取的序列类型 (1 - kvs, 2 - kns): ")

    for 根, 目录, 文件 in os.walk(目录路径):
        for 文件名 in 文件:
            文件路径 = os.path.join(根, 文件名)
            print(f"处理文件: {文件路径}")
            文件内容 = open(文件路径, 'rb').read()

            if 提取序列选择 == '1':
                kvs数量 = 文件内容.count(kvs起始序列)
                if kvs数量 > 0:
                    提取内容(文件路径, 目录路径, kvs起始序列, '.kvs', 'kvs')
                else:
                    print(f"文件 {文件路径} 中未找到kvs序列。")
            elif 提取序列选择 == '2':
                kns数量 = 文件内容.count(kns起始序列)
                if kns数量 > 0:
                    提取内容(文件路径, 目录路径, kns起始序列, '.kns', 'kns')
                else:
                    print(f"文件 {文件路径} 中未找到kns序列。")
            else:
                print(f"未选择有效的序列类型。")

if __name__ == "__main__":
    main()
