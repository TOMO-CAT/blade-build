# 更新日志

## 发布版本规范

需要保证如下命令运行通过（后续考虑配置 github action 流水线）：

```bash
```

## v1.0.0

### Feature

* 通过 install 脚本安装 blade 后会将 version 写入到 blade/blade_version.py, 从而更容易定位到 blade 版本
* 优化 `cuda_config`, 支持指定 ccbin 和 linkflags
* 优化 `cc_config`, 支持添加 `extra_sys_incs`
* 优化 `prebuilt_cc_library`, 以 `-isystem` 的方式添加 prebuild 库的头文件, 从而避免污染我们自己项目的参数
