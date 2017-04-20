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

"""Storage API."""

from __future__ import absolute_import, print_function

from os import makedirs, remove, symlink, walk
from os.path import dirname, exists, getmtime, islink, join, realpath, relpath
from shutil import copy


def iter_files(folder):
    """Recursively iterate all files in a given root directory."""
    for root, dirnames, filenames in walk(folder):
        for f in filenames:
            f = join(root, f)
            yield (f, relpath(f, folder))


class FileStorage(object):
    """Storage class that copies files if source is newer than destination."""

    def __init__(self, srcdir, dstdir):
        """Initialize storage."""
        self.srcdir = srcdir
        self.dstdir = dstdir

    def __iter__(self):
        """Iterate files from a directory."""
        return iter_files(self.srcdir)

    def _copyfile(self, src, dst):
        """Copy file from source to destination."""
        if exists(dst):
            if getmtime(dst) >= getmtime(src):
                return
            remove(dst)
        copy(src, dst)

    def run(self):
        """Copy files from source to destination."""
        for fsrc, relpath in self:
            fdst = join(self.dstdir, relpath)
            fdstdir = dirname(fdst)

            if not exists(fdstdir):
                makedirs(fdstdir)

            self._copyfile(fsrc, fdst)


class LinkStorage(FileStorage):
    """Storage class that link files."""

    def _copyfile(self, src, dst):
        """Symlink file from source to destination."""
        if exists(dst):
            if not islink(dst) or realpath(src) == realpath(dst):
                return
            remove(dst)
        symlink(src, dst)
