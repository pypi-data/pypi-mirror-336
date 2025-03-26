from setuptools import setup, find_packages

setup(
    name='pyurlextract',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='Salil',
    author_email='d2kyt@protonmail.com',
    description='A library to expand Short URL with all possible redirections',
    url='https://github.com/Deadpool2000/Short-URL-Expander-API',
)