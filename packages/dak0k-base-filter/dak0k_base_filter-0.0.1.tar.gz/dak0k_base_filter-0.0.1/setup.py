from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Filtering package'
LONG_DESCRIPTION = 'A package that allows filtering and sorting of data efficiently.'

setup(
    name="dak0k_base_filter",
    version=VERSION,
    author="dak0k (Adaibekov Darkhan)",
    author_email="<adaibekovdarkhan5@gmail.com>",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        'django',
    ],
    keywords=['python', 'data filtering', 'data processing', 'sorting', 'queryset filtering'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
