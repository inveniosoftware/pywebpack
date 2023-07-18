# -*- coding: utf-8 -*-
#
# This file is part of PyWebpack
# Copyright (C) 2017-2020 CERN.
# Copyright (C) 2020 Cottage Labs LLP.
#
# PyWebpack is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Module tests."""

import json
import os
from os.path import exists, join

import pytest

from pywebpack import (
    WebpackBundle,
    WebpackBundleProject,
    WebpackProject,
    WebpackTemplateProject,
)
from pywebpack.errors import MergeConflictError
from pywebpack.helpers import max_version, merge_deps


def json_from_file(filepath):
    """Load JSON from file."""
    with open(filepath) as fp:
        return json.load(fp)


def test_version():
    """Test version import."""
    from pywebpack import __version__

    assert __version__


@pytest.mark.parametrize(
    "v1,v2,expected",
    [
        ("1", "1", "1"),
        ("1", "2", "2"),
        ("2", "1", "2"),
        ("1.0", "1.1", "1.1"),
        ("2.3", "2.1", "2.3"),
        ("2.3", "2", "2.3"),
        ("1.0.0", "1.0.1", "1.0.1"),
        ("1.0.0", "1.1.0", "1.1.0"),
        ("1.0.0", "1.1", "1.1"),
        ("1.0.0", "2.0.1", "2.0.1"),
        ("1.0.0-alpha", "1.0.0-alpha.1", "1.0.0-alpha.1"),
        ("1.0.0-alpha.1", "1.0.0-alpha.beta", "1.0.0-alpha.beta"),
        ("1.0.0-alpha.beta", "1.0.0-beta", "1.0.0-beta"),
        ("1.0.0-beta", "1.0.0-beta.2", "1.0.0-beta.2"),
        ("1.0.0-beta.2", "1.0.0-beta.11", "1.0.0-beta.11"),
        ("1.0.0-beta.11", "1.0.0-rc.1", "1.0.0-rc.1"),
        ("1.0.0-rc.1", "1.0.0", "1.0.0"),
    ],
)
def test_max_version(v1, v2, expected):
    assert max_version(v1, v2) == expected


@pytest.mark.parametrize(
    "target,source,expected",
    [
        ({}, {}, {"dependencies": {}, "devDependencies": {}, "peerDependencies": {}}),
        (
            {},
            {"dependencies": {"mypkg": "1.0"}},
            {
                "dependencies": {"mypkg": "1.0"},
                "devDependencies": {},
                "peerDependencies": {},
            },
        ),
        (
            {"dependencies": {"mypkg": "1.0"}},
            {"dependencies": {"mypkg": "1.1"}},
            {
                "dependencies": {"mypkg": "1.1"},
                "devDependencies": {},
                "peerDependencies": {},
            },
        ),
        (
            {"dependencies": {"mypkg": "0.0.1"}},
            {"dependencies": {"mypkg": "0.1.0"}},
            {
                "dependencies": {"mypkg": "0.1.0"},
                "devDependencies": {},
                "peerDependencies": {},
            },
        ),
        (
            {"dependencies": {"mypkg": "~2.0.1-alpha.1"}},
            {"dependencies": {"mypkg": "2.0.1-beta"}},
            {
                "dependencies": {"mypkg": "2.0.1-beta"},
                "devDependencies": {},
                "peerDependencies": {},
            },
        ),
        (
            {"dependencies": {"mypkg": "^2.0.1"}},
            {"dependencies": {"mypkg": "2.0.2"}},
            {
                "dependencies": {"mypkg": "2.0.2"},
                "devDependencies": {},
                "peerDependencies": {},
            },
        ),
        (
            {"dependencies": {"mypkg": "^3.3.1"}},
            {"dependencies": {"mypkg": "~3.2.1"}},
            {
                "dependencies": {"mypkg": "^3.3.1"},
                "devDependencies": {},
                "peerDependencies": {},
            },
        ),
    ],
)
def test_merge_deps(target, source, expected):
    assert merge_deps(target, source) == expected


def test_merge_deps_incompat_major():
    with pytest.raises(MergeConflictError):
        merge_deps(
            {"dependencies": {"mypkg": "3.3.1"}},
            {"dependencies": {"mypkg": "4.2.1"}},
        )


def test_project(simpleprj):
    """Test extension initialization."""
    project = WebpackProject(simpleprj)
    assert exists(project.project_path)

    node_modules = join(project.project_path, "node_modules")
    bundlejs = join(project.project_path, "dist/bundle.js")

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
    assert exists(join(project.project_path, "node_modules"))
    assert exists(join(project.project_path, "dist/bundle.js"))


def test_project_no_scripts(brokenprj):
    project = WebpackProject(brokenprj)
    with pytest.raises(RuntimeError):
        project.buildall()


def test_project_failed_build(simpleprj):
    # Remove a file necessary for the build
    os.unlink(os.path.join(os.path.dirname(simpleprj), "index.js"))
    project = WebpackProject(simpleprj)
    with pytest.raises(RuntimeError):
        project.buildall()


def test_templateproject_create(templatedir, destdir):
    """Test template project creation."""
    project = WebpackTemplateProject(destdir, project_template_dir=templatedir)
    assert not exists(project.npmpkg.package_json_path)
    project.create()
    assert exists(project.npmpkg.package_json_path)


def test_templateproject_clean(templatedir, destdir):
    """Test template project creation."""
    project = WebpackTemplateProject(destdir, project_template_dir=templatedir)
    project.create()
    assert exists(project.project_path)
    project.clean()
    assert not exists(project.project_path)


def test_templateproject_create_config(templatedir, destdir):
    """Test template project creation."""
    expected_config = {"entry": "./index.js"}

    project = WebpackTemplateProject(
        working_dir=destdir,
        project_template_dir=templatedir,
        config=lambda: expected_config,
    )

    assert not exists(project.config_path)
    project.create()
    assert json_from_file(project.config_path) == expected_config


def test_templateproject_buildall(templatedir, destdir):
    """Test build all."""
    project = WebpackTemplateProject(
        working_dir=destdir,
        project_template_dir=templatedir,
        config={"test": True},
        config_path="build/config.json",
    )
    project.buildall()
    assert exists(project.config_path)
    assert exists(join(project.project_path, "node_modules"))
    assert exists(join(project.project_path, "dist/bundle.js"))


def test_bundleproject(builddir, bundledir, destdir):
    """Test bundle project."""
    entry = {"app": "./index.js"}
    aliases = {"@app": "index.js"}
    bundle = WebpackBundle(
        bundledir,
        entry=entry,
        dependencies={
            "lodash": "~4",
        },
        aliases=aliases,
    )
    project = WebpackBundleProject(
        working_dir=destdir,
        project_template_dir=builddir,
        bundles=(x for x in [bundle]),  # Test for iterator evaluation
        config={"test": True, "entry": False},
    )

    assert project.bundles == [bundle]
    assert project.entry == entry
    assert project.config == {"entry": entry, "test": True, "aliases": aliases}
    assert project.dependencies == {
        "dependencies": {
            "lodash": "~4",
        },
        "devDependencies": {},
        "peerDependencies": {},
    }

    project.create()

    # Assert generated files.
    paths = ["config.json", "index.js", "package.json", "webpack.config.js"]
    distpaths = [
        "dist/bundle.js",
        "node_modules",
    ]
    for p in paths:
        assert exists(join(project.project_path, p))
    for p in distpaths:
        assert not exists(join(project.project_path, p))

    # Assert generated package.json
    package_json = json_from_file(project.npmpkg.package_json_path)
    # Coming from bundle
    assert package_json["dependencies"] == {"lodash": "~4"}
    # Coming from source package.json
    assert package_json["devDependencies"] == {"lodash": "~4"}
    assert package_json["peerDependencies"] == {}

    # Build project and see that it works.
    project.install()
    project.build()
    for p in distpaths:
        assert exists(join(project.project_path, p))


@pytest.mark.xfail(raises=RuntimeError)
def test_bundle_duplicated_entries(builddir, bundledir, bundledir2, destdir):
    """Test bundles with duplicated entries."""
    bundle1 = WebpackBundle(
        bundledir,
        entry={"app": "./index.js"},
        dependencies={
            "lodash": "~4",
        },
    )
    bundle2 = WebpackBundle(
        bundledir2,
        entry={"app": "./main.js"},
        dependencies={
            "lodash": "~3",
        },
    )
    project = WebpackBundleProject(
        working_dir=destdir,
        project_template_dir=builddir,
        bundles=(x for x in [bundle1, bundle2]),
        config={"test": True, "entry": False},
    )

    project.create()
