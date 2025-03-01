from setuptools import setup, find_packages

setup(
    name="langlands_transformer",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scipy",
        "matplotlib"
    ],
    description="A spectral transformer for analyzing L-functions and automorphic representations",
    author="Your Name",
    license="MIT",
)
