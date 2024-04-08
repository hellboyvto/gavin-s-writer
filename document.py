# document.py
from node import Node

class Document:
    def __init__(self, file_path=None, root=None):
        if file_path:
            self.root = Node("Document Root")
            self.file_path = file_path  # 保存文件路径
        else:
            assert root
            self.root = root

    def print_tree(self, node=None, target_levels=None, current_level=0):
        if node is None:
            node = self.root
        if target_levels is None:
            target_levels = []

        prefix = '  ' * current_level  # 根据节点深度增加缩进
        if node.title:
            print(f"{prefix}- {node.title}")

        if node.level in target_levels and node.content:
            content_indent = '  ' * (current_level + 1)
            print(f"{content_indent}Content: {node.content.strip()}")

        for child in node.children:
            self.print_tree(child, target_levels, current_level + 1)
