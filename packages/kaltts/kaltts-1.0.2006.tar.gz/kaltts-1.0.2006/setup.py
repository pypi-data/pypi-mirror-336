from setuptools import setup, find_packages

# Read the long description from the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="kaltts",
    version="1.0.2006",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pydub",
        "requests",
        "numpy",
        "tensorflow",
        "librosa",
        "pyyaml",
        "num2words",
        "urllib3"
    ],
    entry_points={
        "console_scripts": [
            "kaltts=kaltts.controller:main",
        ],
    },
    author='kalculusGuy',
    author_email='calculus069@gmail.com',
    description='Kal Text-to-Speech (TTS) Synthesis',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Odeneho-Calculus/KTTS_v1_model",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    project_urls={
        "Bug Tracker": "https://github.com/Odeneho-Calculus/KTTS_v1_model/issues",
        "Documentation": "https://github.com/Odeneho-Calculus/KTTS_v1_model#readme",
        "Source Code": "https://github.com/Odeneho-Calculus/KTTS_v1_model",
    },
)
