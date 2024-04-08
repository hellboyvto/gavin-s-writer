import os
import concurrent.futures
from document import Document
from parser import Parser
from render import Render
from config import Config
from logger import get_logger

def process_documents(doc_path, output_path, target_levels, max_concurrency):
    try:
        # 在子进程内配置logger，确保其设置正确
        logger = get_logger(__name__)
        logger.setLevel("INFO")  # 或从配置中获取正确的日志级别
        
        doc = Document(file_path=doc_path)
        parser = Parser(doc)  # 这里初始化解析文档
        renderer = Render(doc, max_concurrency)
        
        renderer.render(output_path, target_levels)
        
        # 文档处理完成后，输出成功的日志信息
        logger.info(f"Document processing completed: {output_path}")
        
    except Exception as e:
        logger.error(f"Error processing {doc_path}: {str(e)}")

if __name__ == "__main__":
    config = Config.parse_command_line_args()
    max_concurrency = config['max_concurrency']
    doc_paths = config['doc_paths']
    target_levels = config['target_levels']
    logger_level = config['logger_level']
    max_workers = config['max_workers']
    # 打印当前配置情况
    Config.print_current_config()
    logger = get_logger(__name__)
    logger.setLevel(logger_level.upper())
    output_paths = [doc_path.replace('.md', '_out.md') for doc_path in doc_paths]

    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(process_documents, doc_path, output_path, target_levels, max_concurrency)
            for doc_path, output_path in zip(doc_paths, output_paths)
        ]
        concurrent.futures.wait(futures)
        logger.info("All documents processed.")
