import unittest
import os
from unittest.mock import mock_open, patch, MagicMock
from Difflib import read_file, calculate_similarity, compare_files  # 确保正确导入你的模块

class TestFileSimilarity(unittest.TestCase):
    def setUp(self):
        # 设置参考文件和目录的路径
        self.directory = "D:\\作业\\软件工程\\zhiyou\\3121002717\\测试文本"
        self.reference_file = "D:\\作业\\软件工程\\zhiyou\\3121002717\\测试文本\\orig.txt"
        self.reference_content = "你好，世界"

    def test_read_file_success(self):
        # 创建一个模拟的open对象，里面有指定的内容
        m = mock_open(read_data='data')

        # 使用模拟对象替代'open'
        with patch('builtins.open', m):
            # 调用你的函数来读取文件
            result = read_file('filename.txt')

            # 进行断言或检查结果
            self.assertEqual(result, 'data')

    def test_read_file_failure(self):
        # 模拟文件读取失败
        with patch('builtins.open', side_effect=Exception("File not found")):
            content = read_file('nonexistent.txt')
        self.assertIsNone(content)

    def test_calculate_similarity_exact(self):
        # 测试完全相同的文本
        self.assertEqual(calculate_similarity("你好", "你好"), 1.0)

    def test_calculate_similarity_none(self):
        # 测试完全不同的文本
        self.assertEqual(calculate_similarity("你好", "世界"), 0.0)

        def test_compare_files(self):
            directory = 'dummy_directory'
            reference_text = 'Hello world!'
            reference_filepath = os.path.join(directory, 'reference.txt')
            files = ['file1.txt', 'file2.txt', 'reference.txt']

            # 使用 mock 模拟文件系统操作和 difflib 库的行为
            with patch('os.listdir', return_value=files), \
                    patch('os.path.join', side_effect=lambda x, y: os.path.join(x, y)), \
                    patch('os.path.isfile', return_value=True), \
                    patch('builtins.open', mock_open(read_data='Hello world! Different words here')):
                results = list(compare_files(directory, reference_text, reference_filepath, '.txt'))

            # 假设所有文件都与参考文本有相同程度的相似度（由于difflib计算）
            expected_results = [('file1.txt', 0.9230769230769231), ('file2.txt', 0.9230769230769231)]
            self.assertEqual(len(results), len(expected_results))
            for result, expected in zip(results, expected_results):
                self.assertEqual(result[0], expected[0])
                self.assertAlmostEqual(result[1], expected[1], places=4)

    if __name__ == '__main__':
        unittest.main()