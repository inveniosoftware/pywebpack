# -*- coding: utf-8 -*-
#
# This file is part of PyWebpack
# Copyright (C) 2017 CERN.
#
# PyWebpack is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Webpack integration layer for Python."""

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
