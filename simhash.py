import os
import hashlib

def hashfunc(x):
    """使用 MD5 哈希函数"""
    return int(hashlib.md5(x.encode('utf-8')).hexdigest(), 16)

def get_features(text):
    """提取特征：这里将文本简单拆分为单词"""
    words = text.split()
    return words

def simhash(features):
    """根据特征计算 SimHash 值"""
    v = [0]*128
    for f in features:
        h = hashfunc(f)
        for i in range(128):
            bitmask = 1 << i
            v[i] += 1 if h & bitmask else -1
    fingerprint = 0
    for i in range(128):
        if v[i] >= 0:
            fingerprint += 1 << i
    return fingerprint

def hamming_distance(x, y):
    """计算两个哈希值的汉明距离"""
    return bin(x ^ y).count('1')

def calculate_similarity(distance):
    """计算基于汉明距离的相似度百分比"""
    return (1 - distance / 128) * 100

def read_file(filepath):
    """从给定的路径读取文件内容"""
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()

def main(directory):
    # 读取原始文件
    orig_path = os.path.join(directory, 'orig.txt')
    orig_text = read_file(orig_path)
    orig_hash = simhash(get_features(orig_text))

    # 遍历目录下的所有文件
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if file_path != orig_path:  # 避免与自身比较
            text = read_file(file_path)
            current_hash = simhash(get_features(text))
            distance = hamming_distance(orig_hash, current_hash)
            similarity = calculate_similarity(distance)
            print(f'文件 "{filename}" 与原始文件的汉明距离: {distance}, 相似度: {similarity:.2f}%')

# 指定文件夹路径
directory = r'D:\作业\软件工程\zhiyou\测试文本'
main(directory)