from setuptools import setup, find_packages

setup(
    name="data_wrangling_python",
    version="0.1.0",
    author="Jeroen van Raak",
    author_email="j.j.f.vanraak@uva.nl",
    description="A simple utility to create lagged and lead variables in time series data",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/vanraak/data_wrangling",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
    install_requires=["pandas"],
)
