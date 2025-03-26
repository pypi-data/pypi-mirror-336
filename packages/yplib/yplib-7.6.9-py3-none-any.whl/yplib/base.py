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


def check_file(file_name):
    r"""
    检查文件夹是否存在,不存在,就创建新的
    支持多级目录 , 例如: C:\Users\yangpu\Desktop\study\a\b\c\d\e\f
    """
    if file_name is None or file_name == '':
        return
    for sep in ['\\', '/']:
        f_n = file_name.split(sep)
        for i in range(1, len(f_n) + 1):
            # C:\Users\yangpu\Desktop\study\p.t
            p_n = sep.join(f_n[0:i])
            if not os.path.exists(p_n):
                os.mkdir(p_n)


def get_file_name(file_name, suffix='.txt', is_date=False):
    """
    获得文件名称
    按照  name_天小时分钟_秒毫秒随机数 的规则来生成
    """
    # %Y-%m-%d %H:%M:%S
    [year, month, day, hour, minute, second, ss] = datetime.today().strftime('%Y_%m_%d_%H_%M_%S_%f').split('_')
    s = year + month + day + '_' + hour + minute if is_date else month + day + '_' + hour + minute
    # 在 file_name 中, 检查是否有后缀
    if '.' in file_name:
        suffix = '.' + file_name.split('.')[-1]
        file_name = file_name[0:file_name.rfind('.')]
    return str(file_name) + '_' + s + '_' + second + random_str(length=4, start_str=27, end_str=52) + suffix


def to_txt(data_list,
           file_name='txt',
           file_path='txt',
           fixed_name=False,
           mode='a',
           suffix='.txt',
           sep_list='\t',
           file_name_is_date=False):
    r"""
    将 list 中的数据以 json 或者基本类型的形式写入到文件中
    data_list   : 数组数据, 也可以不是数组
    file_name   : 文件名 , 默认 txt
                  当文件名是 C:\Users\yangpu\Desktop\study\abc\d\e\f\a.sql 这种类型的时候, 可以直接创建文件夹,
                      会赋值 file_name=a,
                            file_path=C:\Users\yangpu\Desktop\study\abc\d\e\f,
                            fixed_name=True,
                            suffix=.sql
                  当文件名是 abc 的时候, 按照正常值,计算
    file_path   : 文件路径
    fixed_name  : 是否固定文件名
    suffix      : 文件后缀, 默认 .txt
    sep_list    : 当 data_list 是 list(list) 类型的时候 使用 sep_list 作为分割内部的分隔符,
                  默认使用 \t 作为分隔符, 如果为 None , 则按照 json 去处理这个 list
    """
    file_name = str(file_name)
    for sep in ['\\', '/']:
        f_n = file_name.split(sep)
        if len(f_n) > 1:
            file_name = f_n[-1]
            file_path = sep.join(f_n[0:-1])
            if '.' in file_name:
                suffix = '.' + file_name.split('.')[-1]
                file_name = file_name[0:file_name.rfind('.')]
                fixed_name = True

    # 检查路径 file_path
    while file_path.endswith('/'):
        file_path = file_path[0:-1]
    check_file(file_path)

    # 在 file_name 中, 检查是否有后缀
    if '.' in file_name:
        suffix = '.' + file_name.split('.')[-1]
        file_name = file_name[0:file_name.rfind('.')]

    # 生成 file_name
    if fixed_name:
        file_name = file_name + suffix
    else:
        file_name = get_file_name(file_name, suffix, is_date=file_name_is_date)
    # 文件路径
    file_name_path = file_name
    if file_path != '':
        file_name_path = file_path + '/' + file_name
    # 写入文件
    text_file = open(file_name_path, mode, encoding='utf-8')
    if isinstance(data_list, set):
        data_list = list(data_list)
    if not isinstance(data_list, list):
        text_file.write(to_str(data_list) + '\n')
    else:
        for one in data_list:
            if isinstance(one, (list, tuple, set)) and sep_list is not None:
                text_file.write(str(sep_list).join(list(map(lambda x: to_str(x), one))) + '\n')
            else:
                text_file.write(to_str(one) + '\n')
    text_file.close()
    return file_name_path


# 将 list 中的数据写入到固定的文件中,自己设置文件后缀
def to_txt_file(data_list, file_name=None, mode='a'):
    file_name = datetime.today().strftime('%Y%m%d_%H%M') if file_name is None else file_name
    return to_txt(data_list=data_list, file_name=file_name, file_path='txt', fixed_name=True, mode=mode)


# 将 list 中的数据写入到固定的文件中,自己设置文件后缀
def to_file(data_list, file_name=None, mode='a'):
    file_name = datetime.today().strftime('%Y%m%d_%H%M') if file_name is None else file_name
    suffix = '.txt'
    f = file_name
    for sep in ['\\', '/']:
        f_n = file_name.split(sep)
        if len(f_n) > 1:
            f = file_name
    if '.' in f:
        suffix = '.' + f.split('.')[-1]
        file_name = file_name.replace(suffix, '')
    return to_txt(data_list=data_list, file_name=file_name, file_path='file', suffix=suffix, fixed_name=True, mode=mode)
