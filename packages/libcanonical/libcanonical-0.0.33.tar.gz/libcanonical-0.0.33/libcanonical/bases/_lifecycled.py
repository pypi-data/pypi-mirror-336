# Copyright (C) 2022-2025 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import inspect
from typing import Any
from typing import Coroutine
from types import TracebackType


class Lifecycled:
    __module__: str = 'libcanonical.bases'

    def setup(
        self,
        reloading: bool = False
    ) -> None | Coroutine[Any, Any, None]:
        raise NotImplementedError

    def teardown(
        self,
        exception: BaseException | None = None
    ) -> bool | Coroutine[Any, Any, bool]:
        raise NotImplementedError

    async def __aenter__(self):
        result = self.setup(reloading=False)
        if inspect.isawaitable(result):
            await result
        return self

    async def __aexit__(
        self,
        cls: type[BaseException] | None = None,
        exception: BaseException | None = None,
        traceback: TracebackType | None = None
    ) -> bool:
        result = self.teardown()
        if inspect.isawaitable(result):
            await result
        assert isinstance(result, bool)
        return result