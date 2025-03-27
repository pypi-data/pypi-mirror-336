# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'phystool'
author = 'Jérome Dufour'

release = '0.1'
version = '0.1.0'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
]

import os, sys
sys.path.insert(0, os.path.abspath(os.path.join("..", "..", "src")))
