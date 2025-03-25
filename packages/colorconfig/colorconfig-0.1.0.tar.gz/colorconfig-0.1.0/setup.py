from setuptools import setup, find_packages

setup(
    name="colorconfig",
    version="0.1.0",
    author="Otis L. Crossley",
    author_email="soon@soon.com",
    description="Ein einfaches Farbkonfigurationsmodul für die Konsole",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jacock123/colorconfig",
    packages=find_packages(),
    install_requires=["colorama"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
