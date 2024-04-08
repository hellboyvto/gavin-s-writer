# parser.py
import re
from node import Node
from document import Document

class Parser:
    def __init__(self, document):
        self.document = document
        self._parse()  # 初始化时自动调用_parse方法来解析文档

    def _parse(self):  # 将parse方法改为私有
        title_pattern = re.compile(r'^(#+)\s*(.*)')
        current_node = self.document.root
        with open(self.document.file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.rstrip()
                match = title_pattern.match(line)
                if match:
                    level = len(match.group(1))
                    title = match.group(2)
                    new_node = Node(title, level=level)
                    while current_node.level >= level:
                        current_node = current_node.parent
                    current_node.add_child(new_node)
                    new_node.parent = current_node
                    current_node = new_node
                else:
                    if current_node.content:
                        current_node.content += '\n' + line
                    else:
                        current_node.content = line

