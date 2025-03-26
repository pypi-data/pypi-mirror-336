# Copyright (C) 2022-2025 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from ._externalstate import ExternalState


class PollingExternalState(ExternalState):
    """An :class:`~libcanonical.bases.ExternalState` implementation that
    uses polling as it's transport mechanism.
    """
    __module__: str = 'libcanonical.bases'

    #: The interval between queries at the remote source for the
    #: current state.
    interval: float = 10.0

    #

    async def poll(self) -> None:
        """Polls the remote source for data."""
        raise NotImplementedError