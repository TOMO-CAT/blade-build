#!/bin/bash

set -e


# 准备环境
# 1. 安装 tcmalloc
# sudo apt install google-perftools libgoogle-perftools-dev
# 2. 安装 javac
# sudo apt install openjdk-11-jdk
# 3. 安装 thrift
# sudo apt install thrift-compiler
# sudo apt install libthrift-dev

bash example/blade.sh build ...
