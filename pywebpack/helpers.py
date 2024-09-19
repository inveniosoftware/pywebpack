# -*- coding: utf-8 -*-
#
# This file is part of PyWebpack
# Copyright (C) 2017-2020 CERN.
# Copyright (C) 2020 Cottage Labs LLP.
#
# PyWebpack is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Webpack bundle API."""

import re
from functools import wraps

from importlib_metadata import entry_points

from pywebpack.errors import MergeConflictError

# https://semver.org/#is-there-a-suggested-regular-expression-regex-to-check-a-semver-string
# Differences:
# - `^\D*`: ignores the first not numberic char (major version), e.g. ~ or <
# - minor and patch versions are optional
SEM_VER = r"^\D*(?P<major>0|[1-9]\d*)\.?(?P<minor>0|[1-9]\d*)?\.?(?P<patch>0|[1-9]\d*)?(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"


def _load_ep(ep):
    mod = ep.load()
    return mod() if callable(mod) else mod


def bundles_from_entry_point(group):
    """Load bundles from entry point group."""
    return (_load_ep(ep) for ep in entry_points(group=group))


def cached(f):
    """Decorator to cache result of property."""

    @wraps(f)
    def inner(self):
        name = "_{}".format(f.__name__)
        if getattr(self, name, None) is None:
            setattr(self, name, f(self))
        return getattr(self, name)

    return inner


def check_exit(f):
    """Decorator to ensure that an NPM process exited successfully."""

    @wraps(f)
    def inner(self, *args, **kwargs):
        exit_code = f(self, *args, **kwargs)
        if exit_code != 0:
            raise RuntimeError("Process exited with code {}".format(exit_code))
        return exit_code

    return inner


def _parse_version(version):
    """Parse semantic version."""
    match = re.match(SEM_VER, version)
    if not match:
        raise ValueError(f"{version} is not a valid semantic version.")
    major = match.group("major")
    minor = match.group("minor") or 0
    patch = match.group("patch") or 0
    prerelease = match.group("prerelease") or ""
    return int(major), int(minor), int(patch), prerelease


def max_version(v1, v2):
    """Given 2 semver strings, return the max version.

    Complies with specification: <https://semver.org/#spec-item-11>.
    """
    v1_maj, v1_min, v1_patch, v1_pre = _parse_version(v1)
    v2_maj, v2_min, v2_patch, v2_pre = _parse_version(v2)

    if v1_maj == v2_maj:
        if v1_min == v2_min:
            if v1_patch == v2_patch:
                if v1_pre and v2_pre:
                    # check pre-release
                    v1_pre_tags = v1_pre.split(".")
                    v2_pre_tags = v2_pre.split(".")
                    # zip creates pairs for shortest list
                    for v1_pre_tag, v2_pre_tag in zip(v1_pre_tags, v2_pre_tags):
                        if v1_pre_tag == v2_pre_tag:
                            continue
                        if v1_pre_tag.isdigit() and v2_pre_tag.isdigit():
                            _max = max(int(v1_pre_tag), int(v2_pre_tag))
                        else:
                            _max = max(v1_pre_tag, v2_pre_tag)
                        return v1 if _max == v1_pre_tag else v2
                    # lists have different lengths: return the longest
                    return v1 if len(v1_pre_tags) > len(v2_pre_tags) else v2
                elif v1_pre and not v2_pre:
                    return v2
                elif v2_pre and not v1_pre:
                    return v1
                # identical: no pre-release, return any (the first)
                return v1
            # return higher patch
            return v1 if v1_patch > v2_patch else v2
        # return higher minor
        return v1 if v1_min > v2_min else v2
    # return higher major
    return v1 if v1_maj > v2_maj else v2


def merge_deps(computed_deps, incoming_deps):
    """Merge NPM dependencies.

    :param computed_deps: dict with all computed deps,
        after merging incoming deps into it.
    :param incoming_deps: new incoming deps to be merged
        into `computed_deps`.
    :return: the computed_deps dict with merged `incoming_deps` into it.
    :raise: raises the MergeConflictError exception when deps
        cannot be merged.
    """
    dep_types = ["dependencies", "devDependencies", "peerDependencies"]
    for dep_type in dep_types:
        computed_deps.setdefault(dep_type, {})
        if dep_type in incoming_deps:
            computed = computed_deps[dep_type]
            incoming = incoming_deps[dep_type]
            for incoming_pkg, incoming_version in incoming.items():
                if incoming_pkg in computed:
                    computed_version = computed[incoming_pkg]

                    v_maj, _, _, _ = _parse_version(incoming_version)
                    tv_maj, _, _, _ = _parse_version(computed_version)
                    if v_maj != tv_maj:
                        raise MergeConflictError(
                            f"Incompatible major versions for package {incoming_pkg}: current version is {computed_version}, incoming version is {incoming_version}"
                        )

                    _max = max_version(incoming_version, computed_version)
                    computed[incoming_pkg] = _max
                else:
                    computed[incoming_pkg] = incoming_version
    return computed_deps
