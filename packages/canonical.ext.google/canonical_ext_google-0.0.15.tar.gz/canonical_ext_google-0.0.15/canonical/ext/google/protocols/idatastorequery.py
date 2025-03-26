# Copyright (C) 2022-2025 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Protocol


class IDatastoreQuery(Protocol):
    __module__: str = 'canonical.ext.google.protocols'
    order: list[str]
    def add_filter(self, attname: str, op: str, value: Any) -> None: ...
    def keys_only(self) -> bool: ...
    def fetch(self, *args: Any, **kwargs: Any) -> None: ...