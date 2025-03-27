from collections.abc import Callable

from pydantic import (
    BaseModel,
    ConfigDict,
)

from labels.artifact.relationship import (
    Relationship,
)
from labels.file.location_read_closer import (
    LocationReadCloser,
)
from labels.file.resolver import (
    Resolver,
)
from labels.linux.release import (
    Release,
)
from labels.model.core import (
    Package,
)


class Environment(BaseModel):
    linux_release: Release | None
    model_config = ConfigDict(frozen=True)


Parser = Callable[
    [Resolver, Environment, LocationReadCloser],
    tuple[list[Package], list[Relationship]] | None,
]
