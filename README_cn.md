# Gavin's Writer

## 简介
Gavin's Writer 是一个强大的文档处理工具，可用于文档的解析、渲染和内容加工，支持并行处理和日志记录。它能够根据用户设置的配置选项通过命令行参数来处理一系列文档。

## 功能

- **并行文档处理**：利用Python的并发特性，可处理多个文档。
- **内容任务处理**：集成了OpenAI的API，支持扩充或总结文档内容。
- **灵活的日志记录**：提供DEBUG到INFO不同级别的日志输出，帮助调试与追踪。
- **自定义配置**：通过命令行参数自定义并发程度、工作进程数、目标级别等。

## 安装

### 前提条件

Python 3.10 或更高版本。
- 安装必要的Python包：

```
pip install -r requirements.txt
```

### 下载

直接从GitHub克隆仓库：

```
git clone https://github.com/hellboyvto/gavin-s-writer.git
cd gavin-s-writer
```

## 使用方法

1. 设置环境变量`OPENAI_API_KEY`为你的OpenAI API 密钥。

2. 使用命令行界面，定位到项目目录并执行：

```
python main.py -m YOUR_MAX_CONCURRENCY -w YOUR_MAX_WORKERS -t YOUR_TARGET_LEVELS -l YOUR_LOGGER_LEVEL DOCUMENT_PATHS
```

### 参数说明

- `-m` 或 `--max-concurrency`：单个进程中的最大并发程度。
- `-w` 或 `--max-workers`：进程池中的最大进程数。
- `-t` 或 `--target-levels`：要处理的目标级别。
- `-l` 或 `--logger-level`：日志级别（DEBUG, INFO等）。
- `doc_paths`：要处理的文档路径列表。

例：

```
python main.py -m 8 -w 4 -t 3 -l DEBUG example1.md example2.md
```

## 架构

此工具主要包括几个模块：

- `config.py`：负责解析命令行参数和提供配置。
- `document.py`：定义了文档结构和打印树形结构的功能。
- `content_processor.py`：利用OpenAI API处理文档内容。
- `logger.py`：定义了日志的设置。
- `main.py`：程序的入口点，组织整个文档的处理流程。

## 贡献

我们欢迎各种形式的贡献，无论是功能改进、bug 修复还是文档更新。请通过 GitHub Pull Requests 把你的改进贡献给社区。

## 许可证

此项目采用 [Apache License](LICENSE)。
