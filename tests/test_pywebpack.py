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

from pywebpack import WebpackBundle, WebpackBundleProject, WebpackProject, \
    WebpackTemplateProject


def json_from_file(filepath):
    """Load JSON from file."""
    with open(filepath) as fp:
        return json.load(fp)


def test_version():
    """Test version import."""
    from pywebpack import __version__
    assert __version__


def test_project(simpleprj):
    """Test extension initialization."""
    project = WebpackProject(simpleprj)
    assert exists(project.project_path)

    node_modules = join(project.project_path, 'node_modules')
    bundlejs = join(project.project_path, 'dist/bundle.js')

    assert not exists(node_modules)
    project.install()
    assert exists(node_modules)

    assert not exists(bundlejs)
    project.build()
    assert exists(bundlejs)


def test_project_buildall(simpleprj):
    """Test build all."""
    project = WebpackProject(simpleprj)
    project.buildall()
    assert exists(join(project.project_path, 'node_modules'))
    assert exists(join(project.project_path, 'dist/bundle.js'))


def test_templateproject_create(templatedir, destdir):
    """Test template project creation."""
    project = WebpackTemplateProject(destdir, project_template=templatedir)
    assert not exists(project.npmpkg.package_json_path)
    project.create()
    assert exists(project.npmpkg.package_json_path)


def test_templateproject_clean(templatedir, destdir):
    """Test template project creation."""
    project = WebpackTemplateProject(destdir, project_template=templatedir)
    project.create()
    assert exists(project.project_path)
    project.clean()
    assert not exists(project.project_path)


def test_templateproject_create_config(templatedir, destdir):
    """Test template project creation."""
    expected_config = {'entry': './index.js'}

    project = WebpackTemplateProject(
        destdir,
        project_template=templatedir,
        config=lambda: expected_config,
    )

    assert not exists(project.config_path)
    project.create()
    assert json_from_file(project.config_path) == expected_config


def test_tempateproject_buildall(templatedir, destdir):
    """Test build all."""
    project = WebpackTemplateProject(
        destdir,
        config={'test': True},
        config_path='build/config.json',
        project_template=templatedir
    )
    project.buildall()
    assert exists(project.config_path)
    assert exists(join(project.project_path, 'node_modules'))
    assert exists(join(project.project_path, 'dist/bundle.js'))


def test_bundleproject(builddir, bundledir, destdir):
    """Test bundle project."""
    entry = {'app': './index.js'}
    bundle = WebpackBundle(
        bundledir,
        entry=entry,
        dependencies={
            'lodash': '~4',
        }
    )
    project = WebpackBundleProject(
        destdir,
        project_template=builddir,
        bundles=(x for x in [bundle]),  # Test for iterator evaluation
        config={'test': True, 'entry': False},
    )

    assert project.bundles == [bundle]
    assert project.entry == entry
    assert project.config == {'entry': entry, 'test': True}
    assert project.dependencies == {
        'dependencies': {
            'lodash': '~4',
        },
        'devDependencies': {},
        'peerDependencies': {}
    }

    project.create()

    # Assert generated files.
    paths = [
        'config.json',
        'index.js',
        'package.json',
        'webpack.config.js'
    ]
    distpaths = [
        'dist/bundle.js',
        'node_modules',
    ]
    for p in paths:
        assert exists(join(project.project_path, p))
    for p in distpaths:
        assert not exists(join(project.project_path, p))

    # Assert generated package.json
    package_json = json_from_file(project.npmpkg.package_json_path)
    for k in ['dependencies', 'devDependencies', 'peerDependencies']:
        assert package_json[k] == project.dependencies[k]

    # Build project and see that it works.
    project.install()
    project.build()
    for p in distpaths:
        assert exists(join(project.project_path, p))
