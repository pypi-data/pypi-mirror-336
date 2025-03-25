# Crealand SDK

Crealand SDK

# 版本号修改

- 修改`version.txt`中的版本号

## Requirements

- build
 - setuptools
 - wheel
 - twine

## build

需要先 pip 安装 build（setuptools 和 wheel会自动安装）， 再编译打包：

```
python3 -m pip install build
python3 -m build
```

## Install

```bash
pip install crealand
```

## Uninstall

```bash
pip uninstall crealand
```

## Publish

### 前置条件

- 把根目录的`.pypirc`文件拷贝到系统用户根目录；
- 安装`twine`

### 发布测试环境

> https://test.pypi.org/

```bash
python3 -m twine upload --repository testpypi dist/*
```

### 发布正式环境

> https://pypi.org/

```bash
python3 -m twine upload --repository pypi dist/*
```
