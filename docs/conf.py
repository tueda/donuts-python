"""Configuration file for the Sphinx documentation builder."""

# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import subprocess
import sys

sys.path.insert(0, os.path.abspath(".."))

# Check if we are running on Read the Docs' servers.
read_the_docs_build = os.environ.get("READTHEDOCS", None) == "True"

# Check if sphinx_rtd_theme is available
try:
    import sphinx_rtd_theme  # noqa: F401

    has_sphinx_rtd_theme = True
except ImportError:
    has_sphinx_rtd_theme = False
    pass


# -- Project information -----------------------------------------------------

project = "donuts-python"
copyright = "2021-2022, Takahiro Ueda"  # noqa: A001
author = "Takahiro Ueda"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_autodoc_typehints",
]

if has_sphinx_rtd_theme:
    extensions.append("sphinx_rtd_theme")

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme" if has_sphinx_rtd_theme else "default"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']

# ----------------------------------------------------------------------------

if read_the_docs_build:
    subprocess.run(["invoke", "build"])  # noqa: S603, S607

# This hack is needed to suppress "WARNING: autodoc: failed to determine
# JavaObject id=oxx to be documented.the following exception was raised:
# 'JavaMember' object has no attribute 'rpartition'".
import donuts  # noqa: E402

donuts.Polynomial._Polynomial__RAW_ZERO = None  # type: ignore
donuts.RationalFunction._RationalFunction__RAW_ZERO = None  # type: ignore
