from glob import glob
from setuptools import setup, find_packages


setup(
    name="py_client",
    version="0.1.0",
    packages=find_packages(),
    scripts=glob("bin/*"),
    install_requires=[
    ],
    extras_require={
        "dev": ["black", "pylama", "rope"],
    },
)
