..
    This file is part of Invenio.
    Copyright (C) 2017 CERN.

    Invenio is free software; you can redistribute it
    and/or modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation; either version 2 of the
    License, or (at your option) any later version.

    Invenio is distributed in the hope that it will be
    useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Invenio; if not, write to the
    Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
    MA 02111-1307, USA.

    In applying this license, CERN does not
    waive the privileges and immunities granted to it by virtue of its status
    as an Intergovernmental Organization or submit itself to any jurisdiction.

===========
 PyWebpack
===========

.. image:: https://img.shields.io/travis/inveniosoftware/pywebpack.svg
        :target: https://travis-ci.org/inveniosoftware/pywebpack

.. image:: https://img.shields.io/coveralls/inveniosoftware/pywebpack.svg
        :target: https://coveralls.io/r/inveniosoftware/pywebpack

.. image:: https://img.shields.io/github/tag/inveniosoftware/pywebpack.svg
        :target: https://github.com/inveniosoftware/pywebpack/releases

.. image:: https://img.shields.io/pypi/dm/pywebpack.svg
        :target: https://pypi.python.org/pypi/pywebpack

.. image:: https://img.shields.io/github/license/inveniosoftware/pywebpack.svg
        :target: https://github.com/inveniosoftware/pywebpack/blob/master/LICENSE

Webpack integration layer for Python.

**Using Flask?** Check out
`Flask-WebpackExt <https://flask-webpackext.readthedocs.io>`_.

PyWebpack makes it easy to interface with your existing Webpack project and
does not try to manage Webpack for you. PyWebpack does this via:

* **Manifests**: You tell Webpack to write a ``manifest.json`` using plugins
  such as `webpack-manifest-plugin
  <https://www.npmjs.com/package/webpack-manifest-plugin>`_,
  `webpack-yam-plugin
  <https://www.npmjs.com/package/webpack-yam-plugin>`_ or
  `webpack-bundle-tracker
  <https://www.npmjs.com/package/webpack-bundle-tracker>`_. PyWebpack
  reads the manifest and makes your compiled assets available to your template
  engine such as Jinja.
* **API for NPM**: PyWebpack provides an API so that e.g. ``project.install()``
  will run ``npm install`` in your Webpack project.

Optionally you can use PyWebpack to also:

* **Inject configuration:** PyWebpack will write a ``config.json`` into
  your webpack project, which you can import in your webpack configuration. You
  define what goes in the config, but you can use to let e.g. Webpack know
  about output paths or dynamic entry points.
* **Collect bundles:** If you Webpack project is spread over multiple Python
  packages, PyWebpack can help you dynamically assemble the files into a
  Webpack project. This is useful if you don't know until runtime which
  packages are installed.
