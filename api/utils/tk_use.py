# -*- coding: utf-8 -*-

"""
@author: HighWay.Li
@contact:byamian@gmail.com
@version: 1.0.0
@license: Apache Licence
@file: tk_use.py
@time: 12/12/24 PM8:50
"""
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


def select_directory():
    root = tk.Tk()
    root.withdraw()
    answer = messagebox.askquestion('重要提示', message='请选择数据保存目录', icon='warning')
    if answer == 'no':
        sys.exit()
    folder_selected = filedialog.askdirectory()
    return folder_selected

if __name__ == '__main__':
    print(select_directory())
