from setuptools import setup, find_packages

setup(
    name="kaltts",
    version="1.0.2004",
    packages=find_packages(),
    install_requires=[
        "pydub",
        "requests",
        'numpy',
        'tensorflow',
        'librosa',
        'pydub',
    ],
    entry_points={
        "console_scripts": [
            "kaltts=kaltts.tts_module:main",
        ],
    },
    author='kalculusGuy',
    author_email='calculus069@gmail.com',
    description='Kal Text-to-Speech (TTS) Synthesis',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Odeneho-Calculus/KTTS_v1_model",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)