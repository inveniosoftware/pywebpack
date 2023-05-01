# -*- coding: utf-8 -*-
#
# This file is part of PyWebpack
# Copyright (C) 2017 CERN.
#
# PyWebpack is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Pytest configuration."""

import shutil
import subprocess
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
    return join(dirname(__file__), "projects")


@pytest.fixture()
def manifestsdir():
    """Get source dir for projects."""
    return join(dirname(__file__), "manifests")


@pytest.fixture()
def templatedir(sourcedir):
    """Get source dir for projects."""
    return join(sourcedir, "simple")


@pytest.fixture()
def builddir(sourcedir):
    """Get build dir for projects."""
    return join(sourcedir, "buildtpl")


@pytest.fixture()
def bundledir(sourcedir):
    """Get build dir for bundle."""
    return join(sourcedir, "bundle")


@pytest.fixture()
def bundledir2(sourcedir):
    """Get build dir for bundle."""
    return join(sourcedir, "bundle2")


@pytest.yield_fixture()
def destdir(tmpdir):
    """Get example output directory."""
    dst = join(tmpdir, "simple")
    makedirs(dst)
    yield dst
    if exists(dst):
        shutil.rmtree(dst)


@pytest.fixture()
def simpleprj(templatedir, tmpdir):
    """Initialize simple webpack project."""
    dst = join(tmpdir, "simple")
    shutil.copytree(templatedir, dst)
    return join(dst, "package.json")


@pytest.fixture()
def brokenprj(sourcedir, tmpdir):
    """Initialize broken webpack project."""
    dst = join(tmpdir, "broken")
    shutil.copytree(join(sourcedir, "broken"), dst)
    return join(dst, "package.json")


@pytest.fixture()
def bundletracker_path(manifestsdir):
    """Bundletracker manifest."""
    return join(manifestsdir, "bundletracker.json")


@pytest.fixture()
def bundletracker_invalid_path(manifestsdir):
    """Bundletracker manifest."""
    return join(manifestsdir, "bundletracker-invalid.json")


@pytest.fixture()
def yam_path(manifestsdir):
    """Bundletracker manifest."""
    return join(manifestsdir, "yam.json")


@pytest.fixture()
def yam_invalid_path(manifestsdir):
    """Bundletracker manifest."""
    return join(manifestsdir, "yam-invalid.json")


@pytest.fixture()
def manifest_path(manifestsdir):
    """webpack-manifest-plugin manifest."""
    return join(manifestsdir, "manifest.json")


@pytest.fixture(autouse=True, scope="session")
def check_webpack_installation():
    """Check if Webpack is installed locally or globally."""
    command = "npm list {where} {pkg}"

    # webpack and webpack-cli must be installed both globally or locally
    same_scope = dict(globally=[], locally=[])
    for where, scope in [("-g", "globally"), ("", "locally")]:
        for pkg in ["webpack", "webpack-cli"]:
            # check local installation
            cmd = command.format(where=where, pkg=pkg)
            try:
                subprocess.check_call(cmd.split(" "))
            except subprocess.CalledProcessError as exc:
                same_scope[scope].append(1)
            else:
                same_scope[scope].append(0)

    if sum(same_scope["globally"]) != 0 and sum(same_scope["locally"]) != 0:
        raise RuntimeError("webpack and webpack-cli must be installed.")
