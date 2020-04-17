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

from os import makedirs, remove, scandir, symlink, walk
from os.path import dirname, exists, getmtime, islink, join, realpath, relpath
from shutil import copy


def iter_files(folder):
    """Iterate all files in a given root directory."""
    for root, dirnames, filenames in walk(folder):
        for f in filenames:
            f = join(root, f)
            yield (f, relpath(f, folder))


def iter_paths(folder, root=None, depth=None):
    """Recursively yields paths under a folder up to a maximum depth."""
    assert depth is None or depth >= 0
    root = root or folder  # needed to compute the relative name

    if depth is None:  # yield all paths
        yield from iter_files(folder)
    elif depth == 0:
        yield folder, relpath(folder, root)
    else:
        for entry in scandir(folder):
            if entry.is_file():  # always yield files no matter the depth
                f = join(folder, entry.name)
                yield f, relpath(f, root)
            else:
                yield from iter_paths(
                    join(folder, entry.name),
                    root=root, depth=(depth - 1)
                )


class FileStorage(object):
    """Storage class that copies files if source is newer than destination."""

    def __init__(self, srcdir, dstdir, **kwargs):
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

    def __init__(self, *args, depth=None, **kwargs):
        """Initialize storage."""
        self.depth = depth
        super(LinkStorage, self).__init__(*args, **kwargs)

    def __iter__(self):
        """Iterate files from a directory."""
        # Only yield files and directories up to "depth"
        return iter_paths(self.srcdir, depth=self.depth)

    def _copyfile(self, src, dst, force=False):
        """Symlink file from source to destination."""
        if exists(dst):
            if (not islink(dst) or realpath(src) == realpath(dst)) \
                    and not force:
                return
            remove(dst)
        symlink(src, dst)
