from matplotlib.font_manager import FontManager
import platform


# 获取系统字体
def get_system_font():
    fm = FontManager()
    mat_fonts = set(f.name for f in fm.ttflist)
    print(mat_fonts)


# 根据系统选取字体
def select_chinese_font_by_os():
    if platform.system() == "Windows":
        font = 'SimHei'
    else:
        font = 'Arial Unicode MS'
    return font
