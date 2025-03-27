import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE/"README.MD").read_text()

setup(
    name='topsis_102203883',
    version='0.3.5',
    description="a package to calculate topsis",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        
    ],
    entry_points={
        "console_scripts": [
            "topsis-102203883 = topsis_102203883.__main__:result",
        ],
    },
)