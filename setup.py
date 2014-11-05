__author__ = 'xudshen@hotmail.com'

import os

from setuptools import setup


# Utility function to read the README file.
def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name='forest',
    version='0.0.1',
    author='Xudong Shen',
    author_email='xudshen@hotmail.com',
    description=('restful api generator using XPath',),
    license='MIT',
    keywords='rest restful api html xhtml xml XPath parser',
    url='https://github.com/xudshen/forest',
    packages=['forest', ],
    long_description=read('README.md'),
    classifiers=[
        'Development Status :: 1 - Planning',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
    ],
    requires=['requests>=2.4.3', 'beautifulsoup4>=4.2.0', 'lxml>=3.4', 'html5lib>=0.999', 'chardet>=2.3.0', 'sqlparse>=0.1.2']
)