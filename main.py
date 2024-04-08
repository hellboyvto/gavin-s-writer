# main.py
import os
import concurrent.futures
from document import Document
from parser import Parser
from render import Render
from config import Config
from logger import get_logger

def process_documents(doc_path, output_path, target_levels, max_concurrency):
    try:
        doc = Document(file_path=doc_path)
        parser = Parser(doc)
        parser.parse()  # 注意这里不再需要传递文件路径参数
        #doc.print_tree(target_levels=target_levels)
        renderer = Render(doc, max_concurrency)
        renderer.render(output_path)
    except Exception as e:
        logger.error(f"Error processing {doc_path}: {str(e)}")

def main():
    # 使用Config类直接获取配置
    max_concurrency = Config.get('max_concurrency')
    doc_paths = Config.get('doc_paths')
    target_levels = Config.get('target_levels')
    logger_level = Config.get('logger_level')

    logger = get_logger(__name__)
    logger.setLevel(logger_level)

    output_paths = [doc_path.replace('.md', '_out.md') for doc_path in doc_paths]

    with concurrent.futures.ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = [
            executor.submit(process_documents, doc_path, output_path, target_levels, max_concurrency)
            for doc_path, output_path in zip(doc_paths, output_paths)
        ]
        concurrent.futures.wait(futures)
        logger.info("All documents processed.")

if __name__ == "__main__":
    main()
