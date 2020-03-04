"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import io
import os.path
from typing import Dict  # noqa

import setuptools


MODULE_NAME = "readmemaker"
REPOSITORY_URL = "https://github.com/thombashi/{:s}".format(MODULE_NAME)
REQUIREMENT_DIR = "requirements"
ENCODING = "utf8"

pkg_info = {}  # type: Dict[str, str]


def get_release_command_class():
    try:
        from releasecmd import ReleaseCommand
    except ImportError:
        return {}

    return {"release": ReleaseCommand}


with open(os.path.join(MODULE_NAME, "__version__.py")) as f:
    exec(f.read(), pkg_info)

with io.open("README.rst", encoding=ENCODING) as fp:
    long_description = fp.read()

with open(os.path.join(REQUIREMENT_DIR, "requirements.txt")) as f:
    install_requires = [line.strip() for line in f if line.strip()]

with open(os.path.join(REQUIREMENT_DIR, "test_requirements.txt")) as f:
    tests_require = [line.strip() for line in f if line.strip()]

setuptools.setup(
    name=MODULE_NAME,
    version=pkg_info["__version__"],
    url=REPOSITORY_URL,
    author=pkg_info["__author__"],
    author_email=pkg_info["__email__"],
    description=("A Python utility library to help make a README file from " "document files."),
    include_package_data=True,
    license=pkg_info["__license__"],
    long_description=long_description,
    long_description_content_type="text/x-rst",
    keywords=["README"],
    packages=setuptools.find_packages(exclude=["test*"]),
    package_data={MODULE_NAME: ["py.typed"]},
    project_urls={"Source": REPOSITORY_URL, "Tracker": "{:s}/issues".format(REPOSITORY_URL),},
    python_requires=">=3.5",
    install_requires=install_requires,
    tests_require=tests_require,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Documentation",
        "Topic :: Software Development :: Documentation",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing",
    ],
    cmdclass=get_release_command_class(),
)
