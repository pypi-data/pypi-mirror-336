from setuptools import setup, find_packages

setup(
    name='mathkat',
    version='0.1.0',
    description='Una libreria de gradientes para Python',
    author='Fernando Leon Franco',
    packages=find_packages(),
    install_requires=[
        'numpy>=2.0.2',
        'matplotlib>=3.10.0',
        'tabulate>=0.9.0'
    ],
)