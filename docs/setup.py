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


import argparse
import os
import re
import shutil
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("command", nargs="?", default="html", choices=["clean", "html"], help="Command to run.")
arguments = parser.parse_args()

root_dir = os.path.abspath(os.path.join(__file__, "..", ".."))
docs_dir = os.path.join(root_dir, "docs")
build_dir = os.path.join(docs_dir, "_build")
test_dir = os.path.join(docs_dir, "_test")

def convert_notebook(name):
    # If the Sphinx source is up-to-date, we're done.
    source = os.path.join(docs_dir, "%s.ipynb" % name)
    target = os.path.join(docs_dir, "%s.rst" % name)
    if os.path.exists(target) and os.path.getmtime(
            target) >= os.path.getmtime(source):
        return

    # Convert the notebook to pure Python, so we can run verify
    # that it runs without any errors.

    if not os.path.exists(test_dir):
        os.mkdir(test_dir)

    subprocess.check_call(["jupyter",
                           "nbconvert",
                           "--execute",
                           "--to",
                           "python",
                           source,
                           "--output",
                           os.path.join(test_dir, name),
                           ])

    subprocess.check_call(["python", os.path.join(test_dir, "%s.py" % name)])

    # Convert the notebook into restructured text suitable for the
    # documentation.

    env = dict()
    env.update(os.environ)

    subprocess.check_call(["jupyter",
                           "nbconvert",
                           "--execute",
                           "--to",
                           "rst",
                           source,
                           "--output",
                           name,
                           ], env=env)

    # Unmangle Sphinx cross-references in the tutorial that get mangled by
    # markdown.
    with open(target, "r") as file:
        content = file.read()
        content = re.sub(":([^:]+):``([^`]+)``", ":\\1:`\\2`", content)
        content = re.sub("[.][.].*\\\\(_[^:]+):", ".. \\1:", content)

        content = """
  .. image:: ../artwork/pipecat.png
    :width: 200px
    :align: right
  """ + content

    with open(target, "w") as file:
        file.write(content)

# Always build the documentation from scratch.
if os.path.exists(build_dir):
    shutil.rmtree(build_dir)

notebooks = [
        ]

# Clean the build.
if arguments.command == "clean":
    for name in notebooks:
        if os.path.exists("%s.rst" % name):
            os.remove("%s.rst" % name)

# Generate the HTML documentation.
if arguments.command in ["html"]:
    for name in notebooks:
        convert_notebook(name)
    subprocess.check_call(["make", arguments.command], cwd=docs_dir)

