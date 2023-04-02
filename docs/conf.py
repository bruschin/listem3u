#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
""" Created on 25 mars 2023

  @author: Nicolas Bruschi
  
  Configuration file for the Sphinx documentation builder.

  This file only contains a selection of the most common options. For a full
  list see the documentation:
  https://www.sphinx-doc.org/en/master/usage/configuration.html
  pip install sphinx-multiversion gitpython --user
  
  [Autres refs] :
  https://blog.stephane-robert.info/post/sphinx-documentation-multi-version/
  https://github.com/maltfield/rtd-github-pages
  
"""
# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

import os
import sys
from git import Repo

sys.path.insert(0, os.path.abspath('../src/'))


# -- Project information -----------------------------------------------------
# pylint: disable=invalid-name
project = 'listem3u'
# pylint: disable=invalid-name,redefined-builtin
copyright = '2023, 😀 Nicolas Bruschi'
# pylint: disable=invalid-name
author = 'Nicolas Bruschi'

# The full version, including alpha/beta/rc tags
release = 'V1.4 b'

# avant lancement : export TZ="Europe/Paris" sinon UTC
#today_fmt = '%Y-%b-%d at %H:%M'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
"""
extensions = [  'sphinx_rtd_theme','sphinx.ext.todo', 'sphinx.ext.autodoc',\
                'sphinx.ext.autosummary', 'sphinx.ext.intersphinx',\
                'sphinx.ext.mathjax', 'sphinx.ext.viewcode',\
                'sphinx.ext.graphviz', 'sphinx.ext.napoleon' ,\
                'sphinx_multiversion',\
              ]
"""
extensions = [  'sphinx_rtd_theme', 'sphinx.ext.autodoc',\
                'sphinx.ext.autosummary', 'sphinx.ext.viewcode',\
                'sphinx.ext.githubpages', 'sphinx.ext.graphviz',\
                'sphinx_multiversion', 'sphinx.ext.autodoc',\
]



# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'fr'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
#html_theme = 'alabaster'
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_logo = 'listem3u.png'
html_favicon = 'listem3u.ico'
html_last_updated_fmt = '%d %b %Y à %H:%M'

numfig = True

autosummary_generate = True
# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'listem3u'


# -- Options for LaTeX output ------------------------------------------------

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
  (master_doc, 'listem3u.tex', 'listem3u Documentation', \
    [author], 'manual'),]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
  (master_doc, 'listem3u', 'listem3u Documentation', \
    [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
  (master_doc, 'listem3u', 'listem3u Documentation', \
    author, 'listem3u', 'Doc forge logicielle.', \
    'Miscellaneous'),
]


# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']


# -- Extension configuration -------------------------------------------------

# add sourcecode to path
#sys.path.insert(0, os.path.abspath('..'))

############################
# SETUP THE RTD LOWER-LEFT #
############################
try:
  # pylint: disable=used-before-assignment
  html_context
except NameError:
  html_context = dict()
html_context['display_lower_left'] = True

if 'REPO_NAME' in os.environ:
  REPO_NAME = os.environ['REPO_NAME']
else:
  REPO_NAME = 'https://bruschin.github.io/listem3u'

html_context['namenic'] = 'https://bruschin.github.io/listem3u'

# SET CURRENT_LANGUAGE
if 'current_language' in os.environ:
  # get the current_language env var set by buildDocs.sh
  current_language = os.environ['current_language']
else:
  # the user is probably doing `make html`
  # set this build's current language to english
  current_language = 'fr'

#html_context['display_lower_left'] =
# # tell the theme which language to we're currently building
#html_context['current_language'] = current_language

# SET CURRENT_VERSION

repo = Repo( search_parent_directories=True )
#current_language = language

if 'current_version' in os.environ:
  # get the current_version env var set by buildDocs.sh
  current_version = os.environ['current_version']
else:
  # the user is probably doing `make html`
  # set this build's current version by looking at the branch
  current_version = repo.active_branch.name

# tell the theme which version we're currently on ('current_version' affects
# the lower-left rtd menu and 'version' affects the logo-area version)
html_context['current_version'] = current_version
html_context['version'] = current_version

# POPULATE LINKS TO OTHER LANGUAGES
html_context['languages'] = []
html_context['languages'] = [ ( f'{current_language}', f'{REPO_NAME}' ) ]

# html_context['languages'] = []
# languages = [lang.name for lang in os.scandir('locales') if lang.is_dir()]
# for lang in languages:
#   html_context['languages'].append( (f'{lang}', f'{REPO_NAME}/'\
# f'{lang}/{current_version}/') )


# POPULATE LINKS TO OTHER VERSIONS
html_context['versions'] = []
versions = [branch.name for branch in repo.branches]
for version in versions:
  html_context['versions'].append( (f'{version}', f'{REPO_NAME}/'\
f'{current_language}/{version}/') )

# POPULATE LINKS TO OTHER FORMATS/DOWNLOADS

# settings for creating PDF with rinoh
#rinoh_documents = [(f'{master_doc}', 'target', f'{project} Documentation',
#  f'© {copyright}',)]

### mise à l'heure de index.rst
# avant lancement : export TZ="Europe/Paris" sinon UTC
today_fmt = '%Y %b %d à %H:%M'
#today_fmt = "%B %d, %Y"

# settings for EPUB
epub_basename = f'{project}-docs_{current_language}_{current_version}'

html_context['downloads'] = []

#html_context['downloads'].append( ('pdf', f'{REPO_NAME}/'\
#f'{project}-docs_{current_language}_{current_version}.pdf') )

html_context['downloads'].append( ('epub', f'{REPO_NAME}/'\
f'{epub_basename}.epub') )

##########################
# "EDIT ON GITHUB" LINKS #
##########################

html_context['display_github'] = True
html_context['github_user'] = 'maltfield'
html_context['github_repo'] = 'rtd-github-pages'
html_context['github_version'] = 'master/docs/'
