from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='OctoLingo',
    version='0.1.3',
    description='A Python package for translating large texts with advanced features.',
    long_description=long_description,
    long_description_content_type='text/markdown',  # Specify that the description is in Markdown
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