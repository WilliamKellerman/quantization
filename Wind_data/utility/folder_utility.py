import os


# 创建文件目录结构
def create_folder(folder_name):
    folder_name_exist = os.path.exists(folder_name)
    if not folder_name_exist:
        os.makedirs(folder_name)
