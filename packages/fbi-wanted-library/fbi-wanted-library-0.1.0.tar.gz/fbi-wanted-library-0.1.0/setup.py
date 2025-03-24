from setuptools import setup, find_packages

setup(
    name="fbi-wanted-library",
    version="0.1.0",
    author="Inioluwa Adenaike",
    author_email="inioluwadenaike@gmail.com",
    description="A library to search for wanted persons using the FBI API.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ininike/fbi-wanted-search",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "requests",
    ],
)