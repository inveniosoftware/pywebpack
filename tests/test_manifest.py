# -*- coding: utf-8 -*-
#
# This file is part of PyWebpack
# Copyright (C) 2017 CERN.
# Copyright (C) 2017 Anders Kaseorg.
#
# PyWebpack is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Module tests."""

import pytest

from pywebpack import (
    InvalidManifestError,
    Manifest,
    ManifestEntry,
    ManifestLoader,
    UnfinishedManifestError,
    UnsupportedExtensionError,
    WebpackBundleTrackerFactory,
    WebpackManifestFactory,
    WebpackYamFactory,
)


@pytest.fixture()
def exmanif():
    m = Manifest()
    m.add(ManifestEntry("script", ["/a.js", "/b.js"]))
    m.add(ManifestEntry("styles", ["/a.css", "/b.css"]))
    return m


def test_render(exmanif):
    """Test rendering."""

    assert (
        exmanif.script.render()
        == exmanif["script"].render()
        == str(exmanif.script)
        == '<script src="/a.js"></script>'
        '<script src="/b.js"></script>'
    )
    assert (
        exmanif.styles.render()
        == exmanif["styles"].render()
        == '<link rel="stylesheet" href="/a.css" />'
        '<link rel="stylesheet" href="/b.css" />'
    )


def test_manifest_add_same_name():
    """Test add with same name."""
    m = Manifest()
    m.add(ManifestEntry("script", ["/a.js"]))
    pytest.raises(KeyError, m.add, ManifestEntry("script", ["/b.js"]))


def test_nonexisting_entry():
    """Test non-existing entry."""
    m = Manifest()
    pytest.raises(AttributeError, getattr, m, "script")
    pytest.raises(KeyError, m.__getitem__, "script")


def test_invalid_ext():
    """Test invalid entry ext."""
    m = Manifest()
    m.add(ManifestEntry("script", ["/a.exe"]))
    pytest.raises(UnsupportedExtensionError, m.script.render)


def test_factory(bundletracker_path, yam_path, manifest_path):
    """Test factories."""
    m = WebpackBundleTrackerFactory().load(bundletracker_path)
    assert m["app.js"]
    assert m["app.css"]
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
        bundletracker_invalid_path,
    )
    pytest.raises(UnfinishedManifestError, WebpackYamFactory().load, yam_invalid_path)


def test_iter_manifest(exmanif):
    assert {m.name for m in exmanif} == {"script", "styles"}


def test_iter_manifest_entry(exmanif):
    assert {p for p in exmanif.script} == {"/a.js", "/b.js"}
