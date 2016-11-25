from setuptools import setup, find_packages
import re

setup(
    name="datacat",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Environment :: Other Environment",
        "Framework :: IPython",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    description="Data logger for managing information collected from real-world instruments.",
    install_requires=[
        "arrow",
        "numpy>=1.8.0",
        "Pint",
    ],
    maintainer="Timothy M. Shead",
    maintainer_email="tim@shead-custom-design.gov",
    packages=find_packages(),
    scripts=[
        ],
    url="http://datacat.readthedocs.org",
    version=re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]",
        open(
            "datacat/__init__.py",
            "r").read(),
        re.M).group(1),
)
