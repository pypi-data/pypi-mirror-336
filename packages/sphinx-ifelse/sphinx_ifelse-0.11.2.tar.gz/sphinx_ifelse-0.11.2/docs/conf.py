"""sphinx-ifelse documentation build configuration file"""

import os
import datetime

# -- Print Versions ------------------------------------------------------

from sphinx import __version__ as sphinx_version
print ('sphinx version: ' + str(sphinx_version))

from sphinx_ifelse import __version__ as sphinx_ifelse_version
print ('sphinx_ifelse version: ' + str(sphinx_ifelse_version))

from sphinx_needs import __version__ as sphinx_needs_version
print ('sphinx-needs version: ' + str(sphinx_needs_version))

# -- General configuration ------------------------------------------------

# General information about the project.
project = "Sphinx-IfElse"
now = datetime.datetime.now()
copyright = f"2025-{now.year}, X-As-Code"
author = "X-As-Code"

master_doc = "index"
language = "en"

version = release = sphinx_ifelse_version

# -- General configuration
on_rtd = os.environ.get("READTHEDOCS") == "True"

extensions = [
   "sphinx_ifelse",
   "sphinx_needs",
   "sphinx.ext.autodoc",
   "sphinxcontrib.test_reports",
]

html_static_path = ['_static']

# -- extension configuration: ifelse

ifelse_variants = {
   'html': True,
   'latex': False,
   'pdf': False,
   'epub': False,
   'l1': 3,
   'l2': 3,
   'l3': 3,
}

# -- extension configuration: sphinx-needs

needs_build_json = True
