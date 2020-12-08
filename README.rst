===========
 PyWebpack
===========

.. image:: https://github.com/inveniosoftware/pywebpack/workflows/CI/badge.svg
        :target: https://github.com/inveniosoftware/pywebpack/actions?query=workflow%3ACI

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
  can define what goes in the config e.g. let webpack know about output paths or
  dynamic entry points.
* **Collect bundles:** If your Webpack project is spread over multiple Python
  packages, PyWebpack can help you dynamically assemble the files into a
  Webpack project. This is useful if you don't know until build time which
  packages are installed.

Further documentation is available on
https://pywebpack.readthedocs.io/
