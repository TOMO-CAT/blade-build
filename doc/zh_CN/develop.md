# 开发 #

## 基本原理 ##

### 加载配置 ###

Blade 启动后，会依次尝试通过 `execfile` 函数执行多个路径下的配置文件，这些配置文件都是 python 源文件，调用 blade 里预先定义好的配置函数，
把配置项更新到 blade.config 的配置 dict 里，供后续使用。

配置文件加载完毕后，blade 还会尝试把命令行选项里和 global_config 同名的选项更新到配置里，使得来自命令行的配置信息优先级最高。

### 加载 BUILD 文件 ###

Blade 会从命令行指定的构建目标展开，通过 `execfile` 函数逐个执行 `BUILD` 文件，BUILD 文件里的代码被执行的时候，
就会调用 blade 内部预先定义好的规则函数，把目标注册到 blade 内部的数据结构里。

对于被命令行里指定的目标直接或者间接依赖的目标，blade 都会加载相应目录下的 BUILD 文件，直到所有的依赖都被加载。

### 依赖分析 ###

Blade 会对加载后的目标，从命令行指定的目标为根出发，进行拓扑排序，得出一个要构建的目标列表及其正确的构建顺序。

### 生成后端构建文件 ###

Blade 得到要构建的目标列表后，就可以逐渐根据各个目标来生成相应的构建规则的目标动作，并输出到后端构建脚本文件。

### 执行后端构建系统 ###

Blade 调用后端构建工具执行实际的构建，执行完毕后，删除后端构建脚本文件。

### 运行测试 ###

从命令行收集到的测试目标列表，逐个构建执行环境运行测试，Blade 支持多任务并发测试，这时后台会起多个线程去执行测试文件。
所有测试都执行完毕后，收集测试结果汇总并输出报告。

## 如何参与开发 ##

欢迎给 Blade 贡献代码！无论是 bugfix 还是 feature。大的 feature 可以先提 issue，以避免沟通不畅带来的反复。

### 拉取代码 ###

通过 github 的 Fork 功能 fork 到你自己的仓库，即可进行修改和测试。

### 修改文件 ###

我们遵守 Google Python 代码风格，修改代码请用 pylint 进行代码检查。

### 测试验证 ###

在源代码开发目录中，Blade 优先运行开发中的代码。可以执行 src/test/runalltests.sh 进行全局验证。

### 调试与诊断 ###

大多数子命令支持 `--stop-after` 选项，可选的参数有 {load, analyze, generate, build}，可以控制 blade 在完成此阶段后就结束。比如

```bash
blade build --stop-after generate
```

使得 blade 在生成后端构建系统描述文件（比如 `build.ninja`）后即结束，可以用于检查生成的文件的问题。

### 性能分析 ###

大多数子命令支持 `--profiling` 选项，在 blade 结束后会输出性能分析报告。如果需要更详细的分析，可以把性能分析留下的 blade.pstats 按指示转为图。

和 --stop-after 选项组合，可以用于分析不同阶段的性能。

### 打包 ###

代码根目录下的 `dist_blade` 可以用来打包成 zip 方便部署，和同目录下的 `blade` bash 脚本以及 `blade.conf` 放在一起即可。

### Pull Request ###

代码本地修改后，Push 到你自己的 github 仓库，在向我们发起 Pull Request 即可。我们会尽快进行 review，但是由于工作繁忙，时间不好保证。
最好检查一下代码风格，确保有必要而不冗余的注释，避免不必要的评审往复。

## 其他资料 ##

这里还有两篇其他网友对 Blade 实现原理的分析，是基于 Blade 早期版本，虽然有些过时，但是依然有参考价值。

* [浅谈 blade 中 C++Build 的设计与实现](https://tsgsz.github.io/2013/11/01/2013-11-01-thinking-in-design-of-blade-cpp-build/)
* [锋利的 blade 到底锋利在哪里](https://blog.csdn.net/zaishaoyi/article/details/48465081)
