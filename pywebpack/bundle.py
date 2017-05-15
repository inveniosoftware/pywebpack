# -*- coding: utf-8 -*-
#
# This file is part of PyWebpack
# Copyright (C) 2017 CERN.
#
# PyWebpack is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Webpack bundle API."""

from __future__ import absolute_import, print_function


class WebpackBundle(object):
    """Webpack bundle."""

    def __init__(self, path, entry=None, dependencies=None,
                 devDependencies=None, peerDependencies=None):
        """Initialize webpack bundle."""
        self.path = path
        self.entry = entry or {}
        self.dependencies = {
            'dependencies': dependencies or {},
            'devDependencies': devDependencies or {},
            'peerDependencies': peerDependencies or {},
        }
