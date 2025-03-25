from setuptools import setup, find_packages

setup(
    name="FNA_DB",
    version="0.1.0",
    author="Hyabusa1990",
    description="Client für den FNA-DBServer",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.gras-it.de/bsapp/fieldnet-ampel/fna-dbclient",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)