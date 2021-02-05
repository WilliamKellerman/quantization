import os
import platform


# 创建文件目录结构
def create_folder(folder_name):
    if platform.system() == "Windows":
        folder_name = 'D:/' + folder_name
    else:
        folder_name = folder_name

    folder_name_exist = os.path.exists(folder_name)

    if not folder_name_exist:
        os.makedirs(folder_name)


create_folder('./pictures/aaa')
