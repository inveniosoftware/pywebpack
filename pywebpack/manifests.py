# -*- coding: utf-8 -*-
#
# This file is part of PyWebpack
# Copyright (C) 2017 CERN
# Copyright (C) 2017 Anders Kaseorg
#
# PyWebpack is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Webpack manifests API."""

import json
import sys
from os.path import splitext

_string_types = (str,) if sys.version_info[0] == 3 else (basestring,)


#
# Errors
#
class ManifestError(Exception):
    """Manifest error."""


class InvalidManifestError(ManifestError):
    """Invalid manifest."""


class UnfinishedManifestError(ManifestError):
    """Manifest is currently being built."""


class UnsupportedManifestError(ManifestError):
    """Could not parse the manifest."""


class UnsupportedExtensionError(ManifestError):
    """Manifest contains a file with an extension that is not supported."""


#
# Manifest
#
class Manifest(object):
    """Assets manifest."""

    def __init__(self):
        """Initialize manifest."""
        self._entries = {}

    def add(self, entry):
        """Add an entry to the manifest."""
        if entry.name in self._entries:
            raise KeyError("Entry {} already present".format(entry.name))
        self._entries[entry.name] = entry

    def __getitem__(self, key):
        """Get a manifest entry."""
        return self._entries[key]

    def __getattr__(self, name):
        """Get a manifest entry."""
        try:
            return self._entries[name]
        except KeyError:
            raise AttributeError("Attribute {} does not exists.".format(name))

    def __iter__(self):
        """Iterate over entries in the manifest."""
        return iter(self._entries.values())


class ManifestEntry(object):
    """Represents a manifest entry."""

    templates = {
        ".js": '<script src="{}"></script>',
        ".css": '<link rel="stylesheet" href="{}" />',
    }

    def __init__(self, name, paths):
        """Initialize manifest entry."""
        self.name = name
        self._paths = paths

    def render(self):
        """Render entry."""
        out = []
        for p in self._paths:
            _dummy_name, ext = splitext(p)
            tpl = self.templates.get(ext.lower())
            if tpl is None:
                raise UnsupportedExtensionError(p)
            out.append(tpl.format(p))
        return "".join(out)

    def __iter__(self):
        """Iterate over files in the manifest entry."""
        for path in self._paths:
            yield path

    def __str__(self):
        """Render entry."""
        return self.render()


#
# Factories
#
class ManifestFactory(object):
    """Manifest factory base class."""

    def __init__(self, manifest_cls=Manifest, entry_cls=ManifestEntry):
        """Initialize factory."""
        self.manifest_cls = manifest_cls
        self.entry_cls = entry_cls

    def load(self, filepath):
        """Load a manifest file."""
        with open(filepath) as fp:
            return self.create(json.load(fp))

    def create_entry(self, entry, paths):
        """Create a manifest entry instance."""
        return self.entry_cls(entry, paths)

    def create_manifest(self):
        """Create a manifest instance."""
        return self.manifest_cls()


class WebpackManifestFactory(ManifestFactory):
    """Manifest factory for webpack-manifest-plugin."""

    def create(self, data):
        """Create manifest from parsed data."""
        manifest = self.create_manifest()
        for entry_name, path in data.items():
            if not isinstance(path, _string_types):
                raise InvalidManifestError("webpack-manifest-plugin")
            manifest.add(self.create_entry(entry_name, [path]))
        return manifest


class WebpackYamFactory(ManifestFactory):
    """Manifest factory for webpack-yam-plugin."""

    def create(self, data):
        """Create manifest from parsed data."""
        # Is manifest of correct type?
        try:
            status = data["status"]
            files = data["files"]
        except KeyError:
            raise InvalidManifestError("webpack-yam-plugin")

        # Is manifest finished?
        if files is None or status != "built":
            raise UnfinishedManifestError(data)

        manifest = self.create_manifest()
        for entry_name, paths in files.items():
            manifest.add(self.create_entry(entry_name, paths))
        return manifest


class WebpackBundleTrackerFactory(ManifestFactory):
    """Manifest factory for webpack-bundle-tracker."""

    def create(self, data):
        """Create manifest from parsed data."""
        # Is manifest of correct type?
        try:
            status = data["status"]
        except KeyError:
            raise InvalidManifestError("webpack-bundle-tracker")

        if "chunks" not in data:
            raise InvalidManifestError("webpack-bundle-tracker")

        # Is manifest finished?
        if status != "done":
            raise UnfinishedManifestError(data)

        manifest = self.create_manifest()
        chunks = data["chunks"]
        assets = data["assets"]
        for entry_name, paths in chunks.items():
            js_paths = [p for p in paths if p.endswith(".js")]
            if js_paths:
                manifest.add(
                    self.create_entry(
                        entry_name + ".js", [assets[p]["publicPath"] for p in js_paths]
                    )
                )

            css_paths = [p for p in paths if p.endswith(".css")]
            if css_paths:
                manifest.add(
                    self.create_entry(
                        entry_name + ".css",
                        [assets[p]["publicPath"] for p in css_paths],
                    )
                )
        return manifest


class ManifestLoader(object):
    """Loads a Webpack manifest (multiple types supported)."""

    types = [
        WebpackBundleTrackerFactory,
        WebpackYamFactory,
        WebpackManifestFactory,
    ]

    def __init__(self, manifest_cls=Manifest, entry_cls=ManifestEntry):
        """Initialize loader."""
        self.manifest_cls = manifest_cls
        self.entry_cls = entry_cls

    def load(self, filepath):
        """Load a manifest from a file."""
        with open(filepath) as fp:
            data = json.load(fp)

        for t in self.types:
            try:
                return t(
                    manifest_cls=self.manifest_cls, entry_cls=self.entry_cls
                ).create(data)
            except InvalidManifestError:
                pass

        raise UnsupportedManifestError(filepath)
