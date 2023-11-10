import os
import re
# 遍历ncnn/src/layer子目录下的所有文件，获取文件名，然后将文件名转换为layer层，最后将文件名和layer层写入csv文件中

# 最好是字典类型；主要层为小写relu;名称为Relu;【list存储架构信息0,1,2,3,4,5】

AllDict = {}
# AllDict = {"relu": {0:"Relu",1:[0,0,0,0,0,0]}, }
# 处理完毕后，遍历字典，将Relu和数字1写入csv文件中


def get_layer_name():
    # 获取当前目录路径
    current_path = os.getcwd() + "/src/layer"
    # 获取当前目录下的所有文件名
    file_names = os.listdir(current_path)
    # 打开文件
    # 遍历文件名
    for file_name in file_names:
        # print(file_name)
        # 如果文件名是以.h结尾的
        if file_name.endswith(".h") and file_name != "fused_activation.h":
            # 将文件名转换为layer层
            layer_name = file_name.replace(".h", "")
            # 此处的layer名称对后续内容比较有意义
            AllDict[layer_name] = {0: "", 1: [0, 0, 0, 0, 0, 0]}
            # 读取文件，获得正确的层名
            with open(current_path + "/" + file_name, "r") as f:
                result = re.search("class (\\w+)", str(f.readlines()))
                AllDict[layer_name][0] = result.group(1)
    # 处理arm目录下的文件
    file_names = os.listdir(current_path + "/arm")
    for file_name in file_names:
        # 如果文件名是以.h结尾的
        if file_name.endswith("_arm.h"):
            # 将文件名转换为layer层
            layer_name = file_name.replace("_arm.h", "")
            AllDict[layer_name][1][0] = 1  # 代表arm架构第一个为真
    # 处理loongarch
    file_names = os.listdir(current_path + "/loongarch")
    for file_name in file_names:
        # 如果文件名是以.h结尾的
        if file_name.endswith("_loongarch.h"):
            # 将文件名转换为layer层
            layer_name = file_name.replace("_loongarch.h", "")
            AllDict[layer_name][1][1] = 1  # 代表arm架构第一个为真
    # 处理mips目录下的文件
    file_names = os.listdir(current_path + "/mips")
    for file_name in file_names:
        # 如果文件名是以.h结尾的
        if file_name.endswith("_mips.h"):
            # 将文件名转换为layer层
            layer_name = file_name.replace("_mips.h", "")
            AllDict[layer_name][1][2] = 1  # 代表arm架构第一个为真
    # 处理riscv目录下的文件
    file_names = os.listdir(current_path + "/riscv")
    for file_name in file_names:
        # 如果文件名是以.h结尾的
        if file_name.endswith("_riscv.h"):
            # 将文件名转换为layer层
            layer_name = file_name.replace("_riscv.h", "")
            AllDict[layer_name][1][3] = 1  # 代表arm架构第一个为真
    # 处理vulkan目录下的文件
    file_names = os.listdir(current_path + "/vulkan")
    for file_name in file_names:
        # 如果文件名是以.h结尾的
        if file_name.endswith("_vulkan.h"):
            # 将文件名转换为layer层
            layer_name = file_name.replace("_vulkan.h", "")
            AllDict[layer_name][1][4] = 1  # 代表arm架构第一个为真
    # 处理x86目录下的文件
    file_names = os.listdir(current_path + "/x86")
    for file_name in file_names:
        # 如果文件名是以.h结尾的
        if file_name.endswith("_x86.h"):
            # 将文件名转换为layer层
            layer_name = file_name.replace("_x86.h", "")
            AllDict[layer_name][1][5] = 1  # 代表arm架构第一个为真
    # 白名单操作
    AllDict["split"] = ["Split", [1, 1, 1, 1, 1, 1]]  # split层全支持
    print(AllDict)

    # 遍历字典，写入csv文件
    with open("ncnn_layer.csv", "w", encoding="utf-8") as f:
        f.write(f"Layer,arm,loongarch,mips,riscv,vulkan,x86\n")
        for key, value in AllDict.items():
            # 格式化输出
            f.write(
                f"{value[0]},{value[1][0]},{value[1][1]},{value[1][2]},{value[1][3]},{value[1][4]},{value[1][5]}\n"
            )


if __name__ == "__main__":
    get_layer_name()
