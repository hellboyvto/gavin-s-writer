import re
import os
import asyncio
import concurrent.futures
from collections import deque

class Node:
    def __init__(self, title=None, content=None, level=0):
        self.title = title
        self.content = content
        self.level = level
        self.parent = None
        self.children = []

    def add_child(self, node):
        self.children.append(node)

class Document:
    def __init__(self, concurrency, file_path=None):
        self.root = Node("Document Root")
        self.semaphore = asyncio.Semaphore(concurrency)  # 控制并发数量
        if file_path:
            self.parse(file_path)

    def parse(self, src_path):
        title_pattern = re.compile(r'^(#+)\s*(.*)')
        current_node = self.root
        with open(src_path, 'r', encoding='utf-8') as file:
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

    def render(self, output_path):
        with open(output_path, 'w', encoding='utf-8') as file:
            for child in self.root.children:  # 从根节点的子节点开始迭代
                for node in self.iter_nodes(child):  # 为每个子节点及其子树调用iter_nodes
                    if node.title:  # 确保不处理空标题的节点
                        file.write('#' * node.level + ' ' + node.title + '\n\n')
                    if node.content:  # 确保节点有内容再写入
                        file.write(node.content.strip() + '\n\n')

    def iter_nodes(self, node):
        yield node
        for child in node.children:
            yield from self.iter_nodes(child)

    async def async_process_node(self, target_levels=None):
        if target_levels is None:
            target_levels = []

        tasks = []
        queue = deque([self.root])
        while queue:
            node = queue.pop()
            if node.level in target_levels and node.content is not None:
                tasks.append(self.process_node_with_semaphore(node))  # 使用控制并发的方式处理node
            queue.extendleft(node.children)

        for coro in asyncio.as_completed(tasks):
            await coro  # 这里，await 不会阻塞，因为它等待的是最先完成的任务

    async def process_node_with_semaphore(self, node):
        async with self.semaphore:  # 获取semaphore
            await self._process_node(node)

    async def _process_node(self, node):
        print(f"处理 {node.title} at level {node.level}")
        await asyncio.sleep(1)  # 模拟IO操作
        node.content = f"处理后的内容: {node.title}"

def process_documents(doc_path, output_path, target_levels, max_concurrency):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    doc = Document(concurrency=max_concurrency, file_path=doc_path)
    loop.run_until_complete(doc.async_process_node(target_levels=target_levels))
    doc.print_tree(target_levels=target_levels)
    doc.render(output_path)

if __name__ == "__main__":
    cpu_cores = os.cpu_count()  # 启动的进程数量
    max_concurrency = 3  # 每个进程中的协程数量
    doc_paths = ['test1.md', 'test2.md']  # 假设有多个文档待处理
    # 根据原文件名生成输出文件名
    output_paths = [doc_path.replace('.md', '_out.md') for doc_path in doc_paths]
    target_levels = [3]
    # 根据CPU核心数量设定ProcessPoolExecutor的最大进程数
    with concurrent.futures.ProcessPoolExecutor(max_workers=cpu_cores) as executor:
        futures = []
        for doc_path, output_path in zip(doc_paths, output_paths):
            futures.append(executor.submit(process_documents, doc_path, output_path, target_levels, max_concurrency))
        
        # 等待所有的任务完成
        concurrent.futures.wait(futures)

        # 可选：处理结果
        for future in futures:
            try:
                result = future.result()  # 获取结果，如果任务抛出了异常，这里会重新抛出
                # 处理结果...
            except Exception as e:
                # 处理异常...
                print(f"Task generated an exception: {e}")

