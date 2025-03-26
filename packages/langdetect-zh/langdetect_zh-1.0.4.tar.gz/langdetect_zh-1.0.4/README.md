langdetect_zh
==========



Installation
============

    $ pip install langdetect_zh

Supported Python versions 2.7, 3.4+.


Languages
=========

``langdetect_zh`` supports 2 languages out of the box ([ISO 639-1 codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)):

    zh-cn, zh-tw


Basic usage
===========

Directly output the most similar language code：

```python
>>> from langdetect_zh import detect
>>> detect("这是一段中文文本")
'zh-cn'
```

To find out the probabilities for the top languages:

```python
>>> from langdetect_zh import detect_langs
>>> detect_langs("这是一段中文文本")
[zh-cn:0.999997316441747]
```

**NOTE**

Language detection algorithm is non-deterministic, which means that if you try to run it on a text which is either too short or too ambiguous, you might get different results everytime you run it.

To enforce consistent results, call following code before the first language detection:

```python
from langdetect_zh import DetectorFactory
DetectorFactory.seed = 0
```




Original project
================

This package is an optimization of [langdetect](https://github.com/Mimino666/langdetect). The specific optimization measure is to subdivide simplified Chinese and traditional Chinese under the condition of pure Chinese.
