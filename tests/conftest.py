# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2017 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Pytest configuration."""

from __future__ import absolute_import, print_function

import json
import shutil
import tempfile
from os import makedirs
from os.path import dirname, exists, join

import pkg_resources
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
    """Example output directory."""
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
