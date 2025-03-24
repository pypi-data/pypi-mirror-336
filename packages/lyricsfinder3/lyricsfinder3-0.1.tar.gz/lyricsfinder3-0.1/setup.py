from setuptools import setup, find_packages

setup(
    name='lyricsfinder3',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
    description='A simple library to find song lyrics.',
    author='Ramya',
    author_email='ramyacp97@gmail.com',
    url='https://github.com/yourusername/lyrics_finder',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)