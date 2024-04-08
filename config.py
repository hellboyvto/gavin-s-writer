# config.py
class Config:
    # 所有配置信息都直接以字典形式保存
    CONFIG = {
        'max_concurrency': 1,
        'doc_paths': ['test1.md', 'test2.md'],
        'target_levels': [3],
        'logger_level': 'DEBUG',
    }

    @staticmethod
    def get(key, default=None):
        return Config.CONFIG.get(key, default)
