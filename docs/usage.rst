Usage
=====

A simple example
----------------

Let's take a simple ``package.json``::

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

Let's add to it a run script that executes webpack::

    "scripts": {
      "build": "webpack --config webpack.config.js"
    }

And the corresponding ``webpack.config.js``::

    var path = require('path');

    module.exports = {
      context: path.resolve(__dirname, 'src'),
      entry: './index.js',
      output: {
        filename: '[name].js',
        path: path.resolve(__dirname, 'dist')
      }
    };

We can easily wrap our project in a :class:`~pywebpack.project.WebpackProject` object::

    from pywebpack.project import WebpackProject
    project = WebpackProject('.')

This will allow us to install the dependencies::

    project.install()

And invoke webpack to build the assets::

    project.build()

Alternative, :meth:`~pywebpack.project.WebpackProject.buildall` can be used to execute both tasks at once.


Using a manifest
----------------

Manifests help you deal with long-term caching, by providing a mapping between the name of a resource and its "hashed"
version::

    {
      "main.js": "main.75244bb780acd727ebd3.js"
    }

This package supports manifest files that are compatible with `webpack-manifest-plugin`_, `webpack-yam-plugin`_ and
`webpack-bundle-tracker`_.

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

:class:`~pywebpack.manifests.ManifestLoader` should be able to load a manifest in any of those formats::

    manifest = ManifestLoader.load('/path/to/dist/manifest.json')

The manifest entries can be retrieved as object attributes or items::

    manifest.myresource
    manifest['myresource']
    manifest['main.js']


.. _webpack-manifest-plugin: https://www.npmjs.com/package/webpack-manifest-plugin
.. _webpack-yam-plugin: https://www.npmjs.com/package/webpack-yam-plugin
.. _webpack-bundle-tracker: https://www.npmjs.com/package/webpack-bundle-tracker
