import os
from difflib import SequenceMatcher


def read_file(filepath):
    """从给定路径读取文件内容"""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None


def calculate_similarity(text1, text2):
    """计算两段文本的相似度"""
    matcher = SequenceMatcher(None, text1, text2)
    return matcher.ratio()


def main(directory, reference_file):
    """主函数：比较文件夹中的所有文件与参考文件的相似度"""
    reference_text = read_file(reference_file)
    if reference_text is None:
        print("无法读取参考文件，查重无法进行。")
        return

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if filepath != reference_file and filepath.endswith('.txt'):  # 避免自我比较
            other_text = read_file(filepath)
            if other_text:
                similarity = calculate_similarity(reference_text, other_text) * 100
                print(f'文件 "{filename}" 与参考文件的相似度为：{similarity:.2f}%')


# 文件夹路径和参考文件
directory = 'D:\\作业\\软件工程\\zhiyou\\测试文本' #使用双反斜杠阻止报错
reference_file = 'D:\\作业\\软件工程\\zhiyou\\测试文本\\orig.txt'
main(directory, reference_file)