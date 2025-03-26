import re
from copy import (
    deepcopy,
)

from packageurl import (
    PackageURL,
)

from sbom.artifact.relationship import (
    Relationship,
)
from sbom.file.dependency_type import (
    DependencyType,
)
from sbom.file.location_read_closer import (
    LocationReadCloser,
)
from sbom.file.resolver import (
    Resolver,
)
from sbom.model.core import (
    Language,
    Package,
    PackageType,
)
from sbom.pkg.cataloger.generic.parser import (
    Environment,
)

QUOTE = r'["\']'
NL = r"(\n?\s*)?"
TEXT = r'[^"\']+'
RE_SBT: re.Pattern[str] = re.compile(
    r"^[^%]*"
    rf"{NL}{QUOTE}(?P<group>{TEXT}){QUOTE}{NL}%"
    rf"{NL}{QUOTE}(?P<name>{TEXT}){QUOTE}{NL}%"
    rf"{NL}{QUOTE}(?P<version>{TEXT}){QUOTE}{NL}"
    r".*$",
)


def build_stb(
    _: Resolver | None,
    __: Environment | None,
    reader: LocationReadCloser,
) -> tuple[list[Package], list[Relationship]]:
    packages = []
    content = reader.read_closer.read()
    for line_no, line in enumerate(content.splitlines(), start=1):
        if match := RE_SBT.match(line):
            product: str = str(match.group("group")) + ":" + match.group("name")
            version = match.group("version")
        else:
            continue
        location = deepcopy(reader.location)
        if location.coordinates:
            location.coordinates.line = line_no
            location.dependency_type = DependencyType.DIRECT
        packages.append(
            Package(
                name=product,
                version=version,
                type=PackageType.JavaPkg,
                locations=[location],
                p_url=PackageURL(
                    type="maven",
                    namespace=str(match.group("group")),
                    name=str(match.group("name")),
                    version=version,
                    qualifiers=None,
                    subpath="",
                ).to_string(),
                metadata=None,
                language=Language.JAVA,
                licenses=[],
                is_dev=False,
            ),
        )
    return packages, []
