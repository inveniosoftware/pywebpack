# -*- coding: utf-8 -*-
#
# This file is part of PyWebpack
# Copyright (C) 2017 CERN.
#
# PyWebpack is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

r"""Webpack integration layer for Python.

A simple example
----------------

Let's take a simple ``package.json`` that includes a Node module::

    {
      "private": true,
      "name": "example",
      "version": "0.0.1",
      "author": "myself",
      "license": "WTFPL",
      "description": "example",
      "dependencies": {
        "jquery": "^3.2.1"
      }
    }

And let's create a Webpack configuration file ``webpack.config.js`` to load the
entry point ``src/index.js`` and output the built version in the ``dist``
folder::

    var path = require('path');

    module.exports = {
      context: path.resolve(__dirname, 'src'),
      entry: './index.js',
      output: {
        filename: '[name].js',
        path: path.resolve(__dirname, 'dist')
      }
    };

Now, let's add to the ``packages.json`` a run script ``build`` that executes
webpack::

    "scripts": {
      "build": "webpack --config webpack.config.js"
    }

We can easily wrap our project in a :class:`~pywebpack.project.WebpackProject`
object::

    from pywebpack.project import WebpackProject
    project_path = '.'
    project = WebpackProject(project_path)

This will allow us to install the ``npm`` dependencies::

    project.install()

And invoke the ``npm`` ``build`` command to execute ``webpack`` to build the
entry points::

    project.build()

Alternative, :meth:`~pywebpack.project.WebpackProject.buildall` can be used to
execute both tasks at once.

Build time config
-----------------

If we need to inject extra configuration at build time we can define a
:class:`~pywebpack.project.WebpackTemplateProject`::

    from pywebpack.bundle import WebpackTemplateProject
    project = WebpackTemplateProject(
        working_dir='tmp',  # where config and assets files will be copied
        project_template_dir='buildconfig',  # `webpack.config.js` location
        config={'debug': True},
        config_path='build/config.json',
    )

``debug: True`` is an example of configuration that can be injected from Python
and expose it to Webpack via the generated ``config.json``.

Assets for multiple modules
---------------------------

It is a common practice to split your assets in several files to decrease
assets file sizes and speed up webpage loading. Pywebpack lets you define a
project that can have bundles, which are definitions of assets and npm
dependencies.

The recommended folder structure for a project with modules is the following::

    /buildconfig
        /package.json
        /webpack.config.js
    /modules
        /module1
            /...
            /static
                /js
                /css
        /module2
            /...
            /static
                /js
                /css
    main.py  # or any script name

Pywebpack will copy all bundles static files in the same working directory.
It is **important** to name assets with distinct filenames, or create a
namespaced subfolder to contain your static files, so that name collisions
will be avoided.

In our main script, let's add two bundles (called ``mainsite`` and
``backoffice``)::

    from pywebpack.bundle import WebpackBundle
    mainsite = WebpackBundle(
        './modules/mainsite/static',
        entry={
            'mainsite-base': './js/mainsite-base.js',
            'mainsite-products': './js/mainsite-products.js',
        },
        dependencies={
            'jquery': '^3.2.1'
        }
    )

    backoffice = WebpackBundle(
        './modules/backoffice/static',
        entry={
            'backoffice-base': './js/backoffice-base.js',
            'backoffice-admin': './js/backoffice-admin.js',
        },
        dependencies={
            'jquery': '^3.1.0'
        }
    )

A :class:`~pywebpack.bundle.WebpackBundle` requires the path to the static
files of the module, an entry for each asset with its relative path and any
extra npm package.

Then, we create a project :class:`~pywebpack.project.WebpackBundleProject`
for our bundles::

    from pywebpack.project import WebpackBundleProject
    project = WebpackBundleProject(
        working_dir='build',  # where config and assets files will be copied
        project_template_dir='buildconfig',  #`webpack.config.js` location
        bundles=[mainsite, backoffice]
    )

Pywebpack will generate a ``config.json`` which will contain all the assets
with their paths. Each bundle entry will be a `webpack entry`_.

As last step, in our ``webpack.config.js``, we set the entry to the
``config.json`` so webpack will build each asset::

    var path = require('path');
    var config = require('./config')

    module.exports = {
        context: path.resolve(__dirname),
        entry: config.entry,
        output: {
            filename: '[name].js',
            path: path.resolve(__dirname, 'dist')
        }
    };

When executing ``project.buildall()``, Pywebpack will copy all the files
contained in the ``project_template_dir`` folder and all the assets of each
bundle to the ``working_dir`` folder. Then, it will install ``npm`` packages
and run ``webpack`` to build the assets.

Node dependencies resolution
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Bundles can declare extra npm packages needed to build the assets. Pywebpack
supports ``dependencies``, ``devDependencies`` and ``peerDependencies``.

Dependencies will be merged to a common list. In case the same dependency is
defined multiple times with different version, only the highest version that
satisfies all of them is kept. For more information, see the documentation of
`node-semver`_.

Extension points
----------------

With Pywebpack, we can "expose" bundles of our module so we can dynamically
build assets of other installed modules.

Let's define a module and expose it as an entry point. In
``mymodule.bundles.py``::

    from pywebpack.bundle import WebpackBundle
    css = WebpackBundle(
        __name__,
        entry={
            'mymodule-styles': './js/mymodule/styles.css',
        },
        dependencies={
            'bootstrap-sass': '~3.3.5',
            'font-awesome': '~4.4.0',
        }
    )

And in ``setup.py``::

    setup(
        ...
        entry_points={
            ...
            'webpack_bundles': [
                'mymodule_css = mymodule.bundles:css',
                'mymodule_js = mymodule.bundles:js',
            ],
    )

In our main project, we can now define a
:class:`~pywebpack.project.WebpackBundleProject` that dynamically uses the
installed and exposed bundles::

    from pywebpack import bundles_from_entry_point
    from pywebpack.project import WebpackBundleProject
    project = WebpackBundleProject(
        __name__,
        project_folder='assets',
        config_path='build/config.json',
        bundles=bundles_from_entry_point('mymodule.webpack_bundles'),
    )

When executing ``project.buildall()``, the bundles exposed as entry points will
be collected and built.

Manifest
--------

A manifest is the output file created by ``webpack`` which contains the list of
all generated assets.
It also helps you deal with long-term caching, by providing a mapping between
the name of a resource and its "hashed" version::

    {
      "main.js": "main.75244bb780acd727ebd3.js"
    }

Pywebpack can parse the manifest file and make it available to your python
project. It supports manifest files generated using `webpack-manifest-plugin`_,
`webpack-yam-plugin`_ and `webpack-bundle-tracker`_.

You will normally want webpack to add a hash of a file's contents to its name::

    output: {
      filename: '[name].[chunkhash].js',
      path: path.resolve(__dirname, 'dist')
    }

And then have it invoke your favorite manifest plugin::

    plugins: [
      new ManifestPlugin({
        fileName: 'manifest.json'
      })
    ]

:class:`~pywebpack.manifests.ManifestLoader` should be able to load a manifest
in any of those formats::

    manifest = ManifestLoader.load('/path/to/dist/manifest.json')

The manifest entries can be retrieved as object attributes or items::

    manifest.myresource
    manifest['main.js']
    manifest['myresource']

.. _webpack entry: https://webpack.js.org/concepts/#entry
.. _node-semver: https://pypi.org/project/node-semver/
.. _webpack-manifest-plugin:
        https://www.npmjs.com/package/webpack-manifest-plugin
.. _webpack-yam-plugin:
        https://www.npmjs.com/package/webpack-yam-plugin
.. _webpack-bundle-tracker:
        https://www.npmjs.com/package/webpack-bundle-tracker

"""

from __future__ import absolute_import, print_function

from .bundle import WebpackBundle
from .helpers import bundles_from_entry_point
from .manifests import Manifest, ManifestEntry, ManifestLoader, \
    WebpackManifestFactory, WebpackYamFactory, WebpackBundleTrackerFactory, \
    ManifestError, InvalidManifestError, UnfinishedManifestError,  \
    UnsupportedExtensionError, UnsupportedManifestError
from .project import WebpackProject, WebpackTemplateProject, \
    WebpackBundleProject
from .storage import FileStorage, LinkStorage
from .version import __version__

__all__ = (
    '__version__',
    'bundles_from_entry_point',
    'FileStorage',
    'InvalidManifestError',
    'LinkStorage',
    'Manifest',
    'ManifestEntry',
    'ManifestError',
    'ManifestLoader',
    'UnfinishedManifestError',
    'UnsupportedExtensionError',
    'UnsupportedManifestError',
    'WebpackBundle',
    'WebpackBundleProject',
    'WebpackBundleTrackerFactory',
    'WebpackManifestFactory',
    'WebpackProject',
    'WebpackTemplateProject',
    'WebpackYamFactory',
)
