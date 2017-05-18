# -*- coding: utf-8 -*-
#
# This file is part of PyWebpack
# Copyright (C) 2017 CERN.
#
# PyWebpack is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Pytest configuration."""

from __future__ import absolute_import, print_function

import shutil
import tempfile
from os import makedirs
from os.path import dirname, exists, join

import pytest


@pytest.yield_fixture()
def tmpdir():
    """Temporary directory."""
    path = tempfile.mkdtemp()
    yield path
    shutil.rmtree(path)


@pytest.fixture()
def sourcedir():
    """Get source dir for projects."""
    return join(dirname(__file__), 'projects')


@pytest.fixture()
def manifestsdir():
    """Get source dir for projects."""
    return join(dirname(__file__), 'manifests')


@pytest.fixture()
def templatedir(sourcedir):
    """Get source dir for projects."""
    return join(sourcedir, 'simple')


@pytest.fixture()
def builddir(sourcedir):
    """Get build dir for projects."""
    return join(sourcedir, 'buildtpl')


@pytest.fixture()
def bundledir(sourcedir):
    """Get build dir for projects."""
    return join(sourcedir, 'bundle')


@pytest.yield_fixture()
def destdir(tmpdir):
    """Get example output directory."""
    dst = join(tmpdir, 'simple')
    makedirs(dst)
    yield dst
    if exists(dst):
        shutil.rmtree(dst)


@pytest.fixture()
def simpleprj(templatedir, tmpdir):
    """Initialize simple webpack project."""
    dst = join(tmpdir, 'simple')
    shutil.copytree(templatedir, dst)
    return join(dst, 'package.json')


@pytest.fixture()
def brokenprj(sourcedir, tmpdir):
    """Initialize broken webpack project."""
    dst = join(tmpdir, 'broken')
    shutil.copytree(join(sourcedir, 'broken'), dst)
    return join(dst, 'package.json')


@pytest.fixture()
def bundletracker_path(manifestsdir):
    """Bundletracker manifest."""
    return join(manifestsdir, 'bundletracker.json')


@pytest.fixture()
def bundletracker_invalid_path(manifestsdir):
    """Bundletracker manifest."""
    return join(manifestsdir, 'bundletracker-invalid.json')


@pytest.fixture()
def yam_path(manifestsdir):
    """Bundletracker manifest."""
    return join(manifestsdir, 'yam.json')


@pytest.fixture()
def yam_invalid_path(manifestsdir):
    """Bundletracker manifest."""
    return join(manifestsdir, 'yam-invalid.json')


@pytest.fixture()
def manifest_path(manifestsdir):
    """webpack-manifest-plugin manifest."""
    return join(manifestsdir, 'manifest.json')
