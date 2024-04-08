# Gavin's Writer

## Introduction
Gavin's Writer is a powerful document processing tool, designed to parse, render, and modify documents with support for parallel processing and logging. It allows users to process a batch of documents using configuration options set through command-line arguments.

## Features

- **Parallel Document Processing**: Leverages Python's concurrency features for handling multiple documents simultaneously.
- **Content Task Handling**: Integrates OpenAI's API to enrich or summarize document content.
- **Flexible Logging**: Offers logging levels from DEBUG to INFO for troubleshooting and tracking purposes.
- **Customizable Configuration**: Users can specify concurrency level, number of workers, target levels, and more through command-line parameters.

## Installation

### Prerequisites

Python 3.10 or higher.
- Required Python packages installed:

```
pip install -r requirements.txt
```

### Download

Clone the repository from GitHub:

```
git clone https://github.com/hellboyvto/gavin-s-writer.git
cd gavin-s-writer
```

## Usage

1. Set the `OPENAI_API_KEY` environment variable to your OpenAI API key.

2. Open a command line interface, navigate to the project directory, and execute:

```
python main.py -m YOUR_MAX_CONCURRENCY -w YOUR_MAX_WORKERS -t YOUR_TARGET_LEVELS -l YOUR_LOGGER_LEVEL DOCUMENT_PATHS
```

### Parameters Explanation

- `-m` or `--max-concurrency`: The maximum number of coroutines in a single process.
- `-w` or `--max-workers`: The maximum number of processes in the pool.
- `-t` or `--target-levels`: The target levels to process.
- `-l` or `--logger-level`: Logging level (e.g., DEBUG, INFO).
- `doc_paths`: File paths of the documents to be processed.

Example:

```
python main.py -m 8 -w 4 -t 3 -l DEBUG example1.md example2.md
```

## Architecture

This tool mainly consists of several modules:

- `config.py`: Responsible for parsing command-line arguments and providing configuration.
- `document.py`: Defines the document structure and functionality for printing a tree structure.
- `content_processor.py`: Uses the OpenAI API to process document content.
- `logger.py`: Sets up logging configurations.
- `main.py`: The entry point of the program, orchestrating the whole document processing flow.

## Contributing

We welcome contributions in any form, whether it's feature enhancement, bug fixes, or documentation updates. Please submit your contributions to the community through GitHub Pull Requests.

## License

This project is licensed under the [Apache License](LICENSE).