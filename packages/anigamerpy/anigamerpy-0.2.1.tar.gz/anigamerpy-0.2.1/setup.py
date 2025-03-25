import setuptools
from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='anigamerpy',
    version='0.2.1',
    author='Sakuya0502',
    description='動畫瘋爬蟲工具',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/Sakuya0502/anigamerpy',
    packages=setuptools.find_packages(),
    classifiers=[
        'Natural Language :: Chinese (Traditional)',
        'Operating System :: Microsoft :: Windows :: Windows 11',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ],
    license='MIT',
    requires=[
        'requests',
        'bs4'
    ]
)