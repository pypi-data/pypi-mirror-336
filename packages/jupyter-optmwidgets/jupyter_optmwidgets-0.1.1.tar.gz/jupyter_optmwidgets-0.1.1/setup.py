#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Chung Chan
# Distributed under the terms of the Modified BSD License.

import os
from os.path import join as pjoin
from setuptools import setup

HERE = os.path.dirname(os.path.abspath(__file__))
NAME = "jupyter-optmwidgets"

try:
    from jupyter_packaging import (
        wrap_installers,
        npm_builder,
        get_version,
        get_data_files,
    )

    # Get the version from _version.py (optional, if not using pyproject.toml version)
    version = get_version(pjoin(NAME, "_version.py"))

    # Representative files that should exist after a successful build
    jstargets = [
        pjoin(HERE, NAME, "nbextension", "index.js"),
        pjoin(HERE, "package.json"),
    ]

    data_files_spec = [
        ("share/jupyter/nbextensions/jupyter-optmwidgets", "optmwidgets/nbextension", "**"),
        ("share/jupyter/labextensions/@optm/jupyter-optmwidgets", "optmwidgets/labextension", "**"),
        ("share/jupyter/labextensions/@optm/jupyter-optmwidgets", ".", "install.json"),
        ("etc/jupyter/nbconfig/notebook.d", ".", "optmwidgets.json"),
    ]

    cmdclass = wrap_installers(
        post_develop=npm_builder(path=HERE, build_cmd="build:prod"),
        ensured_targets=jstargets,
    )

    setup_args = dict(
        cmdclass=cmdclass,
        data_files=get_data_files(data_files_spec),
        packages=[NAME],
        include_package_data=True,
        # Optional dependencies
        extras_require={
            "test": ["pytest>=4.6", "pytest-cov", "nbval"],
            "docs": [
                "jupyter_sphinx",
                "nbsphinx",
                "nbsphinx-link",
                "pytest_check_links",
                "pypandoc",
                "recommonmark",
                "sphinx>=1.5",
                "sphinx_rtd_theme",
            ],
        },
    )

except ImportError:
    setup_args = dict(packages=[NAME])

if __name__ == "__main__":
    setup(**setup_args)