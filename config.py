import argparse
import os
from prettytable import PrettyTable

class Config:
    # 默认配置信息，包括新增的 max_workers
    DEFAULT_CONFIG = {
        'max_concurrency': 5,
        'max_workers': os.cpu_count(),
        'doc_paths': [],
        'target_levels': [3],
        'logger_level': 'DEBUG',
    }

    @staticmethod
    def parse_command_line_args():
        parser = argparse.ArgumentParser(description='Document Processor Configuration')
        parser.add_argument('-m', '--max-concurrency', type=int, help='Maximum number of coroutines in a single process')
        parser.add_argument('-w', '--max-workers', type=int, help='Maximum number of processes in the pool')
        parser.add_argument('-t', '--target-levels', type=int, nargs='+', help='Target levels to process')
        parser.add_argument('-l', '--logger-level', type=str, help='Logging level (e.g., DEBUG, INFO, WARNING)')
        parser.add_argument('doc_paths', nargs='+', help='File paths of the documents to be processed')

        args = parser.parse_args()

        return {
            'max_concurrency': args.max_concurrency if args.max_concurrency else Config.DEFAULT_CONFIG['max_concurrency'],
            'max_workers': args.max_workers if args.max_workers else Config.DEFAULT_CONFIG['max_workers'],
            'doc_paths': args.doc_paths,
            'target_levels': args.target_levels if args.target_levels else Config.DEFAULT_CONFIG['target_levels'],
            'logger_level': args.logger_level if args.logger_level else Config.DEFAULT_CONFIG['logger_level'],
        }

    @staticmethod
    def get(key, default=None):
        config = Config.parse_command_line_args()
        return config.get(key, Config.DEFAULT_CONFIG.get(key, default))

    @staticmethod
    def print_current_config():
        config = Config.parse_command_line_args()
        table = PrettyTable()
        table.field_names = ['Config Key', 'Value']  # 定义表格列名
        table.align['Config Key'] = 'l'  # 左对齐Config Key列
        table.align['Value'] = 'l'  # 左对齐Value列

        for key, value in config.items():
            table.add_row([key, value])  # 为每个配置项添加一行

        print(table)  # 打印表格
