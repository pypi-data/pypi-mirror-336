# The MIT License (MIT)
#
# Copyright(c) 2021, Damien Feneyrou <dfeneyrou@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files(the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions :
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import io
import os
import os.path
import sys
import shutil
from setuptools import setup, find_packages, Extension


# Constants
isDevMode = False  # Enable to speed up development cycles. Shall be False for final installation

# Deduce some parameters
extra_link_args = []
extra_compilation_flags = ["-I", "palanteer/_cextension"]

if isDevMode:
    if sys.platform == "win32":
        extra_compilation_flags.append("/Zi")
        extra_link_args.append("/DEBUG")
    else:
        extra_compilation_flags.append("-O0")  # Debug symbols are already generated

classifiers_list = [
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",
    "Development Status :: 4 - Beta",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Programming Language :: Python :: Implementation :: CPython",
    "Environment :: Console",
    "Operating System :: Microsoft :: Windows :: Windows 10",
    "Operating System :: Microsoft :: Windows :: Windows 11",
    "Operating System :: POSIX :: Linux",
    "Topic :: Software Development",
    "Topic :: Software Development :: Debuggers",
]

# If in-source, copy palanteer.h inside the folder (constraint from setup.py)
if os.path.isfile("../c++/palanteer.h"):
    shutil.copyfile("../c++/palanteer.h", "palanteer/_cextension/palanteer.h")

# Read the Palanteer version from the C++ header library
with io.open("palanteer/_cextension/palanteer.h", encoding="UTF-8") as versionFile:
    PALANTEER_VERSION = (
        [l for l in versionFile.read().split("\n") if "PALANTEER_VERSION " in l][0]
        .split()[2]
        .replace('"', "")
    )

# Read the content of the readme file
with io.open("README.md", encoding="UTF-8") as readmeFile:
    long_description = readmeFile.read()

# Build call
setup(
    name="palanteer",
    version=PALANTEER_VERSION,
    author="Damien Feneyrou",
    author_email="dfeneyrou@gmail.com",
    license="MIT",
    description="Palanteer instrumentation library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=classifiers_list,
    python_requires=">=3.7",
    url="https://github.com/dfeneyrou/palanteer",
    packages=find_packages(),
    ext_modules=[
        Extension(
            "palanteer._cextension",
            sources=[
                os.path.normpath("palanteer/_cextension/pyPalanteerInstrumentation.cpp")
            ],
            extra_compile_args=extra_compilation_flags,
            extra_link_args=extra_link_args,
        )
    ],
    zip_safe=False,
)

# If in-source, remove the copied palanteer.h (cleanup)
if os.path.isfile("../c++/palanteer.h"):
    os.unlink("palanteer/_cextension/palanteer.h")
