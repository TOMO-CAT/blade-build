# python

## pylint

`.pylintrc` 用于定制 Pylint 的检查规则。

手动运行 pylint：

```bash
# 检查所有 .py 文件
# 支持 Glob 模式匹配语法
# * `**` 表示匹配任意层级的子目录
# * `*` 表示匹配任意字符 (不包含路径分隔符)
pylint **/*.py

# 忽略 scripts 文件夹下的 python 文件
# @see https://stackoverflow.com/questions/2503717/ignore-by-directory-using-pylint
pylint **/*.py --ignore-paths=^scripts/.*$
```
