# Copyright (C) 2022-2025 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Protocol
from typing import Iterator

from .idatastoreentity import IDatastoreEntity


class IDatastoreCursor(Protocol):
    __module__: str = 'canonical.ext.google.protocols'
    next_page_token: bytes | None
    num_results: int
    def __iter__(self) -> Iterator[IDatastoreEntity]: ...
    def __next__(self) -> IDatastoreEntity: ...