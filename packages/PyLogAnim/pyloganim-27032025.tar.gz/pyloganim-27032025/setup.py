from setuptools import setup, find_packages

setup(
    name='PyLogAnim',
    version='27032025',
    packages=find_packages(),
    install_requires=[
        'colorama',  
    ],
    author='Elzzie',
    author_email='fractus.lol@proton.me',
    description='A library for animating your logos',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/lz-fkn/PyLogAnim', # add your github repo here.
)