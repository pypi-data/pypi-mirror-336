from setuptools import setup, find_packages
import os

# Get the long description from the README file
with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='kaltts',
    version='1.0.1002',  # Increment the version number for the new release
    author='kalculusGuy',
    author_email='calculus069@gmail.com',
    description='Kal Text-to-Speech (TTS) Synthesis',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Odeneho-Calculus/KTTS_v1_model',
    packages=find_packages(where='KTTS_v1_model/src'),
    package_dir={'': 'KTTS_v1_model/src'},
    include_package_data=True,
    install_requires=[
        'numpy',
        'tensorflow',
        'librosa',
        'gtts',
        'pydub',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)