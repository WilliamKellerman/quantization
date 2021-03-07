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


def read_caifu_2021_products_xls(file_path):
    sheet = pd.read_excel(file_path, sheet_name=1, header=1, skiprows=0)
    sheet = sheet[sheet['产品类型'].isin(['普通开放式基金', '持有期基金', '定开基金'])]

    # 基金代码int->str, rjust 补足6位，前面填充0
    sheet['基金代码'] = sheet.apply(lambda row: str(row['产品代码']).rjust(6, '0') + '.OF', axis='columns')
    sheet.rename(columns={'产品名称': '基金名称'}, inplace=True)
    return sheet
