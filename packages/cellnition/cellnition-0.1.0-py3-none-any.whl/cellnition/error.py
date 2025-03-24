#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2023-2025 Alexis Pietak & Cecil Curry.
# See "LICENSE" for further details.

'''
Project-wide **exception hierarchy** (i.e., class hierarchy of project-specific
exceptions emitted by the this project).
'''

# ....................{ IMPORTS                            }....................
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# WARNING: To avoid polluting the public module namespace, external attributes
# should be locally imported at module scope *ONLY* under alternate private
# names (e.g., "from argparse import ArgumentParser as _ArgumentParser" rather
# than merely "from argparse import ArgumentParser").
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
from abc import ABCMeta as _ABCMeta

# ....................{ SUPERCLASS                         }....................
class CellnitionException(Exception, metaclass=_ABCMeta):
    '''
    Abstract base class of all **package-specific exceptions.**

    Instances of subclasses of this exception ABC are raised from various
    :mod:`cellnition` submodules.
    '''

    pass

# ....................{ PATH                               }....................
class CellnitionPathnameException(CellnitionException):
    '''
    **Pathname exception.**

    Instances of this exception subclass are raised from various submodules of
    the :mod:`ionyouapp._util.path` subpackage.
    '''

    pass


class CellnitionPathException(CellnitionException):
    '''
    **Path exception.**

    Instances of this exception subclass are raised from various submodules of
    the :mod:`ionyouapp._util.path` subpackage.
    '''

    pass


class CellnitionDirException(CellnitionPathException):
    '''
    **Directory exception.**

    Instances of this exception subclass are raised from various submodules of
    the :mod:`ionyouapp._util.path` subpackage.
    '''

    pass


class CellnitionFileException(CellnitionPathException):
    '''
    **File exception.**

    Instances of this exception subclass are raised from various submodules of
    the :mod:`ionyouapp._util.path` subpackage.
    '''

    pass
