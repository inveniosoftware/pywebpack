# -*- coding: utf-8 -*-
#
# This file is part of PyWebpack
# Copyright (C) 2017 CERN.
#
# PyWebpack is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""API for creating and building Webpack projects."""

from __future__ import absolute_import, print_function

import json
import shutil
from os import makedirs
from os.path import dirname, exists, join

import pkg_resources
from pynpm import NPMPackage, YarnPackage

from .helpers import cached, merge_deps
from .storage import FileStorage


class WebpackProject(object):
    """API for building an existing Webpack project."""

    def __init__(self, path):
        """Initialize instance."""
        self._npmpkg = None
        self._path = path

    @property
    def project_path(self):
        """Get the project path."""
        return dirname(self.npmpkg.package_json_path)

    @property
    def path(self):
        """Path property."""
        return self._path

    @property
    @cached
    def npmpkg(self):
        """Get API to NPM package."""
        return NPMPackage(self.path)

    def install(self, *args):
        """Install project."""
        return self.npmpkg.install(*args)

    def run(self, script_name, *args):
        """Run an NPM script."""
        scripts = self.npmpkg.package_json.get('scripts', {}).keys()
        if script_name not in scripts:
            raise RuntimeError('Invalid NPM script.')
        return self.npmpkg.run_script(script_name, *args)

    def build(self, *args):
        """Run build script."""
        return self.run('build', *args)

    def buildall(self):
        """Build project from scratch."""
        self.install()
        self.build()


class WebpackTemplateProject(WebpackProject):
    """API for creating and building a webpack project based on a template.

    Copies all files from a project template folder into a destionation path
    and optionally writes a user provided config in JSON into the destionation
    path as well.
    """

    def __init__(self, dest, project_template=None, config=None,
                 config_path=None, storage_cls=None):
        """Initialize templated folder."""
        self._project_template = project_template
        self._storage_cls = storage_cls or FileStorage
        self._config = config
        self._config_path = config_path or 'config.json'
        super(WebpackTemplateProject, self).__init__(dest)

    @property
    def config(self):
        """Get configuration dictionary."""
        if self._config is None:
            return None
        config = self._config() if callable(self._config) else self._config
        return config

    @property
    def config_path(self):
        """Get configuration path."""
        return join(self.project_path, self._config_path)

    @property
    def storage_cls(self):
        """Storage class property."""
        return self._storage_cls

    def create(self, force=None):
        """Create webpack project from a template."""
        self.storage_cls(self._project_template, self.project_path).run(
            force=force)

        # Write config if not empty
        config = self.config
        config_path = self.config_path
        if config:
            # Create config path directory if it does not exists.
            if not exists(dirname(config_path)):
                makedirs(dirname(config_path))
            # Write config.json
            with open(config_path, 'w') as fp:
                json.dump(config, fp, indent=2, sort_keys=True)

    def clean(self):
        """Clean created webpack project."""
        if exists(self.project_path):
            shutil.rmtree(self.project_path)

    def buildall(self):
        """Build project from scratch."""
        self.create()
        super(WebpackTemplateProject, self).buildall()


class WebpackBundleProject(WebpackTemplateProject):
    """Build webpack project from multiple bundles."""

    def __init__(self, dest, project_template=None, bundles=None, config=None,
                 config_path=None, storage_cls=None):
        """Initialize templated folder."""
        self._bundles_iter = bundles or []
        super(WebpackBundleProject, self).__init__(
            dest,
            project_template=project_template,
            config=config or {},
            config_path=config_path,
            storage_cls=storage_cls,
        )

    @property
    @cached
    def bundles(self):
        """Get bundles."""
        return list(self._bundles_iter)

    @property
    @cached
    def entry(self):
        """Get webpack entry points."""
        res = {}
        for b in self.bundles:
            res.update(b.entry)
        return res

    @property
    def config(self):
        """Inject webpack entry points from bundles."""
        config = super(WebpackBundleProject, self).config
        config.update({'entry': self.entry})
        return config

    @property
    @cached
    def dependencies(self):
        """Get package.json dependencies."""
        res = {
            'dependencies': {},
            'devDependencies': {},
            'peerDependencies': {}
        }
        for b in self.bundles:
            merge_deps(res, b.dependencies)
        return res

    @property
    @cached
    def package_json(self):
        """Merge bundle dependencies into ``package.json``."""
        return merge_deps(self.npmpkg.package_json, self.dependencies)

    def collect(self, force=None):
        """Collect asset files from bundles."""
        for b in self.bundles:
            self.storage_cls(b.path, self.project_path).run(force=force)

    def create(self, force={'package.json'}):
        """Create webpack project from a template."""
        # Force package.json to be overwritten always.
        super(WebpackBundleProject, self).create(force=force)
        # Collect all asset files from the bundles.
        self.collect(force=force)
        # Generate new package json (reads the package.json and merges in
        # npm dependencies; must be done before opening the file for writing)
        package_json = self.package_json
        # Write package.json (with collected dependencies)
        with open(self.npmpkg.package_json_path, 'w') as fp:
            json.dump(package_json, fp, indent=2, sort_keys=True)
