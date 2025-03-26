from setuptools import setup, find_packages
import os

with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='kaltts',
    version='0.2.2',
    author='kalculus',
    author_email='calculus069@gmail.com',
    description='A Text-to-Speech synthesis model',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'numpy',
        'tensorflow',
        'pyyaml',
    ],
    extras_require={
        'full': [
            'librosa',
            'num2words',
            'phonemizer',
            'torch',
        ],
    },
    entry_points={
        'console_scripts': [
            'kaltts=kaltts.__main__:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)