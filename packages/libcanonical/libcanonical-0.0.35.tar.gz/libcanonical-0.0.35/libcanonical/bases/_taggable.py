# Copyright (C) 2023-2025 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Generic
from typing import TypeVar
from typing import Hashable


T = TypeVar('T', bound=Hashable)


class Taggable(Generic[T]):
    """A base class that provides tagging functionality."""
    tags: set[T]

    def __init__(self, *args: Any, **kwargs: Any):
        self.tags = set()

    def tag(self, tag: T) -> bool:
        added = tag not in self.tags
        self.tags.add(tag)
        return added

    def is_tagged(self, tag: T):
        return tag in self.tags

    def untag(self, tag: T) -> bool:
        removed = tag in self.tags
        self.tags.remove(tag)
        return removed