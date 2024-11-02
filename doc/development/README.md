# Development

## 调试

首先先找到 blade 运行的具体命令（我们已经在 `./blade` 脚本中打印出来了）：

```bash
$ blade build gpu/cuda_util:cuda_test_kernel
+ python /auto_pilot/blade-build/src build gpu/cuda_util:cuda_test_kernel
Blade: Entering directory `/auto_pilot'
```

安装 VSCode 的 `Python` 插件，然后配置对应的 launch.json 。

```json
{
    // 使用 IntelliSense 了解相关属性。 
    // 悬停以查看现有属性的描述。
    // 欲了解更多信息，请访问: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            // 调试配置的名称
            "name": "Blade Version",
            // python 调试配置
            "type": "debugpy",
            // 请求类型: launch / attach
            "request": "launch",
            // Python 脚本路径
            "program": "/home/cat/Documents/company/auto_pilot/blade-build/src", // 指定您的Python脚本路径
            // 传递给程序的命令行参数
            "args": [
                "--version"
            ],
            // 在集成终端中显示输出
            "console": "integratedTerminal",
            // 如果需要调试第三方库代码, 可以设置为false
            "justMyCode": true
        }
    ]
}
```
