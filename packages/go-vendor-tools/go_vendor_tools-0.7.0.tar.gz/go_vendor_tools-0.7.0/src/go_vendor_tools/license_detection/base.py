# Copyright (C) 2024 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT

"""
Base classes for handling license detection tools
"""

from __future__ import annotations

import abc
import dataclasses
import os
import re
import sys
from collections.abc import Collection, Sequence
from itertools import chain
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, Generic

from go_vendor_tools.config.licenses import LicenseConfig, LicenseEntry
from go_vendor_tools.exceptions import LicenseError
from go_vendor_tools.gomod import get_go_module_dirs
from go_vendor_tools.hashing import verify_hash
from go_vendor_tools.license_detection.search import find_license_files
from go_vendor_tools.licensing import combine_licenses

if TYPE_CHECKING:
    from _typeshed import StrPath

    # TypeVar from typing_extensions needed for PEP 696
    from typing_extensions import Self, TypeVar
else:
    from typing import TypeVar

EXTRA_LICENSE_FILE_REGEX = re.compile(
    r"^(AUTHORS|NOTICE|PATENTS).*$", flags=re.IGNORECASE
)


def get_manual_license_entries(
    licenses: list[LicenseEntry], directory: StrPath
) -> tuple[dict[Path, str], list[Path]]:
    results: dict[Path, str] = {}
    not_matched: list[Path] = []
    seen: set[Path] = set()
    for lic in licenses:
        relpath = Path(lic["path"])
        path = directory / relpath
        if path in results:
            raise LicenseError(
                f"{path} was specified multiple times in the configuration!"
            )
        seen.add(path)
        if verify_hash(path, lic["sha256sum"]):
            results[relpath] = lic["expression"]
        else:
            not_matched.append(relpath)
    return results, not_matched


def is_unwanted_path(
    path: Path,
    exclude_directories: Collection[StrPath],
    exclude_files: Collection[str],
) -> bool:
    return (
        # Hardcoded exception
        "testdata" in path.parts
        or str(path) in exclude_files
        or any(path.is_relative_to(directory) for directory in exclude_directories)
    )


def filter_license_map(
    license_map: dict[Path, str],
    exclude_directories: Collection[str],
    exclude_files: Collection[str],
) -> dict[Path, str]:
    """
    Filter licenses files from unwanted paths
    """
    exclude_directories = set(exclude_directories)
    exclude_files = set(exclude_files)
    return {
        path: exp
        for path, exp in license_map.items()
        if not is_unwanted_path(path, exclude_directories, exclude_files)
    }


def python3dist(package: str, /) -> str:
    return f"python{sys.version_info.major}.{sys.version_info.minor}dist({package})"


# TODO(anyone): Should we check for valid filenames
# (each file should be a single license name)
def reuse_path_to_license_map(files: Collection[StrPath]) -> dict[Path, str]:
    result: dict[Path, str] = {}
    for file in files:
        name = os.path.splitext(os.path.basename(file))[0]
        result[Path(file)] = name
    return result


@dataclasses.dataclass()
class LicenseData:
    """
    Generic class representing detected license data.
    Can be subclassed by detector implementations to add additional fields.

    Attributes:
        directory:
            Path that was crawled for licensed
        license_map:
            Mapping of relative paths to license (within `directory`) to str
            SPDX license expressions
        undetected_licenses:
            License files that the license detector implementation failed to
            detect
        license_set:
            Set of unique detected license expressions
        license_expression:
            Cumulative `license_expression.LicenseExpression` SPDX expression
        license_files_paths:
            Full paths to all detected license files
        extra_license_files:
            Extra files (e.g., AUTHORS or NOTICE files) that we should include
            in the distribution but not run through the license detector
    """

    directory: Path
    license_map: dict[Path, str]
    undetected_licenses: Collection[Path]
    unmatched_extra_licenses: Collection[Path]
    license_set: set[str] = dataclasses.field(init=False)
    license_expression: str | None = dataclasses.field(init=False)
    license_file_paths: Collection[Path] = dataclasses.field(init=False)
    extra_license_files: list[Path]
    detector_name: str
    _LIST_PATH_FIELDS: ClassVar = (
        "undetected_licenses",
        "unmatched_extra_licenses",
        "license_file_paths",
        "extra_license_files",
    )
    replace = dataclasses.replace

    def __post_init__(self) -> None:
        self.license_set = set(self.license_map.values())
        self.license_expression = (
            self._combine_licenses(*self.license_set) if self.license_map else None
        )
        self.license_file_paths = tuple(
            self.directory / lic
            for lic in chain(self.license_map, self.undetected_licenses)
        )

    _combine_licenses = staticmethod(combine_licenses)

    # TODO(gotmax23): Consider cattrs or pydantic
    def to_jsonable(self) -> dict[str, Any]:
        data = dataclasses.asdict(self)
        for key, value in data.items():
            if key == "directory":
                data[key] = str(value)
            elif key == "license_map":
                data[key] = {str(key1): value1 for key1, value1 in value.items()}
            elif key in self._LIST_PATH_FIELDS:
                data[key] = list(map(str, value))
                if not isinstance(value, Sequence):
                    data[key].sort()
            elif key == "license_set":
                data[key] = sorted(value)
            elif key == "license_expression":
                data[key] = str(value)
        return data

    @classmethod
    def _from_jsonable_to_dict(cls, data: dict[Any, Any]) -> dict[Any, Any]:
        init_fields = [field.name for field in dataclasses.fields(cls) if field.init]
        newdata: dict[Any, Any] = {}
        for key, value in data.items():
            if key not in init_fields:
                continue
            if key == "directory":
                newdata[key] = Path(value)
            elif key == "license_map":
                newdata[key] = {Path(key1): value1 for key1, value1 in value.items()}
            elif key in cls._LIST_PATH_FIELDS:
                func = set if key == "undetected_licenses" else sorted
                newdata[key] = func(map(Path, value))
            else:
                newdata[key] = value
        return newdata

    @classmethod
    def from_jsonable(cls, data: dict[Any, Any]) -> Self:
        return cls(**cls._from_jsonable_to_dict(data))


if TYPE_CHECKING:
    _LicenseDataT_co = TypeVar(
        "_LicenseDataT_co", bound=LicenseData, covariant=True, default=LicenseData
    )
else:
    _LicenseDataT_co = TypeVar("_LicenseDataT_co", covariant=True, bound=LicenseData)


class LicenseDetector(Generic[_LicenseDataT_co], metaclass=abc.ABCMeta):
    """
    ABC for a license detector backend

    Attributes:
        NAME: Name of the license detector
        PACKAGES_NEEDED:
            Tuple of Fedora package names needed for the license detector
        FIND_PACKAGES_NEEDED:
            Tuple of packages needed for find_only mode (see __init__ docstring)
        license_config:
            LicenseConfig object passed to the constructor
        detector_config:
            Options passeed to constructor
        find_only: Whether find_only mode is enabled
    """

    NAME: ClassVar[str]
    PACKAGES_NEEDED: ClassVar[tuple[str, ...]] = ()
    FIND_PACKAGES_NEEDED: ClassVar[tuple[str, ...]] = ()
    detector_config: dict[str, str]
    license_config: LicenseConfig
    _find_only: bool

    @abc.abstractmethod
    def __init__(
        self,
        detector_config: dict[str, str],
        license_config: LicenseConfig,
        find_only: bool = False,
    ) -> None:
        """
        Args:
            detector_config:
                String key-value pairs of --detector-config options that are
                defined separately for each license detector implementation
            license_config:
                LicenseConfig object.
                The detector_config option is ignored in favor of the
                detector_config argument.
            find_only:
                When find_only is enabled, only the dependencies for the
                find_license_files method is checked.
                This allows a lightweight mode without the dependencies for the
                detect() method when only a list of valid license files is
                required.
        """

    @property
    def find_only(self):
        return self._find_only

    @abc.abstractmethod
    def detect(self, directory: StrPath) -> _LicenseDataT_co: ...
    def find_license_files(self, directory: StrPath) -> list[Path]:
        """
        Default implementation of find_license_files.

        Raises:
            LicenseError:
                Invalid manual license config entries are present in the license config
        """
        reuse_roots = get_go_module_dirs(Path(directory), relative_paths=True)
        license_file_lists = find_license_files(
            directory,
            relative_paths=True,
            exclude_directories=self.license_config["exclude_directories"],
            exclude_files=self.license_config["exclude_files"],
            reuse_roots=reuse_roots,
        )
        manual_license_map, unmatched = get_manual_license_entries(
            self.license_config["licenses"], directory
        )
        if unmatched:
            raise LicenseError(
                "Invalid manual license config entries:"
                + "\n"
                + "\n".join(map(str, unmatched)),
            )
        files: set[Path] = {
            Path(p) for p in chain.from_iterable(license_file_lists.values())
        }
        files.update(manual_license_map)
        return sorted(files)


class LicenseDetectorNotAvailableError(LicenseError):
    """
    Failed to load the requested license detector
    """
