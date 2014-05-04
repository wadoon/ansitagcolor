#!/usr/bin/python

from distutils.core import setup

def read(*filenames, **kwargs):
    """Red the contents of the given files
    """
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with open(filename) as textfile:
            buf.append(textfile.read())
    return sep.join(buf)

DESCRIPTION = read('README.md')

setup(
    name="ansitagcolor",
    version="0.2",
    url="http://github.com/areku/ansitagcolor",
    license="MIT",
    author="Alexander Weigl",
    author_email="alexweigl@gmail.com",
    py_modules=["ansi"],
    requires=['enum'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        "Environment :: Console",
        "Intended Audience :: Developers"
    ],


)
