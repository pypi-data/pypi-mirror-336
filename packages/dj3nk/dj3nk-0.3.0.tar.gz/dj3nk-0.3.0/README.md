# dj3nk

English | [简体中文](README_ZH.md)

`dj3nk` is an ID generation algorithm, the principle of which is from [nightteam](https://www.v2ex.com/t/686977).

## 1. Introduction

* You can use `NaturalKeyGenerator` to generate auto-incrementing IDs.
* When using Django ORM, you can inherit the NKModel class to automatically generate auto-incrementing IDs.

## 2. Usage

### Install

```shell
pip install dj3nk

```

### Examples

* Use directly.

```python
from dj3nk.natural_key_generator import NaturalKeyGenerator

# Optional. Reconfigure.
CONFIG = {
    "increment_main_key": "dj3nk",
    "random_bit_length": 16,
    "puzzle_count": 1000000,
    "rdb_conf_name": "default"
}

g = NaturalKeyGenerator(config=CONFIG)
g.generate_nk()

```

* 在Django ORM中使用

```python
# Optional. Configure `settings.py`.
DJ3NK = {
    "increment_main_key": "dj3nk",
    "random_bit_length": 16,
    "puzzle_count": 1000000,
    "rdb_conf_name": "default"
}

# models
from dj3nk.nk_model import NKModel


class XXX(NKModel):
    ...

```
