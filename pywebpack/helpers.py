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

from functools import wraps

import pkg_resources


def bundles_from_entry_point(group):
    """Load bundles from entry point group."""
    return (ep.load() for ep in pkg_resources.iter_entry_points(group))


def cached(f):
    """Decorator to cache result of property."""
    @wraps(f)
    def inner(self):
        name = '_{}'.format(f.__name__)
        if getattr(self, name, None) is None:
            setattr(self, name, f(self))
        return getattr(self, name)
    return inner


def merge_deps(deps, bundles_deps):
    """Merge NPM dependencies."""
    deps.update(bundles_deps)
    return deps
