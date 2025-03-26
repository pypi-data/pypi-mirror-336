# setup.py
from setuptools import setup, find_packages

setup(
    name='gcsstaff',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'click',  # 如果使用click作为命令行库
    ],
    entry_points={
        'console_scripts': [
            'gcsstaff = gcsstaff.cli:greet',
        ],
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='A simple CLI tool',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/gcsstaff',  # 项目的URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)