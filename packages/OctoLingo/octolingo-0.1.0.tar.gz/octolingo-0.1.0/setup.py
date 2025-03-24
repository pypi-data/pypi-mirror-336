from setuptools import setup, find_packages

setup(
    name='OctoLingo',
    version='0.1.0',
    description='A Python package for translating large texts with advanced features.',
    author='Birhan Tamiru',
    author_email='birhantamiru281@gmail.com',
    packages=find_packages(),
    install_requires=[
        'googletrans==4.0.0-rc1',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)