# Copyright (C) 2024 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT

"""
scancode-toolkit-based license detector backend
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from typing import TYPE_CHECKING, Any, NamedTuple, TypedDict, cast

from go_vendor_tools.gomod import get_go_module_dirs
from go_vendor_tools.license_detection.search import find_license_files

try:
    import scancode.api  # type: ignore[import]
except ImportError:
    HAS_SCANCODE = False
else:
    HAS_SCANCODE = True

from go_vendor_tools.config.licenses import LicenseConfig
from go_vendor_tools.license_detection.base import (
    LicenseData,
    LicenseDetector,
    LicenseDetectorNotAvailableError,
    get_manual_license_entries,
    reuse_path_to_license_map,
)
from go_vendor_tools.licensing import combine_licenses

if TYPE_CHECKING:
    from _typeshed import StrPath


class ScancodeLicenseDict(TypedDict):
    """
    License data returned by the scancode library
    """

    detected_license_expression: str
    detected_license_expression_spdx: str
    license_detections: list[dict[str, Any]]
    license_clues: list[Any]
    percentage_of_license_text: float


class ScancodeResult(NamedTuple):
    scancode_license_data: dict[str, ScancodeLicenseDict]
    simplified_map: dict[Path, str]
    undetected: set[Path]


def get_scancode_license_data(
    directory: Path,
    files: Iterable[Path],
) -> ScancodeResult:
    data_dicts: dict[str, ScancodeLicenseDict] = {}
    simplified_map: dict[Path, str] = {}
    undetected: set[Path] = set()
    for file in files:
        data = cast(
            ScancodeLicenseDict, scancode.api.get_licenses(str(directory / file))
        )
        data["license_detections"].sort(
            key=lambda d: d.get("license_expression_spdx", "")
        )
        data_dicts[str(file)] = data

        if data["detected_license_expression_spdx"] is None:
            undetected.add(file)
        else:
            simplified_map[file] = data["detected_license_expression_spdx"]
    return ScancodeResult(data_dicts, simplified_map, undetected)


@dataclass()
class ScancodeLicenseData(LicenseData):
    """
    scancode-toolkit-specific LicenseData implementation
    """

    scancode_license_data: dict[str, ScancodeLicenseDict]
    _combine_licenses = staticmethod(partial(combine_licenses, recursive_simplify=True))


class ScancodeLicenseDetector(LicenseDetector[ScancodeLicenseData]):
    NAME = "scancode"
    PACKAGES_NEEDED = ("go-vendor-tools+scancode",)

    def __init__(
        self,
        detector_config: dict[str, str],
        license_config: LicenseConfig,
        find_only: bool = False,
    ) -> None:
        self._find_only = find_only
        if not self.find_only and not HAS_SCANCODE:
            raise LicenseDetectorNotAvailableError(
                "The scancode-toolkit library must be installed!"
            )
        self.detector_config = detector_config
        self.license_config = license_config

    def detect(self, directory: StrPath):
        if self.find_only:
            raise ValueError(
                "This cannot be called when class was initalized with find_only=True"
            )
        directory = Path(directory)
        reuse_roots = get_go_module_dirs(Path(directory), relative_paths=True)
        license_file_lists = find_license_files(
            directory,
            relative_paths=True,
            exclude_directories=self.license_config["exclude_directories"],
            exclude_files=self.license_config["exclude_files"],
            reuse_roots=reuse_roots,
        )
        data, license_map, undetected = get_scancode_license_data(
            directory, map(Path, license_file_lists["license"])
        )
        manual_license_map, manual_unmatched = get_manual_license_entries(
            self.license_config["licenses"], directory
        )
        license_map |= manual_license_map
        license_map |= reuse_path_to_license_map(license_file_lists["reuse"])
        return ScancodeLicenseData(
            directory=directory,
            license_map=license_map,
            undetected_licenses=undetected,
            unmatched_extra_licenses=manual_unmatched,
            scancode_license_data=data,
            # FIXME(gotmax): Change the design of LicenseData to not require full paths
            extra_license_files=[
                Path(directory, file) for file in license_file_lists["notice"]
            ],
            detector_name=self.NAME,
        )
