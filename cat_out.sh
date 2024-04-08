#!/bin/bash

# 清空或初始化output.md文件
> output.md

# 遍历当前目录下所有以.py结尾的文件
for file in *.py; do
  # 检查是否真的存在.py文件，避免当目录下没有.py文件时，*.py被解释为字面量字符串
  if [[ -e $file ]]; then
    # 将文件名作为Markdown代码块的标题
    echo -e "File: $file" >> output.md
    echo '```' >> output.md
    # 将当前.py文件的内容追加到output.md
    cat "$file" >> output.md
    # 结束当前文件内容的代码块
    echo '```' >> output.md
    echo -e "\n" >> output.md
  fi
done
