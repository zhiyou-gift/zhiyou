import os
from difflib import SequenceMatcher
import cProfile

def read_file(filepath):
    """
    读取指定文件的内容。

    Args:
        filepath (str): 文件的完整路径。

    Returns:
        str: 文件内容，若读取失败则返回None。
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read().strip()  # 去除文件首尾的空白字符
    except Exception as e:
        print(f"Error reading {filepath}: {e}")  # 打印错误信息
        return None


def calculate_similarity(text1, text2):
    """
    计算两个文本之间的相似度百分比。

    Args:
        text1 (str): 第一个文本。
        text2 (str): 第二个文本。

    Returns:
        float: 两个文本的相似度，值为0到1之间。
    """
    return SequenceMatcher(None, text1, text2).ratio()


def compare_files(directory, reference_text, reference_filepath, file_extension=".txt"):
    """
    对指定目录下的所有文件与参考文本计算相似度，但跳过参考文件本身。

    Args:
        directory (str): 文件所在的目录。
        reference_text (str): 参考文本。
        reference_filepath (str): 参考文件的完整路径，用于排除自比较。
        file_extension (str): 需要比较的文件类型。

    Yields:
        tuple: 包含文件名和其相似度的元组。
    """
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if filepath == reference_filepath:
            continue  # 跳过参考文件本身的比较
        if filepath.endswith(file_extension) and os.path.isfile(filepath):
            other_text = read_file(filepath)
            if other_text:
                similarity = calculate_similarity(reference_text, other_text)
                yield filename, similarity  # 生成文件名和相似度


def main(directory, reference_file):
    """
    主函数：读取参考文件，并比较目录中其他文件的相似度，避免与参考文件自身比较。

    Args:
        directory (str): 存放文件的目录。
        reference_file (str): 参考文件路径。
    """
    reference_text = read_file(reference_file)
    if reference_text is None:
        print("无法读取参考文件，查重无法进行。")
        return

    # 输出文件与参考文本的相似度，排除与参考文件自身的比较
    for filename, similarity in compare_files(directory, reference_text, reference_file):
        print(f'文件 "{filename}" 的相似度为：{similarity * 100:.2f}%')


# 设置文件夹和参考文件的路径
directory = input("请输入文件存放的目录路径：") #'D:\\作业\\软件工程\\zhiyou\\测试文本'
reference_file = input("请输入参考文件的完整路径：") #'D:\\作业\\软件工程\\zhiyou\\测试文本\\orig.txt'
# 创建一个Profile对象，并运行主函数进行性能分析
profiler = cProfile.Profile()
profiler.enable()  # 开始性能分析
main(directory, reference_file) #调用主函数
profiler.disable()  # 结束性能分析
profiler.print_stats(sort='time')  # 打印分析结果，按运行时间排序

# ncalls：表示函数调用的次数；
#
# tottime：表示指定函数的总的运行时间，除掉函数中调用子函数的运行时间；
#
# percall：（第一个percall）等于tottime/ncalls；
#
# cumtime：表示该函数及其所有子函数的调用运行的时间，即函数开始调用到返回的时间；
#
# percall：（第二个percall）即函数运行一次的平均时间，等于cumtime/ncalls；
#
# filename:lineno(function)：每个函数调用的具体信息