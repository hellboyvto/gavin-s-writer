# render.py
import asyncio
from node import Node

class Render:
    def __init__(self, document, max_concurrency=1):
        self.document = document
        self.semaphore = asyncio.Semaphore(max_concurrency)  # 控制并发数量
    
    async def _process_node(self, node):
        async with self.semaphore:
            print(f"处理 {node.title} at level {node.level}")
            await asyncio.sleep(3)  # 模拟IO操作
            node.content = f"处理后的内容: {node.title}"
            
    async def async_process_node(self, node, target_levels=None):
        tasks = []
        if target_levels is None:
            target_levels = []
            
        queue = [node]
        while queue:
            node = queue.pop()
            if node.level in target_levels and node.content is not None:
                tasks.append(self._process_node(node))
            queue.extend(node.children)
            
        for first_done in asyncio.as_completed(tasks):
            await first_done

    def render(self, output_path):
        # 需要创建一个新的事件循环来异步处理节点
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        # 进行异步操作
        loop.run_until_complete(self.async_process_node(self.document.root, [3]))  # 假设我们只对level 3的节点进行处理
        loop.close()
        with open(output_path, 'w', encoding='utf-8') as file:
            for child in self.document.root.children:
                for node in self.iter_nodes(child):
                    if node.title:
                        file.write('#' * node.level + ' ' + node.title + '\n\n')
                    if node.content:
                        file.write(node.content.strip() + '\n\n')

    def iter_nodes(self, node):
        yield node
        for child in node.children:
            yield from self.iter_nodes(child)
