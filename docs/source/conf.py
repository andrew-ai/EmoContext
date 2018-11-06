#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Topic Clustering documentation build configuration file, created by
# sphinx-quickstart on Mon Dec 11 10:38:38 2017.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from pathlib import Path
p = Path(__file__).absolute().parent.parent.parent
for i in p.glob("**/src"):
    sys.path.append(str(i.absolute()))

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc', 'sphinx.ext.autosummary',
    'numpydoc'
]


# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = ['.rst', ".inc"]

# The master toctree document.
master_doc = 'index'

# Read information from the config file

config_info = dict()

with open(str(p / "config.mk")) as f:
    for l in f:
        l_ = l.split("=")
        config_info[l_[0].strip()] = l_[1].strip()
# General information about the project.
project = config_info.get("PROJECT_NAME_DOC", "{Project name}")
copyright = config_info.get("COPYRIGHT_DOC", "D2D CRC Ltd.")
author = 'D2D CRC Ltd.'
description = config_info.get("DESCRIPTION_DOC", "{Project name}")

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = '0.0.1'
# The full version, including alpha/beta/rc tags.
release = '0.0.1'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


numpydoc_show_class_members = False

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'bizstyle'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

autosummary_generate = True


# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "".join(project.split()) + "doc"


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, "".join(project.split()) + ".tex",  project + ' Documentation',
     'D2D CRC Ltd.', 'manual'),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, "".join(project.lower().split()),  project + ' Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, "".join(project.split()), project + ' Documentation',
     author, "".join(project.split()), 'One line description of project.',
     'Miscellaneous'),
]


# create api docs
public_api = """
Public API
==========
"""

dev_api = """
Development API
===============
"""

api_format = """

.. automodule:: {}
        :members:

"""


from setuptools import PEP420PackageFinder

pkgs = PEP420PackageFinder.find(str(p / "src"))

print("***********************************************")
print(len(pkgs))
print(str(p))
for pk in pkgs:
    print(pk)

has_public = False
has_dev = False

for i in pkgs:
    if config_info.get("PACKAGE", "d2d.test") not in i:
        continue
    if "dev" not in i:
        has_public = True

    if "dev" in i:
        has_dev = True

if has_public:
    with open("public_api.rst", "wt") as f:
        f.write(public_api)
        for i in pkgs:
            if config_info.get("PACKAGE", "d2d.test") not in i:
                continue
            if "dev" not in i:
                f.write(i + "\n")
                f.write("~" * len(i) + "\n")
                f.write(api_format.format(i))

                pp = p / "src" / os.path.sep.join(i.split("."))
                for pf in pp.glob("*.py"):
                    if not pf.stem.startswith("__"):
                        api = i + "." + pf.stem
                        f.write(api + "\n")
                        f.write("~" * len(api) + "\n")
                        f.write(api_format.format(api))


if has_dev:
    with open("dev_api.rst", "wt") as f:
        f.write(dev_api)
        for i in pkgs:
            if config_info.get("PACKAGE", "d2d.test") not in i:
                continue
            if "dev" in i:
                f.write(i + "\n")
                f.write("~" * len(i) + "\n")
                f.write(api_format.format(i))

                pp = p / "src" / os.path.sep.join(i.split("."))
                for pf in pp.glob("*.py"):
                    if not pf.stem.startswith("__"):
                        api = i + "." + pf.stem
                        f.write(api + "\n")
                        f.write("~" * len(api) + "\n")
                        f.write(api_format.format(api))


with open("index.inc") as f:
    index = f.read()

with open("index.rst", "wt") as f:
    pub = "public_api" if has_public else ""
    dev = "dev_api" if has_dev else ""
    f.write(index.format(config_info.get("PROJECT_NAME_DOC"), pub, dev))