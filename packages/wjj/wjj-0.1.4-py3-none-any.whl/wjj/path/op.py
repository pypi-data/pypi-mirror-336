import os


def find_files(file_path, suffix=None, ffilter=None):
    """
    遍历目录及其子目录，返回符合条件的文件路径集合

    :param file_path: 要遍历的根目录路径
    :param suffix: 文件后缀过滤条件，支持字符串或列表类型（如 ".py" 或 [".jpg", ".png"]）
    :param ffilter: 自定义过滤函数，接收文件路径参数，返回布尔值
    :return: 符合条件文件的完整路径列表
    """
    file_list = []

    for cur_dir, dirs, files in os.walk(file_path):
        for file in files:
            full_path = os.path.normpath(os.path.join(cur_dir, file))

            # 后缀过滤逻辑
            if suffix:
                file_ext = os.path.splitext(file)[1].lower()
                if isinstance(suffix, str) and file_ext != suffix.lower():
                    continue
                if isinstance(suffix, (list, tuple)) and file_ext not in [e.lower() for e in suffix]:
                    continue

            # 映射函数过滤
            if ffilter and not callable(ffilter):
                raise TypeError("ffilter 必须是可调用函数")
            if ffilter and not ffilter(full_path):
                continue

            file_list.append(full_path)

    return file_list


def shortName(path):
    normalized_path = os.path.normpath(path)
    base_name = os.path.basename(normalized_path)
    return os.path.splitext(base_name)[0]


def path_to_str(path):  # 这个也可以集成函数
    # 先取得文件名路径
    normpath = os.path.normpath(path)  # 转义为通用路径格式
    filepath, _ = os.path.split(normpath)
    Separator = os.sep  # os.sep根据你的平台自动使用分隔符
    part = filepath.split(Separator)  # 字符串根据分隔符分割得到列表
    pathallpart = "-".join(part)  # 第一个往往是.，我们用的都是相对路径所以要去掉
    return pathallpart
