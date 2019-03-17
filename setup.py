import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="k40webserver",
    version="0.0.1",
    install_requires=[
        "k40nano",
        "remi"
    ],
    author="Jonathan Diamond",
    author_email="feros32@gmail.com",
    description="A webserver to allow controlling a K40 laser cutter over the network through an attached computer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/axlan/K40WebServer",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ),
)