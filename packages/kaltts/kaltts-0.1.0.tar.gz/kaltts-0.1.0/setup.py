from setuptools import setup, find_packages

setup(
    name='kaltts',
    version='0.1.0',
    author='kalculus',
    author_email='calculus069@gmail.com',
    description='A Text-to-Speech synthesis model',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'numpy',
        'tensorflow',
        'pyyaml',
        'librosa',
        'num2words',
        'phonemizer',
        'torch',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)