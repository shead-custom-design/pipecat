# Copyright 2016 Timothy M. Shead
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
