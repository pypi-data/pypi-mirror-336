import os
from datetime import datetime
from rich.console import Console

# 加载字体颜色
console = Console()


# 分隔符输出
def separator(input_context='我是分隔符'):
    len_context = len(input_context)
    print('-' * (26 - len_context) + str(input_context) + '-' * (26 - len_context))


# 获取最新文件名函数
def get_new_filename(file_dz, file_name, end_name='.xlsx', warn=True):
    file_list = os.listdir(file_dz)
    new_filename = '未找到相应' + str(file_name) + '文件，请确认'
    new_filename_time = 0
    for f in file_list:
        if file_name in f and f.endswith(end_name) and not f.startswith('~'):
            file_time = os.path.getmtime(file_dz + f)
            if file_time > new_filename_time:
                new_filename = file_dz + f
                new_filename_time = file_time
    if warn:
        print('获取到的文件为：', new_filename)
        if (datetime.now() - datetime.fromtimestamp(new_filename_time)).days > 1:
            console.print('该报表超过1天未更新，请及时更新！', style='bold red')
    return new_filename


def get_latest_file_path(file_path, file_name, end_name='.xlsx', warn=True):
    latest_time = 0
    latest_file_name = ''
    latest_file_path = f'未找到相应{file_name}文件，请确认'
    for root, dirs, files in os.walk(file_path):
        for file in files:
            if file.endswith(end_name) and not file.startswith('~') and file_name in file:
                new_file_path = os.path.join(root, file)
                # 获取文件的修改时间
                new_time = os.path.getmtime(new_file_path)
                # 更新最新时间
                if new_time > latest_time:
                    latest_time = new_time
                    latest_file_name = file
                    latest_file_path = new_file_path
    if warn:
        print(f'获取到的文件为：{latest_file_path}')
        if (datetime.now() - datetime.fromtimestamp(latest_time)).days > 1:
            console.print(f'{latest_file_name}，该报表超过1天未更新，请及时更新！', style='bold red')
    return latest_file_path
