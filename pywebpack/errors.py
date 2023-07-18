# -*- coding: utf-8 -*-
#
# This file is part of PyWebpack
# Copyright (C) 2023 CERN.
#
# PyWebpack is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Errors."""


class PyWebpackException(Exception):
    """Base exception for PyWebpack errors."""


class MergeConflictError(PyWebpackException):
    """Base exception for PyWebpack errors."""
