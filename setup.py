from setuptools import setup, find_packages

setup(
    name='freespacer',
    version="0.0.1",
    description='CLI tool for circular cleaning old backup files',
    author='trapwalker',
    url='https://github.com/sergyp/freespacer',
    author_email='svpmailbox@gmail.com',
    license='MIT',
    install_requires=[
        "click",
        "pathlib",
        "psutil",
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': 'freespacer = freespacer:main'
    },
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License"
    ]
)
