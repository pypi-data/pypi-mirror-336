import csv
import hashlib
import json
import os
import platform
import random
import re
import time
import uuid
from datetime import datetime
from datetime import timedelta
import subprocess
import threading
import openpyxl
import xlrd
from yplib import *

# 创建一个线程本地存储对象
__THREAD_LOCAL_INDEX_DATA = threading.local()


# 是否是 windows 系统
def is_win():
    return platform.system().lower() == 'windows'


# 是否是 linux 系统, 不是 windows , 就是 linux 系统
def is_linux():
    return not is_win()


def to_print(*args, time_prefix=False):
    """
    记录日志, 如果是对象会转化为 json
    数据直接 print, 不记录到文件
    例如: aaa
    """
    d = ' '.join(map(lambda x: json.dumps(x) if can_use_json(x) else str(x), args))
    d = d.strip()
    lo = datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ' ' + d if time_prefix is True else d
    if lo is None or str(lo) == '':
        lo = to_datetime(r_str=True)
    print(lo)
    return lo


def to_log(*args, time_prefix=None):
    """
    记录日志, 如果是对象会转化为 json
    前面加了时间
    例如: 2024-11-07 10:23:47 aaa
    """
    return to_print(*args, time_prefix=time_prefix if time_prefix is not None else True)


def to_print_file_thread(*args, file_path=None, file_name=None, mode='a'):
    """
    将 文本输出到 第一次调用 to_print_file_thread 的时候, 指定的 file_path 中
    例如
    to_print_file_thread('aaa', file_path='sql_file', mode='w')
    to_print_file_thread('aaa')
    """
    file_path = __THREAD_LOCAL_INDEX_DATA.to_print_file_thread = file_path or getattr(__THREAD_LOCAL_INDEX_DATA, 'to_print_file_thread', None)
    to_txt(data_list=[to_print(*args)],
           file_name=datetime.today().strftime('%Y-%m-%d') if file_name is None else file_name,
           file_path=str(file_path if file_path is not None else 'to_print_file_thread'),
           mode=mode,
           fixed_name=True,
           suffix='.txt')


def to_print_date_file(*args, file_path=None, file_name=None, mode='a'):
    """
    将 文本输出到 date_file 中
    例如
    """
    file_path = __THREAD_LOCAL_INDEX_DATA.to_print_date_file = file_path or getattr(__THREAD_LOCAL_INDEX_DATA, 'to_print_date_file', None)
    to_txt(data_list=[to_print(*args)],
           file_name=datetime.today().strftime('%Y-%m-%d') if file_name is None else file_name,
           file_path=str(file_path if file_path is not None else 'to_print_date_file'),
           mode=mode,
           fixed_name=True,
           suffix='.txt')


def to_print_file(*args, file_path=None, file_name=None, mode='a'):
    """
    将 print 数据, 写入到 print_file 文件
    文件按照 日期自动创建
    例如: print_file/2020-01-01.txt
    """
    file_path = __THREAD_LOCAL_INDEX_DATA.to_print_file = file_path or getattr(__THREAD_LOCAL_INDEX_DATA, 'to_print_file', None)
    to_txt(data_list=[to_print(*args)],
           file_name=datetime.today().strftime('%Y-%m-%d') if file_name is None else file_name,
           file_path=str(file_path if file_path is not None else 'to_print_file'),
           mode=mode,
           fixed_name=True,
           suffix='.txt')


def to_print_txt(*args, file_path=None, file_name=None, mode='a'):
    """
    将 print 数据, 写入到 print_txt 文件
    文件按照 日期自动创建
    例如: print_txt/2020-01-01.txt
    """
    file_path = __THREAD_LOCAL_INDEX_DATA.to_print_txt = file_path or getattr(__THREAD_LOCAL_INDEX_DATA, 'to_print_txt', None)
    to_txt(data_list=[to_print(*args)],
           file_name=datetime.today().strftime('%Y-%m-%d') if file_name is None else file_name,
           file_path=str(file_path if file_path is not None else 'to_print_txt'),
           mode=mode,
           fixed_name=True,
           suffix='.txt')


def to_log_file(*args, file_path=None, file_name=None, time_prefix=True, mode='a'):
    """
    将 log 数据, 写入到 log_file 文件
    文件按照 日期自动创建
    例如: log_file/2020-01-01.log
    """
    file_path = __THREAD_LOCAL_INDEX_DATA.to_log_file = file_path or getattr(__THREAD_LOCAL_INDEX_DATA, 'to_log_file', None)
    to_txt(data_list=[to_log(*args, time_prefix=time_prefix)],
           file_name=datetime.today().strftime('%Y-%m-%d') if file_name is None else file_name,
           file_path=str(file_path if file_path is not None else 'to_log_file'),
           fixed_name=True,
           mode=mode,
           suffix='.log')


def to_log_txt(*args, file_path=None, file_name=None, time_prefix=True, mode='a'):
    """
    将 log 数据, 写入到 log_txt 文件夹中
    文件按照 日期自动创建
    例如: log_txt/2020-01-01.txt
    """
    file_path = __THREAD_LOCAL_INDEX_DATA.to_log_txt = file_path or getattr(__THREAD_LOCAL_INDEX_DATA, 'to_log_txt', None)
    to_txt(data_list=[to_log(*args, time_prefix=time_prefix)],
           file_name=datetime.today().strftime('%Y-%m-%d') if file_name is None else file_name,
           file_path=str(file_path if file_path is not None else 'to_log_txt'),
           mode=mode,
           fixed_name=True,
           suffix='.txt')
