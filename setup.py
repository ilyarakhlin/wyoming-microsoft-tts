"""Setup file for wyoming-microsoft-tts."""

from pathlib import Path

import setuptools
from setuptools import setup

this_dir = Path(__file__).parent
module_dir = this_dir / "wyoming_microsoft_tts"

requirements = []
requirements_path = this_dir / "requirements.txt"
if requirements_path.is_file():
    with open(requirements_path, encoding="utf-8") as requirements_file:
        requirements = requirements_file.read().splitlines()

data_files = [module_dir / "voices.json"]

# -----------------------------------------------------------------------------

setup(
    name="wyoming_microsoft_tts",
    version="1.3.2",
    description="Wyoming Server for Microsoft TTS",
    url="https://github.com/ilyarakhlin/wyoming-microsoft-tts",
    author="Hugo Bloem",
    author_email="",
    license="MIT",
    packages=setuptools.find_packages(),
    package_data={
        "wyoming_microsoft_tts": [str(p.relative_to(module_dir)) for p in data_files]
    },
    install_requires=requirements,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Text Processing :: Linguistic",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="rhasspy wyoming microsft tts",
)
