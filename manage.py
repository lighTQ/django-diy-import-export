#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import shutil
import sys
import tkinter as tk
from tkinter import filedialog,messagebox



def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


def get_resource_path():
    try:
        base_path= sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return base_path



def select_directory():
    root = tk.Tk()
    root.withdraw()
    answer = messagebox.askquestion('重要提示', message='请选择数据保存目录', icon='warning')
    if answer == 'no':
        sys.exit()
    folder_selected = filedialog.askdirectory()
    return folder_selected

def diy_db_location():
    # cur db file location
    base_path = get_resource_path()
    db_name = os.path.join(base_path,'db.sqlite3')

    config_file = os.path.join(os.path.expanduser('~'),'.diy_db_path_config')
    # # 检查是否已经有数据库目录配置
    if os.path.exists(config_file):
        print(f'find existing config file: {config_file}')
        with open(config_file, 'r') as file:
            db_directory = file.read().strip()
            if not db_directory:
                db_directory = select_directory()
                # db_directory = '/Users/qlight/Downloads/db_store'
                with open(config_file, 'w') as file:
                    file.write(db_directory)
            else:
                print(f'loading db from  config file value : {db_directory}')
    else:
        db_directory = select_directory()
        # db_directory = '/Users/qlight/Downloads/db_store'
        with open(config_file, 'w') as file:
            file.write(db_directory)

    # 复制数据库文件到新目录（如果不存在）
    src_db_path = db_name
    dst_db_path = os.path.join(db_directory, os.path.basename(src_db_path))

    if not os.path.exists(dst_db_path):
        shutil.copy(src_db_path, dst_db_path)

    print('before set new db path :',dst_db_path)
    os.environ['DJANGO_DB_PATH'] = dst_db_path
    print(f" after set config in env_db_name :'{os.environ.get('DJANGO_DB_PATH')}'" )


def exe_main():
    """Run administrative tasks."""
    diy_db_location()

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    from core.settings import HOSTNAME, PORT
    # 服务器运行命令
    command =['mange.py', 'runserver', f'{HOSTNAME}:{PORT}', '--noreload']
    execute_from_command_line(command)

if __name__ == '__main__':
    # 1. local run
    # main()
    # 2.package exe run
    exe_main()
