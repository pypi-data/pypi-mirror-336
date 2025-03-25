######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.7.1+obcheckpoint(0.1.9);ob(v1)                                                    #
# Generated on 2025-03-24T18:51:07.953807                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

from ......exception import MetaflowException as MetaflowException

class DatastoreReadInitException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, message):
        ...
    ...

class DatastoreWriteInitException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, message):
        ...
    ...

class DatastoreNotReadyException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, message):
        ...
    ...

