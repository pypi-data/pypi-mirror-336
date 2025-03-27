import logging
import re
from copy import (
    deepcopy,
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
from labels.model.core import (
    Language,
    Package,
    PackageType,
)
from labels.pkg.cataloger.generic.parser import (
    Environment,
)
from labels.pkg.cataloger.java.package import (
    package_url,
)

LOGGER = logging.getLogger(__name__)

GRADLE_DIST = re.compile("^distributionUrl=.+gradle-(?P<gradle_version>[^-]+)-.+")


def parse_gradle_properties(
    _resolver: Resolver | None,
    __: Environment | None,
    reader: LocationReadCloser,
) -> tuple[list[Package], list[Relationship]]:
    packages = []
    for line_no, raw_line in enumerate(reader.read_closer.readlines(), start=1):
        line = raw_line.strip()
        if (match := GRADLE_DIST.match(line)) and (version := match.group("gradle_version")):
            location = deepcopy(reader.location)
            if location.coordinates:
                location.coordinates.line = line_no

            packages.append(
                Package(
                    name="gradle",
                    version=version,
                    locations=[location],
                    language=Language.JAVA,
                    type=PackageType.JavaPkg,
                    p_url=package_url("gradle", version),
                    licenses=[],
                ),
            )

    return packages, []
