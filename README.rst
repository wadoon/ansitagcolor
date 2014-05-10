ansitagcolor
============

.. comment: split here

.. image:: https://travis-ci.org/areku/ansitagcolor.png
    :target: https://travis-ci.org/areku/ansitagcolor
    :alt: Build Status

.. image:: https://coveralls.io/repos/areku/ansitagcolor/badge.png
    :alt: Coverage Status
    :target: https://coveralls.io/r/areku/ansitagcolor

* `Bugs <https://github.com/areku/ansitagcolor/issues>`_


The normal terminal color libraries provide an easy way to
print text with colors and styles. _ansitagcolor_ provides a binding between a tag
(e.g. error, warn, info) and a given `style`. Tags are registered at a `term` instance and
text can be processed with `term.cprint` or replace the `print` with `term.printr`.

.. code::

    Author:  Alexander Weigl
    License: MIT
    Date:    2014-03-14
    Version: 0.2
    

Getting Started
---------------

Install with pip::

    pip install --user ansitagcolor

Run in python::

    from __future__ import print_function
    import ansitagcolor as ansi
    t = ansi.term()
    print = t.printr
    t.register("error", style( foreground = ansi.Color16Table.White,
                               background = ansi.Color16Table.Red) )

    print("{error Error Message!}")
