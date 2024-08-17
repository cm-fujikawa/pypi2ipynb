# pypi2ipynb

## 概要

PyPI(pypi.org)の「プロジェクトの説明」をJupyter Notebook形式のファイルに変換します。

指定したパッケージ名に従い、次のファイルを出力します。

* README-<package_name>.md
* README-<package_name>.ipynb

## 使用方法

```
poetry install --no-root
poetry run python pypi2ipynb.py <package_name>
```
