import os
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string

# 加载spaCy模型
nlp = spacy.load('en_core_web_sm')


def preprocess_text(text):
    """文本预处理：去除标点符号、转换为小写、去除停用词。"""
    doc = nlp(text.lower())  # 转换为小写并处理文本
    filtered_tokens = [token.text for token in doc if not token.is_punct and not token.is_stop]
    return ' '.join(filtered_tokens)


def load_texts_from_directory(directory_path):
    """加载指定目录中的所有文本文件。"""
    if not os.path.isdir(directory_path):
        raise NotADirectoryError(f"路径'{directory_path}'不是一个有效的目录。")

    texts = {}
    for filename in os.listdir(directory_path):
        if filename.endswith('.txt'):
            with open(os.path.join(directory_path, filename), 'r', encoding='utf-8') as file:
                texts[filename] = file.read()
    return texts


def calculate_similarity(original_text, other_texts):
    """计算原文与其他文本的余弦相似度。"""
    vectorizer = TfidfVectorizer()  # 使用默认设置，预处理在spaCy中完成
    original_text = preprocess_text(original_text)
    other_texts = [preprocess_text(text) for text in other_texts]

    texts = [original_text] + other_texts
    tfidf_matrix = vectorizer.fit_transform(texts)

    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])

    return cosine_sim[0]


def main(directory_path, original_filename):
    """主函数：加载文本、计算相似度并输出结果。"""
    texts = load_texts_from_directory(directory_path)

    if original_filename not in texts:
        raise ValueError(f"原文文件'{original_filename}'不存在于目录'{directory_path}'中。")

    original_text = texts[original_filename]
    other_texts = [texts[filename] for filename in texts if filename != original_filename]

    similarities = calculate_similarity(original_text, other_texts)

    # 输出结果
    for filename, similarity in zip(texts.keys(), similarities):
        if filename != original_filename:
            print(f"'{filename}' 与原文的相似度为: {similarity:.4f}")


if __name__ == "__main__":
    # 指定目录和原文文件名
    directory_path = 'D:/作业/软件工程/3121002717/测试文本/'  # 替换为你的目录路径
    original_filename = 'orig.txt'  # 替换为原文文件名

    main(directory_path, original_filename)