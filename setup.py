# Copyright 2016 Timothy M. Shead
#
# This file is part of Pipecat.
#
# Pipecat is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pipecat is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pipecat.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup, find_packages
import re

setup(
    name="pipecat",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    description="Elegant, flexible data logging in Python for connected sensors and instruments.",
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
    url="http://pipecat.readthedocs.org",
    version=re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]",
        open(
            "pipecat/__init__.py",
            "r").read(),
        re.M).group(1),
)

