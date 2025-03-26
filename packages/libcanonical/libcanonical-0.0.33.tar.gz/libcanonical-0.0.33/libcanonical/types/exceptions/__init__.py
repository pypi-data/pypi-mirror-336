# Copyright (C) 2022-2025 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from ._conflict import Conflict
from ._doesnotexist import DoesNotExist
from ._fatalexception import FatalException
from ._undecryptable import Undecryptable


__all__: list[str] = [
    'Conflict',
    'ExceptionRaiser',
    'DoesNotExist',
    'FatalException',
    'Undecryptable',
]


class ExceptionRaiser:
    """Mixin class that provides an interface to raise standard exceptions
    defined by the :mod:`libcanonical.types.exceptions` package.
    """
    __module__: str = 'libcanonical.types'
    Conflict        = Conflict
    DoesNotExist    = DoesNotExist
    Undecryptable   = Undecryptable