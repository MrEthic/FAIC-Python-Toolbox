from setuptools import setup, find_packages

from faic_toolbox import __version__

setup(
    name="faic_toolbox",
    version=__version__,
    url="https://github.com/MrEthic/FAIC-Python-Toolbox",
    author="Jeremie Basso",
    py_modules=find_packages(),
    install_requires=[
        "pandas",
        "requests",
    ],
)
