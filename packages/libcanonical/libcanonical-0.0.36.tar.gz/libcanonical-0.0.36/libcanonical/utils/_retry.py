# Copyright (C) 2025 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
import functools
import inspect
import logging
import threading
from typing import Callable
from typing import Iterable
from typing import ParamSpec
from typing import TypeVar


P = ParamSpec('P')
T = TypeVar('T')


class _Retry:
    logger: logging.Logger = logging.getLogger('canonical')
    exception_classes: tuple[type[BaseException], ...]
    logging_message: str = "Caught retryable %(exception_class)s (thread: %(thread)s, attempts: %(attempts)s)"

    def __init__(
        self,
        types: Iterable[type[BaseException]],
        max_attempts: int | None = None,
        delay: int = 10,
        reason: str | None = None
    ):
        self.delay = delay
        self.exception_classes = tuple(types)
        self.max_attempts = max_attempts
        if reason:
            self.logging_message = reason

    def __call__(
        self,
        f: Callable[P, T]
    ) -> Callable[P, T]:
        assert inspect.iscoroutinefunction(f)
        handles = self.exception_classes

        @functools.wraps(f)
        async def d(*args: P.args, **kwargs: P.kwargs):
            attempts = 0
            while True:
                attempts += 1
                try:
                    result = await f(*args, **kwargs)
                    break
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    if not isinstance(e, handles):
                        raise
                    if self.max_attempts and attempts > self.max_attempts:
                        raise e from e
                    t = threading.current_thread()
                    self.logger.warning(
                        self.logging_message,
                        extra={
                            'attempts': attempts,
                            'exception_class': f'{type(e).__name__}',
                            'thread_id': t.ident
                        }
                    )
                    await asyncio.sleep(self.delay)
            return result

        return d # type: ignore


retry = _Retry