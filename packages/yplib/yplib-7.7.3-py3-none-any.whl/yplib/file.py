from yplib import *


def get_file(file_path=None,
             path_prefix=None,
             prefix=None,
             path_contain=None,
             contain=None,
             path_suffix=None,
             suffix=None):
    """
    有关文件的操作
    查询指定文件夹下面的所有的文件信息, 也可以是指定的文件
    file_path     : 文件路径
    path_prefix   : 文件路径,以 prefix 开头
    prefix        : 文件名称,以 prefix 开头
    path_contain  : 文件路径,含有
    contain       : 文件名称,含有
    path_suffix   : 文件路径,以 suffix 结尾
    suffix        : 文件名称,以 suffix 结尾
    return list
    """
    if file_path is None:
        file_path = os.path.dirname(os.path.abspath('.'))
    list_data = []
    get_file_all(file_path, list_data, path_prefix, prefix, path_contain, contain, path_suffix, suffix)
    # 去一下重复的数据
    return list(set(list_data))


def get_folder(file_path=None, prefix=None, contain=None, suffix=None):
    """
    有关文件的操作, 只查询文件夹
    查询指定文件夹下面的所有的文件信息, 也可以是指定的文件
    param list
    return list
    """
    if file_path is None:
        file_path = os.path.dirname(os.path.abspath('.'))
    list_data = []
    get_folder_all(file_path, list_data, prefix, contain, suffix)
    # 去一下重复的数据
    return list(set(list_data))


# 是否包含指定的文件
def contain_file(file_path=None, prefix=None, contain=None, suffix=None):
    return len(get_file(file_path, prefix, contain, suffix)) > 0


def get_file_data_line(file_path=None, find_str='find_str', from_last=True):
    """
    在指定的文件夹中查找包含指定字符串的数据
    file_path : 文件路径
    find_str : 查找的字符串
    from_last : 是否从文件的最后开始查找
    """
    file_list = get_file(file_path)
    for one_file in file_list:
        one_list = to_list(one_file)
        index = 0
        if from_last:
            index = len(one_list) - 1
        while -1 < index < len(one_list):
            one_line = one_list[index]
            if from_last:
                index -= 1
            else:
                index += 1
            if one_line.find(find_str) > -1:
                return one_line
    return None


# 查询指定文件夹下面的所有的文件信息, 也可以是指定的文件
def get_file_all(file_path,
                 list_data,
                 path_prefix=None,
                 prefix=None,
                 path_contain=None,
                 contain=None,
                 path_suffix=None,
                 suffix=None):
    if os.path.isdir(file_path):
        for root, dir_names, file_names in os.walk(file_path):
            for file_name in file_names:
                if (get_file_check(os.path.join(root, file_name), path_prefix, path_contain, path_suffix)
                        and get_file_check(file_name, prefix, contain, suffix)):
                    list_data.append(os.path.join(root, file_name))
            for dir_name in dir_names:
                get_file_all(os.path.join(root, dir_name), list_data, path_prefix, prefix, path_contain, contain, path_suffix, suffix)
    elif (get_file_check(file_path, prefix, contain, suffix)
          and get_file_check(file_path, path_prefix, path_contain, path_suffix)):
        list_data.append(file_path)


# 查询指定文件夹下面的所有的文件信息, 也可以是指定的文件
def get_folder_all(file_path, list_data, prefix=None, contain=None, suffix=None):
    if os.path.isdir(file_path):
        for root, dir_names, file_names in os.walk(file_path):
            for dir_name in dir_names:
                dir_name_path = os.path.join(root, dir_name)
                if get_file_check(dir_name_path, prefix, contain, suffix):
                    list_data.append(dir_name_path)
                else:
                    get_folder_all(dir_name_path, list_data, prefix, contain, suffix)


def get_file_check(
        name=None,
        prefix=None,
        contain=None,
        suffix=None):
    """
    检查文件是否符合要求
    prefix  : 前缀
    contain : 包含这个字符
    suffix  : 后缀
    """
    if name is None or name == '':
        return False
    p = True
    c = True
    s = True
    if prefix is not None:
        p = name.startswith(prefix)
    if contain is not None:
        c = name.find(contain) > -1
    if suffix is not None:
        s = name.endswith(suffix)
    return p and c and s


def find_file_by_content(file_path='', contain_txt=None, prefix=None, contain=None, suffix=None):
    """
    检查文件内容是否包含指定的字符串
    慎用,否则, 执行时间可能比较长
    """
    list_file = get_file(file_path, prefix, contain, suffix)
    if len(list_file) == 0:
        to_log(f'no_matched_file : {file_path} , {contain_txt} , {prefix} , {contain} , {suffix}')
        return False
    if contain_txt is None:
        to_log(list_file)
        return True
    for one_file in list_file:
        try:
            text_file = open(one_file, 'r', encoding='utf-8')
            for line in text_file.readlines():
                if line.find(contain_txt) > -1:
                    if line.endswith('\n'):
                        line = line[0:-1]
                    to_log(one_file, line)
        except Exception as e:
            to_log(one_file, e)
            continue


def to_list(file_name='a.txt',
            sep=None,
            sep_line=None,
            sep_line_contain=None,
            sep_line_prefix=None,
            sep_line_suffix=None,
            sep_all=None,
            ignore_start_with=None,
            ignore_end_with=None,
            start_index=None,
            start_line=None,
            end_index=None,
            end_line=None,
            count=None,
            sheet_index=1,
            column_index=None,
            column_date=None,
            column_datetime=None):
    """
    当读取 txt 之类的文件的时候
    将 txt 文件读取到 list 中, 每一行自动过滤掉行前行后的特殊字符
    sep             : 是否对每一行进行分割,如果存在这个字段,就分割
    sep_all         : 将文件转化成一个字符串,然后对这个字符串,再次总体分割
    start_index     : 从这个地方开始读取,从1开始标号 , 包含这一行
    start_line      : 从这个地方开始读取,从第一行开始找到这个字符串开始标记 , 包含这一行
    end_index       : 读取到这个地方结束,从1开始标号 , 不包含这一行
    end_line        : 读取到这个地方结束,从第一行开始找到这个字符串开始标记 , 不包含这一行
    count           : 读取指定的行数
    ##############################################
    当读取 excel 之类的文件的时候
    将 excel 文件读取到 list 中, 可以指定 sheet, 也可以指定列 column_index(列) ,自动过滤掉每个单元格前后的特殊字符
    sheet           : 从 1 开始编号,
    column_index    : 从 1 开始编号, 指定列
    column_index    : 如果是指定值, 这个时候返回的是一个 list, 没有嵌套 list
    column_index    : 如果是 '1,2,3,4'   [1,2,3,4], 返回的是一个嵌套 list[list]
    column_date     : 指定日期格式的列,规则与 column_index 一样
    column_datetime : 指定日期格式的列,规则与 column_index 一样
    返回的数据一定是一个 list
    """
    if file_name.endswith('.xls') or file_name.endswith('.xlsx'):
        return to_list_from_excel(file_name=file_name,
                                  sheet_index=sheet_index,
                                  column_index=column_index,
                                  column_date=column_date,
                                  column_datetime=column_datetime)
    return to_list_from_txt(file_name=file_name,
                            sep=sep,
                            sep_line=sep_line,
                            sep_line_contain=sep_line_contain,
                            sep_line_prefix=sep_line_prefix,
                            sep_line_suffix=sep_line_suffix,
                            sep_all=sep_all,
                            ignore_start_with=ignore_start_with,
                            ignore_end_with=ignore_end_with,
                            start_index=start_index,
                            start_line=start_line,
                            end_index=end_index,
                            end_line=end_line,
                            count=count)


def to_list_from_excel(file_name='a.xls',
                       sheet_index=1,
                       column_index=None,
                       column_date=None,
                       column_datetime=None):
    """
    当读取 excel 之类的文件的时候
    将 excel 文件读取到 list 中, 可以指定 sheet, 也可以指定列 column_index(列) ,自动过滤掉每个单元格前后的特殊字符
    sheet_index     : 从 1 开始编号,
    column_index    : 从 1 开始编号, 指定列, 如果是指定值是一个, 这个时候返回的是一个 list, 没有嵌套 list
                       如果是 '1,2,3,4'   [1,2,3,4], 返回的是一个嵌套 list[list]
    column_date     : 指定日期格式的列,规则与 column_index 一样
    column_datetime : 指定日期格式的列,规则与 column_index 一样
    """
    if file_is_empty(file_name):
        return []
    data_list = list()
    # excel 表格解析成 list 数据
    list_index = []
    for one_index in [column_index, column_date, column_datetime]:
        list_index_one = None
        if one_index is not None:
            list_index_one = []
            if isinstance(one_index, int):
                list_index_one.append(one_index)
            if isinstance(one_index, str):
                i_list = one_index.split(',')
                for i in i_list:
                    list_index_one.append(int(i))
            if isinstance(one_index, list):
                for i in one_index:
                    list_index_one.append(int(i))
        list_index.append(list_index_one)
    list_all = []
    for one_list in list_index:
        if one_list is not None:
            for o in one_list:
                list_all.append(o)
    if len(list_all) > 0 and list_index[0] is not None:
        list_index[0] = list_all
    # 是否是单 list 类型的数据
    list_only_one = False
    if list_index[0] is not None and len(list_index[0]) == 1:
        list_only_one = True
    # 是 xls 格式
    if file_name.endswith('.xls'):
        book = xlrd.open_workbook(file_name)  # 打开一个excel
        sheet = book.sheet_by_index(sheet_index - 1)  # 根据顺序获取sheet
        for i in range(sheet.nrows):  # 0 1 2 3 4 5
            rows = sheet.row_values(i)
            row_data = []
            for j in range(len(rows)):
                cell_data = str(rows[j]).strip()
                is_date = False
                is_datetime = False
                # 日期格式的列
                if list_index[1] is not None and j + 1 in list_index[1]:
                    cell_data = to_date(xlrd.xldate_as_datetime(to_int(rows[j]), 0))
                    is_date = True
                    row_data.append(cell_data)
                    if list_only_one:
                        row_data = cell_data
                # 日期时间格式的列
                if not is_date and list_index[2] is not None and j + 1 in list_index[2]:
                    cell_data = to_datetime(xlrd.xldate_as_datetime(to_int(rows[j]), 0))
                    is_datetime = True
                    row_data.append(cell_data)
                    if list_only_one:
                        row_data = cell_data
                # 指定需要的列
                if not is_date and not is_datetime:
                    if list_index[0] is None:
                        row_data.append(cell_data)
                    else:
                        # 指定需要的列
                        if j + 1 in list_index[0]:
                            row_data.append(cell_data)
                            if list_only_one:
                                row_data = cell_data
            data_list.append(row_data)
    # 是 xlsx 格式
    if file_name.endswith('.xlsx'):
        wb = openpyxl.load_workbook(filename=file_name, read_only=True)
        ws = wb[wb.sheetnames[sheet_index - 1]]
        for rows in ws.rows:
            row_data = []
            for j in range(len(rows)):
                cell_data = str(rows[j].value).strip()
                is_date = False
                is_datetime = False
                # 日期格式的列
                if list_index[1] is not None and j + 1 in list_index[1]:
                    cell_data = to_date(cell_data)
                    is_date = True
                    row_data.append(cell_data)
                    if list_only_one:
                        row_data = cell_data
                # 日期时间格式的列
                if not is_date and list_index[2] is not None and j + 1 in list_index[2]:
                    cell_data = to_datetime(cell_data)
                    is_datetime = True
                    row_data.append(cell_data)
                    if list_only_one:
                        row_data = cell_data
                # 指定需要的列
                if not is_date and not is_datetime:
                    if list_index[0] is None:
                        row_data.append(cell_data)
                    else:
                        # 指定需要的列
                        if j + 1 in list_index[0]:
                            row_data.append(cell_data)
                            if list_only_one:
                                row_data = cell_data
            data_list.append(row_data)
    return data_list


def to_list_from_txt_with_blank_line(file_name='a.txt'):
    """
    将一个文件中以空行作为分隔符,
    组成一个 list(list) 数据
    多行空行,自动合并到一行空行
    """
    return to_list_from_txt(file_name, sep_line='')


def to_list_list(data_list=[], count=10):
    """
    将 list 切分成 list(list)
    组成一个 list(list) 数据
    多行空行,自动合并到一行空行
    """
    r_list = []
    o_list = []
    c = 0
    for i in range(len(data_list)):
        o_list.append(data_list[i])
        c += 1
        if c == count:
            r_list.append(o_list)
            o_list = []
            c = 0
    if len(o_list):
        r_list.append(o_list)
    return r_list


def to_list_json_from_txt(file_name='a.txt',
                          start_index=None,
                          start_line=None,
                          end_index=None,
                          end_line=None,
                          count=None):
    """
    将一个文件中的数据按照行来区分,
    会自动过滤掉空格行,
    组成一个 list(json) 数据
    """
    return to_list_from_txt(file_name,
                            start_index=start_index,
                            start_line=start_line,
                            end_index=end_index,
                            end_line=end_line,
                            count=count,
                            line_json=True)


# 将多个文件 读取成 list
def to_list_from_txt_list(file_list=[]):
    data_list = []
    for a in file_list:
        data_list.extend(to_list_from_txt(file_name=a))
    return data_list


def to_list_from_txt(file_name='a.txt',
                     sep=None,
                     sep_line=None,
                     sep_line_contain=None,
                     sep_line_prefix=None,
                     sep_line_suffix=None,
                     sep_is_front=True,
                     sep_all=None,
                     ignore_start_with=None,
                     ignore_end_with=None,
                     line_join=None,
                     line_json=None,
                     start_index=None,
                     start_line=None,
                     end_index=None,
                     end_line=None,
                     count=None):
    """
    将 txt 文件转化成 list 的方法
    当读取 txt 之类的文件的时候
    将 txt 文件读取到 list 中, 每一行自动过滤掉行前行后的特殊字符
    sep               : 对每一行进行分割,将 list(str) 转化为 list(list(str)), 或者将 list(list(str)) 转化为 list(list(list(str)))
    sep_line          : 这一行是一个分隔符, 分隔符与这行一样, 将 list(str) 转化为 list(list(str))
    sep_line_contain  : 这一行是一个分隔符,包含这个行分隔符的做分割, 将 list(str) 转化为 list(list(str))
    sep_line_prefix   : 这一行是一个分隔符,以这个分隔符作为前缀的, 将 list(str) 转化为 list(list(str))
    sep_line_suffix   : 这一行是一个分隔符,以这个分隔符作为后缀的, 将 list(str) 转化为 list(list(str))
    sep_is_front      : 这一行，分割行，是包含到前面，还是包含到
    sep_all           : 将文件转化成一个字符串,然后对这个字符串,再次总体分割 将 list(str) 转化为 str , 然后再次转化成 list(str)
    ignore_start_with : 忽略以这个为开头的行
    ignore_end_with   : 忽略以这个为结尾的行
    line_join         : 将 list(list(str)) 转化成 list(str) 类型的数据
    line_json         : 将 list(str) 转化成 list(json) 类型的数据, 会自动过滤掉空格行
    start_index       : 从这个地方开始读取,从1开始标号 , 包含这一行
    start_line        : 从这个地方开始读取,从第一行开始找到这个字符串开始标记 , 包含这一行
    end_index         : 读取到这个地方结束,从1开始标号 , 不包含这一行
    end_line          : 读取到这个地方结束,从第一行开始找到这个字符串开始标记 , 不包含这一行
    count             : 读取指定的行数
    """
    if file_is_empty(file_name=file_name):
        return []
    data_list = []
    # 普通文件的解析
    d_list = open(file_name, 'r', encoding='utf-8').readlines()
    # 数量
    c = 0
    start_flag = None
    end_flag = None
    if start_line is not None:
        start_flag = False
    if end_line is not None:
        end_flag = False
    for i in range(len(d_list)):
        line = d_list[i].strip()
        # 判断开始位置
        if start_index is not None and i + 1 < to_int(start_index):
            continue
        # 判断结束位置
        if end_index is not None and i + 1 >= to_int(end_index):
            continue
        # 判断数量
        if count is not None and c >= to_int(count):
            continue
        # 开始标记位
        if start_flag is not None and not start_flag and line.find(start_line) > -1:
            start_flag = True
        # 开始标记位
        if end_flag is not None and not end_flag and line.find(end_line) > -1:
            end_flag = True
        if start_flag is not None and not start_flag:
            # 有开始标记位参数,并且,还没有走到开始标记位
            continue
        elif end_flag is not None and end_flag:
            # 有结束标记位参数,并且,已经走到了结束标记位
            continue
        c += 1
        can_add = True
        if ignore_start_with is not None:
            if isinstance(ignore_start_with, list) or isinstance(ignore_start_with, set):
                for ss in ignore_start_with:
                    if line.startswith(str(ss)):
                        can_add = False
            elif isinstance(ignore_start_with, str):
                if line.startswith(str(ignore_start_with)):
                    can_add = False
        if ignore_end_with is not None:
            if isinstance(ignore_end_with, list) or isinstance(ignore_end_with, set):
                for ss in ignore_end_with:
                    if line.endswith(str(ss)):
                        can_add = False
            elif isinstance(ignore_end_with, str):
                if line.endswith(str(ignore_end_with)):
                    can_add = False
        if can_add:
            data_list.append(line)
    if sep_all is not None:
        # 全部划分, 重新分割成 list(str)
        data_list = ''.join(data_list).split(str(sep_all))
    # 有行分隔符, 将会把 list(str) 转化成 list(list)
    if len(list(filter(lambda x: x is not None, [sep_line, sep_line_prefix, sep_line_contain, sep_line_suffix]))):
        # 当是这种情况的时候,返回的数据结果
        r_list = []
        # 数据中的一行 list 数据
        one_list = []
        for d_o in data_list:
            # 过滤掉空行,无效行
            if len(d_o.strip()) and sep_is_front:
                one_list.append(d_o)
            # 这一行, 等于 sep_line
            if ((sep_line is not None and d_o == sep_line) or
                    # 这一行, 包含 sep_line_contain
                    (sep_line_contain is not None and d_o.find(sep_line_contain) != -1) or
                    # 这一行, 是否是以 sep_line_prefix 开头
                    (sep_line_prefix is not None and d_o.startswith(sep_line_prefix)) or
                    # 这一行, 是否是以 sep_line_suffix 结尾
                    (sep_line_suffix is not None and d_o.endswith(sep_line_suffix))):
                if len(one_list):
                    r_list.append(one_list)
                    one_list = []
            if len(d_o.strip()) and not sep_is_front:
                one_list.append(d_o)
        # 最后的一条数据,兼容一下
        if len(one_list):
            r_list.append(one_list)
        data_list = r_list
    # 对这个 list 进行行内再次分割
    if sep is not None:
        r_list = []
        for line in data_list:
            # list(str) 情况
            if isinstance(line, str):
                r_list.append(line.split(str(sep)))
            # list(list) 情况
            elif isinstance(line, list):
                a_list = []
                for o_line in line:
                    a_list.append(o_line.split(str(sep)))
                r_list.append(a_list)
        data_list = r_list
    # data_list 中的每一个元素都转化成 str
    if line_join is not None:
        data_list = list(map(lambda x: str(line_join).join(x), data_list))
    # data_list 中的每一个元素都转化成 先转化成str, 然后再转化成json
    if line_json is not None and line_json:
        data_list = list(map(lambda x:
                             json.loads(str('' if line_join is None else line_join).join(x)),
                             list(filter(lambda x: x is not None and len(str(x)), data_list))
                             )
                         )
    return data_list


# 读取文件中的数据,返回一个 str
def to_str_from_file(file_name='a.txt',
                     str_join=' ',
                     ignore_start_with=None,
                     ignore_end_with=None,
                     start_index=None,
                     start_line=None,
                     end_index=None,
                     end_line=None,
                     count=None):
    return to_data_from_file(file_name=file_name,
                             ignore_start_with=ignore_start_with,
                             ignore_end_with=ignore_end_with,
                             str_join=str_join,
                             start_index=start_index,
                             start_line=start_line,
                             end_index=end_index,
                             end_line=end_line,
                             count=count,
                             r_str=True)


# 读取文件中的数据,返回一个 json
def to_json_from_file(file_name='a.txt',
                      start_index=None,
                      start_line=None,
                      end_index=None,
                      end_line=None,
                      count=None):
    return to_data_from_file(file_name=file_name,
                             start_index=start_index,
                             start_line=start_line,
                             end_index=end_index,
                             end_line=end_line,
                             count=count,
                             r_json=True)


def to_data_from_file(file_name='a.txt',
                      sep=None,
                      sep_line=None,
                      sep_all=None,
                      ignore_start_with=None,
                      ignore_end_with=None,
                      start_index=None,
                      start_line=None,
                      end_index=None,
                      end_line=None,
                      count=None,
                      sheet_index=1,
                      column_index=None,
                      column_date=None,
                      column_datetime=None,
                      r_json=False,
                      str_join='',
                      r_str=False):
    """
    在 to_list 方法上再嵌套一层,
    r_str    : 返回的数据是否是一个 字符串, ''.join(list)
    str_join : 返回的数据是否是一个 字符串, str_join.join(list), 用 str_join 做连接
    r_json   : 返回的数据是否是一个 json 类型的数据
    """
    d = to_list(file_name=file_name,
                sep=sep,
                sep_line=sep_line,
                sep_all=sep_all,
                ignore_start_with=ignore_start_with,
                ignore_end_with=ignore_end_with,
                start_index=start_index,
                start_line=start_line,
                end_index=end_index,
                end_line=end_line,
                count=count,
                sheet_index=sheet_index,
                column_index=column_index,
                column_date=column_date,
                column_datetime=column_datetime)
    return str_join.join(d) if r_str else json.loads(str_join.join(d)) if r_json else d


# 将文件导出成excel格式的
def to_excel(data_list, file_name=None, file_path='excel'):
    if file_name is None:
        file_name = 'excel'
    file_name = str(file_name)
    while file_path.endswith('/'):
        file_path = file_path[0:-1]
    check_file(file_path)
    # 实例化对象excel对象
    excel_obj = openpyxl.Workbook()
    # excel 内第一个sheet工作表
    excel_obj_sheet = excel_obj[excel_obj.sheetnames[0]]
    # 给单元格赋值
    for one_data in data_list:
        s_list = []
        if isinstance(one_data, list) or isinstance(one_data, set):
            for one in one_data:
                if isinstance(one, dict) or isinstance(one, list):
                    s = json.dumps(one)
                else:
                    s = str(one)
                s_list.append(s)
            excel_obj_sheet.append(s_list)
        else:
            if can_use_json(one_data):
                s = json.dumps(one_data)
            else:
                s = str(one_data)
            excel_obj_sheet.append([s])

    # 文件保存
    excel_obj.save(file_path + '/' + get_file_name(file_name, '.xlsx', True))


def to_csv(data_list, file_name=None, file_path='csv'):
    """
    将文件导出成csv格式的
    data_list 格式
    data_list = [['Name', 'Age', 'Gender'],
                 ['Alice', 25, 'Female'],
                 ['Bob', 30, 'Male'],
                 ['Charlie', 35, 'Male']]
    data_list = [{
          "a": 1,
          "b": 2,
      },{
          "a": 1,
          "b": 2,
    }]
    file_name = 'data'
    """
    if file_name is None:
        file_name = 'csv'
    file_name = get_file_name(file_name, '.csv', True)
    while file_path.endswith('/'):
        file_path = file_path[0:-1]
    check_file(file_path)
    d_list = []
    if isinstance(data_list, tuple):
        d_list = list(data_list)
    else:
        if len(data_list) and (isinstance(data_list[0], dict) or isinstance(data_list[0], tuple)):
            title_list = []
            for key in data_list[0]:
                title_list.append(key)
            d_list.append(title_list)
            for one_data in data_list:
                one_list = []
                for k in title_list:
                    one_list.append(one_data[k])
                d_list.append(one_list)
        else:
            d_list = data_list
    with open(file_path + '/' + file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(d_list)

# print(get_file_data_line(r'D:\notepad_file\202306\fasdfsadfaf.txt', 'payout', from_last=False))

# file_all = get_file(r'C:\Users\yang\Desktop\ticket\no.use', path_contain='03')
#
# for one_file in file_all:
#     print(one_file)

# get_file_data_line(r'D:\notepad_file\202306', 'a')
# get_file_by_content(r'D:\notepad_file\202306', 'a')
# print(get_file(r'D:\notepad_file\202306', 'a'))
# print(get_file(r'D:\notepad_file\202306'))
# print(get_file())
# print(os.path.abspath('.'))

#
# a_list = get_folder(r'D:\code\20220916\cjgeodatabase-java\platform', contain='build')
# for a in a_list:
#     os.remove(a)
#
# print(json.dumps(a_list))

# print('end')
