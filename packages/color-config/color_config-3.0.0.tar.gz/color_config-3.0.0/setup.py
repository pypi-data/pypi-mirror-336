from setuptools import setup, find_packages

setup(
    name="color_config",
    version="3.0.0",
    packages=find_packages(),
    install_requires=["colorama"],
    author="Otis L. Crossley",
    author_email="soon@email.com",
    description="Ein einfaches Modul für farbige Konsolenausgaben.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jacock123/color_config",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
