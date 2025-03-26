import re

from setuptools import setup


def ulid_version():
    with open('ulid/__init__.py') as f:
        return re.search("__version__ = ['\"]([^'\"]+)['\"]", f.read()).group(1)


VERSION = ulid_version()
with open('README.md', encoding='utf-8') as file:
    DESCRIPTION = file.read()

setup(
    name='simple-ulid',
    version=VERSION,
    python_requires='>=3.6',
    author='Ali RajabNezhad',
    author_email='alirn1997@gmail.com',
    url='https://github.com/alirn76/ulid',
    description='Universally Unique Lexicographically Sortable Identifier',
    long_description=DESCRIPTION,
    long_description_content_type='text/markdown',
    include_package_data=True,
    license='MIT',
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
    ],
)
