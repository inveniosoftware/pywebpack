# SPDX-FileCopyrightText: 2023 CERN.
# SPDX-License-Identifier: BSD-3-Clause

"""Errors."""


class PyWebpackException(Exception):
    """Base exception for PyWebpack errors."""


class MergeConflictError(PyWebpackException):
    """Base exception for PyWebpack errors."""
