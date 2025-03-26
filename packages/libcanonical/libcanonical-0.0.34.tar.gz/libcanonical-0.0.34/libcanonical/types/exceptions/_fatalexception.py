# Copyright (C) 2022-2025 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import sys


class FatalException(SystemExit):
    """Represent an exception condition which prevents an process from
    continuing to run.
    """
    exitcode: int = 1

    def __init__(self, reason: str):
        sys.stderr.write(reason + '\n')
        sys.stderr.flush()
        super().__init__(self.exitcode)