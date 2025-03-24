#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2023-2025 Alexis Pietak & Cecil Curry.
# See "LICENSE" for further details.

'''
Test-specific **exception hierarchy** (i.e., class hierarchy of test-specific
exceptions emitted by the this test suite).

This submodule defines hierarchies of :mod:`cellnition_test`-specific exceptions
and warnings emitted by unit and functional tests and fixtures.
'''

# ....................{ IMPORTS                            }....................
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# WARNING: To avoid polluting the public module namespace, external attributes
# should be locally imported at module scope *ONLY* under alternate private
# names (e.g., "from argparse import ArgumentParser as _ArgumentParser" rather
# than merely "from argparse import ArgumentParser").
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
from abc import ABCMeta as _ABCMeta
from cellnition.error import CellnitionException

# ....................{ SUPERCLASS                         }....................
class CellnitionTestException(CellnitionException, metaclass=_ABCMeta):
    '''
    Abstract base class of all **cellnition test exceptions.**

    Instances of subclasses of this exception are raised at test time from
    :mod:`cellnition_test`-specific unit and functional tests and fixtures.
    '''

    pass


#FIXME: Currently unused but preserved for posterity.
# class CellnitionTestPathException(CellnitionTestException):
#     '''
#     **Cellnition test path exceptions.**
#
#     This exception is raised at test time from callables and classes defined by
#     the :mod:`cellnition_test._util.path` subpackage.
#     '''
#
#     pass
