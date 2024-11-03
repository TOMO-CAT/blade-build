# Test

## 运行 example

```bash
bash scripts/example.sh
```

## 运行单测

```bash
# 运行全部单测
bash src/test/runall.sh

# 运行单个单测
bash src/test/run.sh cc_binary_test.py
```

## 调试单个单测

```bash
export PYTHONPATH=$PYTHONPATH:/auto_pilot/thirdparty/blade-build/src

cd /auto_pilot/thirdparty/blade-build/src/test/
python cc_binary_test.py
```

调试的时候可以使用 `.vscode/launch.json` 断点调试, 或者直接查看 `src/test/testdata/build_output.txt` 日志。
