from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from collections.abc import ItemsView

from labels.artifact.relationship import Relationship
from labels.file.dependency_type import DependencyType
from labels.file.location import Location
from labels.file.location_read_closer import LocationReadCloser
from labels.file.resolver import Resolver
from labels.file.scope import Scope
from labels.internal.collection.json import parse_json_with_tree_sitter
from labels.internal.collection.types import IndexedDict, ParsedValue
from labels.model.core import Language, Package, PackageType
from labels.pkg.cataloger.generic.parser import Environment
from labels.pkg.cataloger.php.package import package_url

EMPTY_DICT: IndexedDict[str, ParsedValue] = IndexedDict()


def _get_location(location: Location, sourceline: int) -> Location:
    if location.coordinates:
        c_upd = {"line": sourceline}
        l_upd = {"coordinates": location.coordinates.model_copy(update=c_upd)}
        location.dependency_type = DependencyType.DIRECT
        return location.model_copy(update=l_upd)
    return location


def _get_packages(
    reader: LocationReadCloser,
    dependencies: IndexedDict[str, ParsedValue],
    *,
    is_dev: bool,
) -> list[Package]:
    if not dependencies:
        return []

    general_location = _get_location(
        reader.location,
        dependencies.position.start.line,
    )
    general_location.scope = Scope.DEV if is_dev else Scope.PROD
    items: ItemsView[str, ParsedValue] = dependencies.items()
    return [
        Package(
            name=name,
            version=version,
            locations=[general_location],
            language=Language.PHP,
            licenses=[],
            type=PackageType.PhpComposerPkg,
            p_url=package_url(name, version),
            is_dev=is_dev,
        )
        for name, version in items
        if isinstance(version, str)
    ]


def parse_composer_json(
    _: Resolver | None,
    __: Environment | None,
    reader: LocationReadCloser,
) -> tuple[list[Package], list[Relationship]]:
    content = cast(
        IndexedDict[str, ParsedValue],
        parse_json_with_tree_sitter(reader.read_closer.read()),
    )
    deps: IndexedDict[str, ParsedValue] = cast(
        IndexedDict[str, ParsedValue],
        content.get("require", EMPTY_DICT),
    )
    dev_deps: IndexedDict[str, ParsedValue] = cast(
        IndexedDict[str, ParsedValue],
        content.get("require-dev", EMPTY_DICT),
    )
    packages = [
        *_get_packages(reader, deps, is_dev=False),
        *_get_packages(reader, dev_deps, is_dev=True),
    ]
    return packages, []
