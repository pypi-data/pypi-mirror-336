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

__CONFIG_PATH = '.yp.config'

__CONFIG_PATH_BAK = '_yp.config'


def is_all_chinese(text):
    return bool(re.compile(r'^[\u4e00-\u9fff]+$').match(text))


def remove_chinese(text):
    return re.compile(r'[\u4e00-\u9fff]+').sub('', text)


def to_java_one(s):
    """
    将下划线命名转成驼峰命名
    例如 : user_id -> userId
    例如 : USER_ID -> userId
    例如 : gpsMaxMove_new -> gpsMaxMoveNew
    """
    if s is None or s == '':
        return s
    r = ''.join(list(map(lambda x: (x[0].upper() + x[1:]) if len(x) > 1 else x[0].upper(), str(s).split('_'))))
    return r[0].lower() + r[1:]


def to_java(s):
    if s is None or s == '':
        return s
    if isinstance(s, list) or isinstance(s, tuple) or isinstance(s, set):
        return list(map(lambda x: to_java_one(x), s))
    return to_java_one(s)


def to_java_more(*args):
    # 使用列表推导式进行过滤和映射
    r = [to_java(x) for x in args if x is not None]
    if not r:
        return None
    return tuple(r)


def to_underline_one(s):
    """
    将驼峰命名转成下划线命名
    例如 : userId -> user_id
    """
    if s == '' or s is None:
        return s
    return ''.join(list(map(lambda x: '_' + str(x).lower() if x.isupper() else x, str(s))))


def to_underline(s):
    if s == '' or s is None:
        return s
    if isinstance(s, list) or isinstance(s, tuple) or isinstance(s, set):
        return list(map(lambda x: to_underline_one(x), s))
    return to_underline_one(s)


def to_underline_more(*args):
    # 使用列表推导式进行过滤和映射
    r = [to_underline(x) for x in args if x is not None]

    if not r:
        return None
    return tuple(r)


# 是否能用 json
def can_use_json(data):
    if (isinstance(data, str)
            or isinstance(data, int)
            or isinstance(data, bytes)
            or isinstance(data, bool)
            or isinstance(data, complex)
            or isinstance(data, float)):
        return False
    try:
        json.dumps(data)
    except Exception:
        return False
    return True


# 文件是否存在
def file_is_empty(file_name=None):
    return file_name is None or file_name == '' or not os.path.exists(file_name)


# md5 算法
def do_md5(data='do_md5'):
    return hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()


# sha256 算法
def do_sha256(data='do_sha256'):
    h = hashlib.sha256()
    h.update(data.encode('utf-8'))
    return h.hexdigest()


# uuid 类型的随机数, 默认 32 位长度
def random_uuid(length=32):
    r = uuid.uuid4().hex
    while len(r) < length:
        r += uuid.uuid4().hex
    return r[0:length]


def random_str(length=64, start_str=1, end_str=62):
    """
    获得随机数
    length    ：随机数长度
    start_str ：随机数开始的字符的位置,从 1 开始, 包含start_str
    end_str   : 随机数结束的字符的位置, 不包含end_str
    默认的随机数是 : 数字+字母大小写
    """
    c_s = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_'
    r = ''
    start_str = max(1, start_str)
    end_str = min(len(c_s), end_str)
    while len(r) < length:
        r += c_s[random.Random().randint(start_str, end_str) - 1]
    return r


# 字母的随机数, 默认小写
def random_letter(length=10, is_upper=False):
    r = random_str(length=length, end_str=26)
    return r.upper() if is_upper else r


def random_int(length_or_start=10, end=None):
    """
    数字的随机数, 返回 int
    也可以返回指定范围的随机数据
    """
    if end is None:
        return int(random_int_str(length=length_or_start))
    return random.Random().randint(int(length_or_start), int(end) - 1)


# 数字的随机数, 返回 str
def random_int_str(length=10):
    return random_str(length=length, start_str=53, end_str=62)


# 去掉 str 中的 非数字字符, 然后, 再转化为 int
def to_int(s):
    if s is None or len(str(s)) == 0:
        return 0
    if isinstance(s, int):
        return s
    if isinstance(s, float):
        return int(s)
    s = re.sub(r'[^\d.]', '', str(s))
    try:
        if s.find('.') == -1:
            return int(s)
        return int(float(s))
    except ValueError:
        return 0


def to_float(s, precision=None):
    """
    去掉 str 中的 非数字字符, 然后, 再转化为 float
    precision , 小数部位的长度 , 多余的部分 直接去掉
    """
    if s is None or len(str(s)) == 0:
        return 0.0
    s = str(s)
    # s = ''.join(filter(lambda ch: ch in '0123456789.', str(s)))
    # @see https://www.runoob.com/python3/python3-reg-expressions.html
    s = re.sub(r'[^\d.]', '', str(s))
    if len(s) == 0:
        return 0.0
    if precision is None:
        return float(s)
    s1 = s.split('.')
    if len(s1) > 1:
        s = s1[0] + '.' + s1[1][:precision]
    else:
        s = s1[0]
    return float(s)


def to_datetime(s=None, r_str=False):
    """
    @see https://www.runoob.com/python3/python3-date-time.html
    将字符串 s 转化成 datetime
    """
    if s is None or s == '':
        return str(datetime.today()) if r_str else datetime.today()
    s = str(s).replace('T', ' ').replace('Z', ' ').strip()
    r = None
    date_time_sdf = '%Y-%m-%d %H:%M:%S'
    m_s = {
        "^\\d{4}$": "%Y",
        "^\\d{4}-\\d{1,2}$": "%Y-%m",
        "^\\d{4}-\\d{1,2}-\\d{1,2}$": "%Y-%m-%d",
        "^\\d{4}-\\d{1,2}-\\d{1,2} {1}\\d{1,2}$": "%Y-%m-%d %H",
        "^\\d{4}-\\d{1,2}-\\d{1,2} {1}\\d{1,2}:\\d{1,2}$": "%Y-%m-%d %H:%M",
        "^\\d{4}-\\d{1,2}-\\d{1,2} {1}\\d{1,2}:\\d{1,2}:\\d{1,2}$": date_time_sdf,
        "^\\d{4}-\\d{1,2}-\\d{1,2} {1}\\d{1,2}:\\d{1,2}:\\d{1,2}.\\d{1,9}$": date_time_sdf,
        "^\\d{4}-\\d{1,2}-\\d{1,2}T{1}\\d{1,2}:\\d{1,2}:\\d{1,2}$": date_time_sdf,
        "^\\d{4}-\\d{1,2}-\\d{1,2}T{1}\\d{1,2}:\\d{1,2}:\\d{1,2}.\\d{1,9}$": date_time_sdf,
    }
    for m in m_s:
        if re.match(m, s):
            st = s.split('.')[0]
            st = st.replace('T', ' ')
            r = datetime.strptime(st, m_s[m])
    if r is None and re.match("^\\d{1,13}$", s):
        s_int = int(s)
        if len(s) > 10:
            s_int = int(s_int / 1000)
        time_arr = time.localtime(s_int)
        time_str = time.strftime(date_time_sdf, time_arr)
        r = datetime.strptime(time_str, date_time_sdf)
    if r is None:
        r = datetime.today()
    return str(r) if r_str else r


# 将字符串 s 转化成 datetime, 然后再次转化成 str
def to_datetime_str(s=None):
    return to_datetime(s, r_str=True)


# 时间加减
def to_datetime_add(s=None, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
    return to_datetime(s) + timedelta(days=days, seconds=seconds, microseconds=microseconds,
                                      milliseconds=milliseconds, minutes=minutes, hours=hours,
                                      weeks=weeks)


# 将字符串 s 转化成 date 例如: 2021-02-03
def to_date(s=None):
    return str(to_datetime(s))[0:10]


def get_timestamp(s=None):
    return int(to_datetime(s).timestamp())


# 时间加减
def to_date_add(s=None, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
    return str(to_datetime_add(s=s, days=days, seconds=seconds, microseconds=microseconds,
                               milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks))[0:10]


# 转化成字符串
def to_str(data):
    return json.dumps(data, ensure_ascii=False) if can_use_json(data) else str(data)


def match_str(pattern, str_a=''):
    """
    匹配字符串
    可以参考 正则表达式的操作, 可以使用 chatgpt 帮忙写出这段代码
    @see https://www.runoob.com/python3/python3-reg-expressions.html
    # 示例用法
    # 输出：t_admin
    print(match_str(r'create TABLE (\\w+)', 'CREATE TABLE t_admin (id bigint(20) NOT NULL'))
    这里的 斜杠w 去掉一个斜杠
    """
    match = re.search(pattern, str_a, re.I)
    if match:
        return match.group(1)
    else:
        return None


def sort_by_json_key(data_obj, sep='&', join='=', join_list=','):
    """
    根据json的key排序,用于签名
    按照 key 排序, 按照 key=value 然后再 & 连接, 如果数据中有 list, 使用 , 连接 list 中的数据, 然后拼接成 str 返回
    sep       : 分隔符 , 默认 &
    join      : 连接符 , 默认 =
    join_list : list 数据 连接符 , 默认 ,
    """
    if isinstance(data_obj, list) or isinstance(data_obj, tuple) or isinstance(data_obj, set):
        return join_list.join(list(map(lambda x: f'{x}', data_obj)))
    if not isinstance(data_obj, dict):
        return str(data_obj)
    data_list = sorted(data_obj.items(), key=lambda x: x[0])
    r_l = []
    for one in data_list:
        value_one = one[1]
        if can_use_json(value_one):
            s = sort_by_json_key(data_obj=value_one, sep=sep, join=join, join_list=join_list)
        else:
            s = str(value_one)
        r_l.append(f'{one[0]}{join}{s}')
    return sep.join(r_l)


# 将数据写入到 config 中
def set_config_data(file_name='config', data=None):
    if data is None:
        data = {}
    set_data_in_user_home(file_name, data)


# 从 config 中获得 配置数据
def get_config_data(file_name='config'):
    # print('get_config_data', file_name)
    config_data = get_data_from_user_home(file_name)
    # print('get_data_from_user_home', config_data)
    if not config_data:
        config_data = get_data_from_path(file_name)
    # print('get_data_from_path', config_data)
    return config_data


# 在当前用户的主目录中, 获得指定文件的数据
def get_data_from_user_home(file_name='config'):
    return get_data_from_path(file_name, os.path.expanduser("~"))


# 将 data 数据,在当前用户的主目录中, 获得指定文件的数据
def set_data_in_user_home(file_name='config', data=None):
    if data is None:
        data = {}
    set_data_in_path(file_name, data, os.path.expanduser("~"))


# 在当前的目录中, 获得指定文件的数据
def get_data_from_path(file_name='config', file_path=None):
    data = get_data_from_path_detail(file_name, file_path, __CONFIG_PATH)
    return data if data else get_data_from_path_detail(file_name, file_path, __CONFIG_PATH_BAK)


def get_data_from_path_detail(file_name='config', file_path=None, path_name=__CONFIG_PATH):
    config_path = file_path + '/' + path_name if file_path else path_name
    # print('config_path_1', config_path)
    if not os.path.exists(config_path):
        # print('config_path_2', config_path)
        return {}
    file_path = config_path + '/' + file_name + '.json'
    # print('config_path_3', file_path)
    if not os.path.exists(file_path):
        return {}
    # print('to_json_from_file', file_path)
    return to_json_from_file(file_path)


# 在当前的目录中, 设置数据到指定路径下
def set_data_in_path(file_name='config', data=None, file_path=''):
    if data is None:
        data = {}
    config_path = file_path + '/' + __CONFIG_PATH
    if not os.path.exists(config_path):
        os.mkdir(config_path)
    file_path = config_path + '/' + file_name + '.json'
    text_file = open(file_path, 'w', encoding='utf-8')
    text_file.write(to_str(data))
    text_file.close()


# 执行命令
def exec_command(command=''):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"command executed error: {e}")


# 找到最新的 html 文件
def get_latest_file(file_path='html'):
    html_list = get_file(file_path=file_path)
    now_date = '_' + to_date()[0:4]
    html_name_list = []
    for html_one in html_list:
        html_name_list.append([html_one, html_one.split(now_date)[-1]])
    html_name_list.sort(key=lambda x: x[1])
    html_name = html_name_list[-1][0]
    return html_name
