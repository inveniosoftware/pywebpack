# -*- coding: utf-8 -*-
#
# This file is part of PyWebpack
# Copyright (C) 2017 CERN.
#
# PyWebpack is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

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

    def _copyfile(self, src, dst, force=False):
        """Copy file from source to destination."""
        if exists(dst):
            if getmtime(dst) >= getmtime(src) and not force:
                return
            remove(dst)
        copy(src, dst)

    def run(self, force=None):
        """Copy files from source to destination."""
        force = force or {}
        for fsrc, relpath in self:
            fdst = join(self.dstdir, relpath)
            fdstdir = dirname(fdst)

            if not exists(fdstdir):
                makedirs(fdstdir)

            self._copyfile(fsrc, fdst, force=relpath in force)


class LinkStorage(FileStorage):
    """Storage class that link files."""

    def _copyfile(self, src, dst, force=False):
        """Symlink file from source to destination."""
        if exists(dst):
            if (not islink(dst) or realpath(src) == realpath(dst)) \
                    and not force:
                return
            remove(dst)
        symlink(src, dst)
