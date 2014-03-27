ansitagcolor
============

[![Build Status](https://travis-ci.org/areku/ansitagcolor.png)](https://travis-ci.org/areku/ansitagcolor)
[![Coverage Status](https://coveralls.io/repos/areku/ansitagcolor/badge.png)](https://coveralls.io/r/areku/ansitagcolor)

The normal terminal color libraries provide an easy way to print text with colors and styles. _ansitagcolor_ provides a binding between a tag (e.g. error, warn, info) and a given `style`. Tags are registered at a `term` instance and text can be processed with `term.cprint` or replace the `print` with `term.printr`.

    Author:  Alexander Weigl
    License: MIT
    Date:    2014-03-14
    Version: 0.2
    

## Getting Started

Install with pip:

```shell
pip install --user ansitagcolor
```

Run in python.

```python
from __future__ import print_function
import ansi 
t = ansi.term()
print = t.printr
t.register("error", style( foreground = ansi.Color16Table.White, background = ansi.Color16Table.Red) )

print("{error Error Message!}")
```


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/areku/ansitagcolor/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

