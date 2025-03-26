# Copyright (C) 2022-2025 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from ._base import BaseCanonicalException


class Undecryptable(BaseCanonicalException):
    """This exception may be raised when the decryption of a ciphertext
    is attempted but the operation failed.
    """
    http_status_code: int = 503