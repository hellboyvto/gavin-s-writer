# node.py
class Node:
    def __init__(self, title=None, content=None, level=0):
        self.title = title
        self.content = content
        self.level = level
        self.parent = None
        self.children = []

    def add_child(self, node):
        self.children.append(node)
