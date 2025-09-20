# Blade Build System

[![license NewBSD](https://img.shields.io/badge/License-NewBSD-yellow.svg)](COPYING)
[![Python](https://img.shields.io/badge/language-python2,3-blue.svg)](https://www.python.org/)
[![Code Style](https://img.shields.io/badge/code%20style-google-blue.svg)](https://google.github.io/styleguide/pyguide.html)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macos-lightgrey.svg)](doc/zh_CN/prerequisites.md)

```text
██████╗ ██╗      █████╗ ██████╗ ███████╗
██╔══██╗██║     ██╔══██╗██╔══██╗██╔════╝
██████╔╝██║     ███████║██║  ██║█████╗
██╔══██╗██║     ██╔══██║██║  ██║██╔══╝
██████╔╝███████╗██║  ██║██████╔╝███████╗
╚═════╝ ╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝
```

Blade 是一个方便易用高性能的现代化代码构建系统，特别适合公司内的大规模代码库的敏捷构建，内置了对多种编程语言及单元测试框架的直接支持。

## Build Status

[![Build Status](https://travis-ci.org/chen3feng/blade-build.svg?branch=master)](https://travis-ci.org/chen3feng/blade-build)
[![codebeat badge](https://codebeat.co/badges/e0d861b7-47cc-4023-9784-7d54246a3576)](https://codebeat.co/projects/github-com-chen3feng-blade-build-master)
[![Coverage](https://coveralls.io/repos/chen3feng/blade-build/badge.svg?branch=master)](https://coveralls.io/github/chen3feng/blade-build)
[![Downloads](https://img.shields.io/github/downloads/chen3feng/blade-build/total.svg)](https://github.com/chen3feng/blade-build/releases)

## 演示

我们先来看一个漂亮的演示：

[![asciicast](https://asciinema.org/a/o9uQ2uia4OVqghXUid7XSNjv1.svg)](https://asciinema.org/a/o9uQ2uia4OVqghXUid7XSNjv1)

## 发布

master 分支上的代码是开发版，应当视为 alpha 版。正式环境请优先考虑使用 tag 上的版本。我们会不定期地把内部大规模代码库上验证过的版本发布到 tag 上。

* Blade 发布 2.0，包含以下特性：
  * 逐步废弃 python2, 仅支持 python3
  * 全面支持 Python 构建
  * 支持自定义扩展
  * 后端只支持 [ninja](doc/zh_CN/config.md#global_config) 构建系统，大幅度提高构建性能

具体请查看 [升级说明](doc/zh_CN/upgrade-to-v2.md)。

## 为何而生

首先，Blade 解决了依赖问题。当你在构建某些目标时，头文件有变化，会自动重新构建。最方便的是，Blade 也能追踪库文件的依赖关系。

比如库 foo 依赖库 common，那么在库 foo 的 BUILD 文件中列入依赖：

```python
cc_library(
    name = 'foo',
    srcs = ...,
    hdrs = ...,
    deps = ':common'
)
```

那么对于使用 foo 的程序，如果没有直接用到 common，那么就只需要列出 foo，并不需要列出 common。

```python
cc_binary(
    name = 'my_app',
    srcs = ...,
    deps = ':foo'
)
```

这样当你的库实现发生变化，增加或者减少库时，并不需要通知库的用户一起改动，Blade 自动维护这层间接的依赖关系。当构建 my_app 时，也会自动检查 foo 和 common 是否也需要更新。

说到易用性，除了依赖关系的自动维护，Blade 还可以做到，用户只需要敲一行命令，就能把整个目录树的编译链接和单元测试全部搞定。例如：

递归构建和测试 common 目录下所有的目标

```bash
blade test common...
```

以 32 位模式构建和测试

```bash
blade test -m32 common...
```

以调试模式构建和测试

```bash
blade test -pdebug common...
```

显然，你可以组合这些标志

```bash
blade test -m32 -pdebug common...
```

## 特点

* 自动分析头文件依赖关系，构建受影响的代码
* 增量编译和链接，只构建因变更受影响而需要重新构建的代码
* 自动计算库的间接依赖，库的作者只需要写出直接依赖，构建时自动检查所依赖的库是否需要重新构建
* 在任意代码树的任意子目录下都能构建
* 支持一次递归构建多个目录下的所有目标，也支持只构建任意的特定的目标
* 无论构建什么目标，这些目标所依赖的目标也会被自动连坐更新
* 内置 debug/release 两种构建类型
* 彩色高亮构建过程中的错误信息
* 支持 ccache
* 支持 distcc
* 支持基于构建多平台目标
* 支持构建时选择编译器（不同版本的 gcc，clang 等）
* 支持编译 protobuf，lex, yacc
* 支持自定义规则
* 支持测试，在命令行跑多个测试
* 支持并行测试（多个测试进程并发运行）
* 支持增量测试（无需重新运行的测试程序自动跳过）
* 集成 gperftools，自动检测测试程序的内存泄露
* 构建脚本 vim 语法高亮
* svn 式的子命令命令行接口
* 支持 bash 命令行补全
* 用 python 编写，无需编译，直接安装使用

彻底避免以下问题：

* 头文件更新，受影响的模块没有重新构建。
* 被依赖的库需要更新，而构建时没有被更新，比如某子目录依

## 安装

```bash
git clone git@github.com:TOMO-CAT/blade-build.git
cd blade-build/
./install
source ~/.bashrc
```

## 文档

看到这里，你应该觉得 Blade 是个不错的工具，那么，阅读 [完整文档](doc/zh_CN/README.md)，开始使用吧。

如果遇到有问题，可以试试先查一下 [FAQ](doc/zh_CN/FAQ.md)，也许有你需要的信息。

## 最佳实践

* IDE: vscode
* 操作系统: ubuntu22.04 / ubuntu24.04
