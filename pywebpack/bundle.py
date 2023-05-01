# -*- coding: utf-8 -*-
#
# This file is part of PyWebpack
# Copyright (C) 2017 CERN.
#
# PyWebpack is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Webpack bundle API."""


class WebpackBundle(object):
    """Webpack bundle."""

    def __init__(
        self,
        path,
        entry=None,
        dependencies=None,
        devDependencies=None,
        peerDependencies=None,
        aliases=None,
    ):
        """Initialize webpack bundle.

        :param path: Absolute path to the folder where the assets are
            located.
        :param entry: webpack entry; it indicates which modules webpack
            should use to begin building out its internal dependency graph.
        :param dependencies: npm dependencies.
        :param devDependencies: npm dev dependencies.
        :param peerDependencies: npm peer dependencies.
        :param aliases: Webpack resolver aliases.
        """
        self.path = path
        self.entry = entry or {}
        self.dependencies = {
            "dependencies": dependencies or {},
            "devDependencies": devDependencies or {},
            "peerDependencies": peerDependencies or {},
        }
        self.aliases = aliases or {}
