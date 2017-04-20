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

"""Module tests."""

from __future__ import absolute_import, print_function

import json
from os.path import exists, join

import pytest

from pywebpack import InvalidManifestError, Manifest, ManifestEntry, \
    ManifestError, ManifestLoader, UnfinishedManifestError, \
    UnsupportedExtensionError, WebpackBundleTrackerFactory, \
    WebpackManifestFactory, WebpackYamFactory


def test_render():
    """Test rendering."""
    m = Manifest()
    m.add(ManifestEntry('script', ['/a.js', '/b.js']))
    m.add(ManifestEntry('styles', ['/a.css', '/b.css']))

    assert m.script.render() == m['script'].render() == str(m.script) == \
        '<script src="/a.js"></script>' \
        '<script src="/b.js"></script>'
    assert m.styles.render() == m['styles'].render() == \
        '<link rel="stylesheet" href="/a.css"></link>' \
        '<link rel="stylesheet" href="/b.css"></link>'


def test_manifest_add_same_name():
    """Test add with same name."""
    m = Manifest()
    m.add(ManifestEntry('script', ['/a.js']))
    pytest.raises(KeyError, m.add, ManifestEntry('script', ['/b.js']))


def test_nonexisting_entry():
    """Test non-existing entry."""
    m = Manifest()
    pytest.raises(AttributeError, getattr, m, 'script')
    pytest.raises(KeyError, m.__getitem__, 'script')


def test_invalid_ext():
    """Test invalid entry ext."""
    m = Manifest()
    m.add(ManifestEntry('script', ['/a.exe']))
    pytest.raises(UnsupportedExtensionError, m.script.render)


def test_factory(bundletracker_path, yam_path, manifest_path):
    """Test factories."""
    m = WebpackBundleTrackerFactory().load(bundletracker_path)
    assert m.app
    m = WebpackYamFactory().load(yam_path)
    assert m.app
    WebpackManifestFactory().load(manifest_path)
    assert m.app

    for p in [bundletracker_path, yam_path, manifest_path]:
        ManifestLoader().load(p)
        assert m.app


def test_factory_invalid(bundletracker_invalid_path, yam_invalid_path):
    """Test invalid manifests."""
    pytest.raises(
        InvalidManifestError,
        WebpackBundleTrackerFactory().load,
        bundletracker_invalid_path
    )
    pytest.raises(
        UnfinishedManifestError,
        WebpackYamFactory().load,
        yam_invalid_path
    )
