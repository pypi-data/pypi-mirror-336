from setuptools import setup, find_packages
import codecs

with codecs.open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nepali-date-cli",
    version="0.1.6",
    packages=find_packages(),
    install_requires=[
        "nepali-datetime",
    ],
    entry_points={
        "console_scripts": [
            "nepdate=nepali_date_cli.cli:main",
        ],
    },
    author="Nishant Thapa",
    author_email="itsnishantu@gmail.com",
    description="A command-line tool to display Nepali dates",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/itznishantthapa/nepdate",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 