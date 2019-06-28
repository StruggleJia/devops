#! /usr/bin/env python
# -*- coding: utf-8 -*-
# code by struggle
# 2019-06-28

import json
from openpyxl import load_workbook

class ExcelToJson(object):
    def __init__(self, filename):
        self.filename = filename
        self.workfile = load_workbook(self.filename)
        self.sheet = None
        self.cellstatus = {}
        self.allinfo = []
    
    def get_sheet_name(self):
        return self.workfile.get_sheet_names()

    def select_sheet(self, sheetname):
        self.sheet = self.workfile.get_sheet_by_name(sheetname)

    def sheet_size(self):
        if self.sheet:
            return "数据表最大的坐标\n" + "最大数据的行数:" + str(self.sheet.max_row) + "\n" + "最大数据的列数:" + str(self.sheet.max_column)

    def bgcolor_no(self, start_wz, end_wz):
        if self.sheet:
            for cell in self.sheet[start_wz:end_wz]:
                for i in cell:
                    self.cellstatus[i.fill.start_color.index] = i.value

    def select_sheet_info(self, action="LR"):
        if action == "LR":
            for row in self.sheet.rows:
                for cell in row:
                    info = {}
                    if cell.comment:
                        zb =  str(cell.column)+ "-" + str(cell.row)
                        try:
                            status = self.cellstatus[cell.fill.start_color.index]
                        except:
                            status = "ERROR"
                        rack = cell.value
                        v = cell.comment.text
                        info['status'] = status
                        info['code'] = rack
                        info['description'] = v.replace("\n", " ")
                        info['meta'] = zb
                        self.allinfo.append(info)
            return self.allinfo

if __name__ == "__main__":
    a = ExcelToJson('1111.xlsx')   #excel文件名
    a.select_sheet("2222")         #标签名称
    a.bgcolor_no("M29", "M39")     #图形规则及颜色对应的status_id
    c = a.select_sheet_info()      #处理只有标注的cell信息，生成字典
    print(c)