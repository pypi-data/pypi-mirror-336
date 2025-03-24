# Introduction

This library provides simple Pythonic interface to use specified text-to-speech synthesizer.

It supports following synthesizers:

- macOS's builtin synthesizer
  - Only allows personal, non-commercial use (as stated in macOS software license agreement).
  - Outputs mp4 file.
- eSpeak NG
  - Requires installing eSpeak NG CLI first.
  - Outputs wav file.

# How to Use

It is straight-forward as below:

``` python
In [1]: from simple_talk import SimpleTalk

In [2]: s = SimpleTalk()

In [3]: s.talk("Hello world!", "output")
```

In addition, you can specify voice and/or synthesizer when constructing `SimpleTalk` object.
