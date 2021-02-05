import openpyxl
import pandas as pd

import os


def append_to_new_sheet(data, wb_file, sheet_name):
    if os.path.exists(wb_file):
        book = openpyxl.load_workbook(wb_file)  # 读取你要写入的workbook
    else:
        book = openpyxl.Workbook()
    # pd.read_excel() 用于将Dataframe写入excel。
    # xls用xlwt; xlsx用openpyxl
    writer = pd.ExcelWriter(wb_file, engine='openpyxl')
    # 此时的writer里还只是读写器. 然后将上面读取的book复制给writer
    writer.book = book
    # 转化为字典的形式
    writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
    # 将data写入writer
    data.to_excel(writer, sheet_name=sheet_name, index=False)
    writer.save()
