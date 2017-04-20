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
