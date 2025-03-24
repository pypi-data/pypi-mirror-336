#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
# Copyright (C) 2024 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from collections.abc import Collection, Iterable, Iterator, MutableSequence, Sequence
from contextlib import ExitStack, contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from textwrap import dedent
from typing import IO, Any, NamedTuple, cast

from license_expression import ExpressionError
from zstarfile import ZSTarfile

from go_vendor_tools import __version__
from go_vendor_tools.archive import get_toplevel_directory
from go_vendor_tools.cli.utils import (
    HAS_TOMLKIT,
    catch_vendor_tools_error,
    load_tomlkit_if_exists,
    need_tomlkit,
    tomlkit_dump,
)
from go_vendor_tools.config.base import load_config
from go_vendor_tools.config.licenses import (
    LicenseConfig,
    LicenseEntry,
    create_license_config,
)
from go_vendor_tools.exceptions import VendorToolsError
from go_vendor_tools.gomod import get_unlicensed_mods
from go_vendor_tools.hashing import get_hash
from go_vendor_tools.license_detection.base import LicenseData, LicenseDetector
from go_vendor_tools.license_detection.load import DETECTORS, get_detectors
from go_vendor_tools.licensing import compare_licenses, simplify_license
from go_vendor_tools.specfile import VendorSpecfile

if HAS_TOMLKIT:
    import tomlkit

try:
    import argcomplete
except ImportError:
    HAS_ARGCOMPLETE = False
else:
    HAS_ARGCOMPLETE = True

COLOR: bool | None = None
RED = "\033[31m"  # ]
CLEAR = "\033[0m"  # ]

MANUALLY_DETECTING_LICENSES_URL = "https://fedora.gitlab.io/sigs/go/go-vendor-tools/scenarios/#manually-detecting-licenses"


def red(__msg: str, /, *, file: IO[str] | None = None) -> None:
    file = cast(IO[str], sys.stdout if file is None else file)
    color = COLOR
    if color is None:
        color = file.isatty()
    print(f"{RED if color else ''}{__msg}{CLEAR if color else ''}", file=file)


def split_kv_options(kv_config: list[str]) -> dict[str, str]:
    results: dict[str, str] = {}
    for opt in kv_config:
        if ";" in opt:
            results |= split_kv_options(opt.split(";"))
        else:
            key, _, value = opt.partition("=")
            results[key] = value
    return results


def choose_license_detector(
    choice: str | None,
    license_config: LicenseConfig,
    kv_config: list[str] | None,
    find_only: bool = False,
) -> LicenseDetector:
    kv_config = kv_config or []
    cli_config = license_config["detector_config"] | split_kv_options(kv_config)
    available, missing = get_detectors(cli_config, license_config, find_only=find_only)
    if choice:
        if choice in missing:
            sys.exit(f"Failed to get detector {choice!r}: {missing[choice]}")
        return available[choice]
    if not available:
        print("Failed to load license detectors:", file=sys.stderr)
        for detector, err in missing.items():
            print(f"! {detector}: {err}")
        sys.exit(1)
    return next(iter(available.values()))


def _add_json_argument(parser: argparse.ArgumentParser, **kwargs) -> None:
    our_kwargs: dict[str, Any] = {
        "type": Path,
        "help": dedent(
            """\
        Write license data to a JSON file.
        This data is not yet considered stable and is only intended for
        go2rpm's internal usage and for testing purposes.
        """
        ).replace("\n", " "),
    }
    kwargs = our_kwargs | kwargs
    parser.add_argument("--write-json", **kwargs)


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Handle licenses for vendored go projects",
        prog="go_vendor_license",
    )
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("-c", "--config", type=Path, dest="config_path")
    parser.add_argument(
        "-C",
        "--path",
        "--directory",
        type=Path,
        dest="directory",
        action="append",
        help=dedent(
            """
        Can be one of the following:

        1. Top-level directory with a go.mod file and vendor directory
        2. If --use-archive is specified, treat as a tarball and unpack it. Can
           be specified multiple times to unpack multiple tarballs on
           top of one another.
        3. Path to a specfile.
           The paths to Source0 and Source1 will be automatically unpacked.
        """
        ),
    )
    parser.add_argument("--use-archive", action="store_true", help="See --path.")
    parser.add_argument(
        "--color",
        action=argparse.BooleanOptionalAction,
        default=False if os.environ.get("NO_COLOR") else None,
        help="Whether to use colored output."
        " Defaults to True if output is a TTY and $NO_COLOR is not defined.",
    )
    parser.add_argument(
        "-d",
        "--detector",
        choices=DETECTORS,
        default=None,
        help="Choose a license detector. Choices: %(choices)s. Default: autodetect",
        dest="detector_name",
    )
    parser.add_argument(
        "-D",
        "--dc",
        "--detector-config",
        help="`KEY=VALUE` pairs to pass to the license detector."
        " Can be passed multiple times."
        " Overrides settings defined in licensing.detector_config.",
        dest="detector_config",
        action="append",
    )
    parser.set_defaults(detector_find_only=False)
    subparsers = parser.add_subparsers(dest="subcommand")
    subparsers.required = True
    report_parser = subparsers.add_parser(
        "report",
        help="Main subcommand",
        description="This command detects licenses within the project tree."
        " It creates a license summary and a normalized SPDX expression",
    )
    report_parser.add_argument(
        "-i",
        "--ignore-undetected",
        action="store_true",
        help="Whether to show undetected licenses in the output",
    )
    report_parser.add_argument(
        "-L",
        "--ignore-unlicensed-mods",
        action="store_true",
        help="Whether to show Go modules without licenses in the output",
    )
    report_parser.add_argument(
        "--subpackage-name",
        help="""
        Which subpackage to use to find license tag.
        Name of a subpackage.

        - `-NAME` for `%%package NAME`;
        - `NAME` for `%%package -n NAME`;
        - Omit this args to use the main package definition
        """,
    )
    verify_opts = report_parser.add_mutually_exclusive_group()
    verify_opts.add_argument(
        "--verify",
        help="Verify license expression to make sure it matches caluclated expression",
        metavar="EXPRESSION",
    )
    verify_opts.add_argument(
        "--verify-spec", help="Verify specfile license tag", action="store_true"
    )
    verify_opts.add_argument(
        "--update-spec", help="Update specfile license tag", action="store_true"
    )
    report_parser.add_argument(
        "--prompt",
        action=argparse.BooleanOptionalAction,
        help="Whether to prompt to fill in undetected licenses."
        " Implies --write-config."
        " Default: %(default)s",
    )
    report_parser.add_argument(
        "mode",
        nargs="?",
        type=str,
        choices=("all", "expression", "list"),
        default="all",
        help="""
        - `all` — print out a breakdown of all license files and their detected
          license expression and then a final, cummluative expression.
        - `expression` — print only the cummulative SPDX expression
        - `list` — print the file-by-file breakdown only
        """,
    )
    _add_json_argument(report_parser)
    report_parser.add_argument(
        "--write-config", help="Write a base config.", action="store_true"
    )
    help_msg = "Add manual license entry to a config file"
    explict_parser = subparsers.add_parser(
        "explicit",
        help=help_msg,
        description=f"{help_msg}. See {MANUALLY_DETECTING_LICENSES_URL} for usage.",
    )
    explict_parser.add_argument(
        "-f",
        "--file",
        dest="license_file",
        required=True,
        type=Path,
        help="Path to file (relative to CWD) to add to license config",
    )
    explict_parser.add_argument("license_expression", help="SPDX license expression")
    install_parser = subparsers.add_parser(
        "install", description=f"INTERNAL: {install_command.__doc__}"
    )
    install_parser.add_argument(
        "--install-directory", dest="install_directory", type=Path, required=True
    )
    install_parser.add_argument(
        "--destdir", dest="install_destdir", type=Path, default=Path("/")
    )
    install_parser.add_argument(
        "--filelist", dest="install_filelist", type=Path, required=True
    )
    install_parser.set_defaults(detector_find_only=True)
    # TODO(gotmax23): Should we support writing JSON from the install command
    # or just reading it?
    # _add_json_argument(install_parser)
    generate_buildrequires_parser = subparsers.add_parser(
        "generate_buildrequires",
        description="Internal command for %%go_vendor_license_buildrequires",
    )
    generate_buildrequires_parser.add_argument(
        "--no-check",
        help="Whether to exclude dependencies for %%go_vendor_license_check",
        action="store_true",
        dest="detector_find_only",
    )
    return parser


def parseargs(argv: list[str] | None = None) -> argparse.Namespace:
    """
    Parse arguments and return an `argparse.Namespace`
    """
    parser = get_parser()
    if HAS_ARGCOMPLETE:
        argcomplete.autocomplete(parser)
    args = parser.parse_args(argv)
    args.directory = list(map(Path, args.directory or (".")))
    if args.subcommand not in ("explicit",):
        loaded = load_config(
            args.config_path, allow_missing=getattr(args, "write_config", False)
        )
        args.config = loaded["licensing"]
        if not args.detector_name:
            args.detector_name = args.config["detector"]
    if args.subcommand in ("report", "install"):
        args.detector = choose_license_detector(
            args.detector_name,
            args.config,
            args.detector_config,
            args.detector_find_only,
        )
        # TODO(anyone): Replace the print if/when we implement more granular logging
        print("Using detector:", args.detector.NAME, file=sys.stderr)
    global COLOR  # noqa: PLW0603
    COLOR = args.color
    return args


def bullet_iterator(it: Iterable[object], bullet: str = "- ") -> Iterator[str]:
    for item in it:
        yield bullet + str(item)


def red_if_true(items: Collection[object], message: str, bullet: str = "- ") -> None:
    if not items:
        return
    print(message)
    red("\n".join(bullet_iterator(items, bullet)))


def paths_relative_to_list(paths: Collection[Path], directory: Path) -> list[Path]:
    return [
        path.resolve().relative_to(directory.resolve()) if path.is_absolute() else path
        for path in paths
    ]


def print_licenses(
    results: LicenseData,
    unlicensed_mods: Collection[Path],
    mode: str,
    show_undetected: bool,
    show_unlicensed: bool,
    directory: Path,
) -> None:
    if mode in ("all", "list"):
        for (
            license_path,
            license_name,
        ) in results.license_map.items():
            print(f"{license_path}: {license_name}")
    if (
        results.undetected_licenses
        or unlicensed_mods
        or results.unmatched_extra_licenses
    ):
        if mode != "expression":
            print()
        if show_undetected:
            red_if_true(
                results.undetected_licenses,
                "The following license files were found "
                "but the correct license identifier couldn't be determined:",
            )
        if show_unlicensed:
            red_if_true(
                paths_relative_to_list(unlicensed_mods, directory),
                "The following modules are missing license files:",
            )
        red_if_true(
            results.unmatched_extra_licenses,
            "The following license files that were specified in the configuration"
            " have changed:",
        )
    if mode == "list":
        return
    if mode != "expression":
        print()
    print(results.license_expression)


def write_license_json(data: LicenseData, file: Path) -> None:
    with file.open("w", encoding="utf-8") as fp:
        json.dump(data.to_jsonable(), fp, indent=2)


class _PromptMissingResult(NamedTuple):
    data: LicenseData
    entries: MutableSequence[LicenseEntry]
    excludes: list[str]


# TODO(gotmax23): Unit test prompt_missing_licenses and write_config code.
# This'll require some mocking of the input() stuff.
def prompt_missing_licenses(
    data: LicenseData,
    entries: MutableSequence[LicenseEntry],
) -> _PromptMissingResult:
    excludes: list[str] = []
    if not data.undetected_licenses:
        return _PromptMissingResult(data, entries, excludes)
    print("Undetected licenses found! Please enter them manually.")
    undetected_licenses = set(data.undetected_licenses)
    license_map: dict[Path, str] = dict(data.license_map)
    for undetected in sorted(data.undetected_licenses):
        print(f"* Undetected license: {data.directory / undetected}")
        expression_str = input("Enter SPDX expression (or EXCLUDE): ")
        if expression_str == "EXCLUDE":
            undetected_licenses.remove(undetected)
            excludes.append(str(undetected))
            print("Adding file to licensing.exclude_files...")
            continue
        expression: str = (
            str(simplify_license(expression_str)) if expression_str else ""
        )
        print(f"Expression simplified to {expression!r}")
        license_map[undetected] = expression
        entry_dict = LicenseEntry(
            path=str(undetected),
            sha256sum=get_hash(data.directory / undetected),
            expression=expression,
        )
        replace_entry(entries, entry_dict, undetected)
        undetected_licenses.remove(undetected)
    assert not undetected_licenses
    return _PromptMissingResult(
        data.replace(undetected_licenses=undetected_licenses, license_map=license_map),
        entries,
        excludes,
    )


def _write_config_verify_path(config_path: Path | None) -> Path:
    if config_path:
        return config_path
    need_tomlkit("--write-config")

    default = Path.cwd() / "go-vendor-tools.toml"
    if not default.is_file():
        sys.exit("--write-config: Please pass --config to write configuration file!")
    else:
        print(
            "WARNING --write-config: No --config path specified"
            f" Will write to {default}",
            file=sys.stderr,
        )
    return config_path or default


def get_report_write_config_data(
    config_path: Path | None, detector: LicenseDetector
) -> tuple[Path, tomlkit.TOMLDocument]:
    need_tomlkit("--write-config")
    new_config_path = _write_config_verify_path(config_path)
    loaded = load_tomlkit_if_exists(config_path)
    write_config_data = loaded.setdefault("licensing", {})
    write_config_data["detector"] = detector.NAME
    if detector.detector_config:
        write_config_data["detector_config"] = detector.detector_config
    return new_config_path, loaded


def write_and_prompt_report_licenses(
    license_data: LicenseData, write_config_data: tomlkit.TOMLDocument
) -> LicenseData:
    # fmt: off
    license_config_list = (
        write_config_data
        .setdefault("licensing", {})
        .setdefault("licenses", tomlkit.aot() if HAS_TOMLKIT else [])
    )
    # fmt: on
    license_data, _, exclude_files = prompt_missing_licenses(
        license_data, license_config_list
    )
    if exclude_files:
        exclude_files_toml = write_config_data["licensing"].setdefault(  # type: ignore[union-attr]
            "exclude_files", []
        )
        exclude_files_toml.extend(exclude_files)
    return license_data


@contextmanager
def handle_alternative_sources_and_spec(
    directories: Sequence[Path], is_archive: bool, subpackage_name: str | None
) -> Iterator[tuple[Path, VendorSpecfile | None]]:
    with ExitStack() as es:
        spec: VendorSpecfile | None = None
        directories = list(directories)
        # The CLI code already checks that the value is greater than zero, so
        # assert is fine here
        assert directories
        if not is_archive and len(directories) > 1:
            sys.exit("Too many paths were passed!")

        if directories[0].suffix == ".spec":
            spec = es.enter_context(VendorSpecfile(directories[0], subpackage_name))
            directories[:] = spec.source0_and_source1()
            is_archive = True
        if is_archive:
            tmp = Path(es.enter_context(TemporaryDirectory()))
            # Extract the first archive
            with ZSTarfile.open(directories[0]) as tar:
                first_toplevel = get_toplevel_directory(tar)
                if not first_toplevel:
                    sys.exit(f"{directories[0]} does not have a top-level directory!")
                print(f"Extracting {directories[0]}", file=sys.stderr)
                tar.extractall(tmp)
            for directory in directories[1:]:
                with ZSTarfile.open(directory) as tar:
                    toplevel = get_toplevel_directory(tar)
                    print(f"Extracting {directory}", file=sys.stderr)
                    tar.extractall(tmp if toplevel else tmp / first_toplevel)
            yield tmp / first_toplevel, spec

        else:
            yield directories[0], spec


def report_command(args: argparse.Namespace) -> None:
    detector: LicenseDetector = args.detector
    paths: Sequence[Path] = args.directory
    ignore_undetected: bool = args.ignore_undetected
    ignore_unlicensed_mods: bool = args.ignore_unlicensed_mods
    mode: str = args.mode
    verify: str | None = args.verify
    write_json: Path | None = args.write_json
    write_config: bool = args.write_config or args.prompt
    prompt: bool = args.prompt
    config_path: Path | None = args.config_path
    use_archive: bool = args.use_archive
    subpackage_name: str | None = args.subpackage_name
    verify_spec: bool = args.verify_spec
    update_spec: bool = args.update_spec
    del args

    if write_config:
        config_path, loaded = get_report_write_config_data(config_path, detector)

    with handle_alternative_sources_and_spec(paths, use_archive, subpackage_name) as (
        directory,
        spec,
    ):
        if (verify_spec or update_spec) and not spec:
            raise VendorToolsError(
                "--path must be a path to a specfile"
                " if --verify-spec or --update-spec is passed"
            )
        license_data: LicenseData = detector.detect(directory)
        unlicensed_mods = (
            set()
            if ignore_unlicensed_mods
            else get_unlicensed_mods(directory, license_data.license_file_paths)
        )
        if prompt:
            license_data = write_and_prompt_report_licenses(license_data, loaded)
        failed = bool(
            (license_data.undetected_licenses and not ignore_undetected)
            or (unlicensed_mods and not ignore_unlicensed_mods)
            or license_data.unmatched_extra_licenses
        )
        print_licenses(
            license_data,
            unlicensed_mods,
            mode,
            not ignore_undetected,
            not ignore_unlicensed_mods,
            directory,
        )
        if write_json:
            write_license_json(license_data, write_json)
        if spec and verify_spec:
            verify = spec.license
        if (
            spec
            and update_spec
            and not compare_licenses(
                spec.license, exp := license_data.license_expression
            )
        ):
            if failed:
                print(
                    "Did not update specfile license tag due to above detector errors."
                )
            else:
                spec.license = str(exp)
        if write_config:
            tomlkit_dump(loaded, cast(Path, config_path))
    if verify and not compare_licenses(license_data.license_expression, verify):
        raise VendorToolsError("Failed to verify license. Expected ^")
    sys.exit(failed)


def _get_intermediate_directories(
    directory_parts: Collection[Sequence[str]],
) -> set[Path]:
    inter_parts = set()
    for parts in directory_parts:
        for i in range(len(parts)):
            inter_parts.add(Path(*parts[: i + 1]))
    return inter_parts


def copy_licenses(
    base_directory: Path,
    license_paths: Iterable[Path],
    install_destdir: Path,
    install_directory: Path,
    install_filelist: Path,
) -> None:
    installdir = install_destdir / install_directory.relative_to("/")
    base_directory = base_directory.resolve()

    entries: list[str] = []
    directory_parts: set[Sequence[str]] = set()
    installdir.mkdir(parents=True, exist_ok=True)
    entries.append(f"%license %dir {install_directory}")
    for lic in license_paths:
        resolvedpath = lic.resolve()
        relpath = resolvedpath.relative_to(base_directory)
        if len(relpath.parts) > 1:
            directory_parts.add(relpath.parts[:-1])
        (installdir / relpath).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(lic, installdir / relpath)
        entries.append(f"%license {install_directory / relpath}")
    entries.extend(
        f"%license %dir {install_directory / path}"
        for path in _get_intermediate_directories(directory_parts)
    )
    entries.sort()
    install_filelist.write_text("\n".join(entries) + "\n")


def install_command(args: argparse.Namespace) -> None:
    """
    Install license files into the license directory
    """
    directory: Path = args.directory[0]
    detector: LicenseDetector = args.detector
    install_destdir: Path = args.install_destdir
    install_directory: Path = args.install_directory
    install_filelist: Path = args.install_filelist
    del args

    license_files = detector.find_license_files(directory)
    copy_licenses(
        directory,
        license_files,
        install_destdir,
        install_directory,
        install_filelist,
    )


def get_relpath(base_directory: Path, path: Path) -> Path:
    if path.is_absolute():
        return path.relative_to(base_directory)
    return path


def replace_entry(
    data: MutableSequence[LicenseEntry], new_entry: LicenseEntry, relpath: Path
) -> None:
    for entry in data:
        if entry == new_entry:
            return
        if Path(entry["path"]) == relpath:
            cast(dict, entry).clear()
            entry.update(new_entry)
            return
    data.append(new_entry)


def explicit_command(args: argparse.Namespace) -> None:
    if not args.config_path:
        sys.exit("--config must be specified!")
    loaded = load_tomlkit_if_exists(args.config_path)

    if "licensing" not in loaded:
        loaded.add("licensing", tomlkit.table())
    data = loaded["licensing"]

    licenses = cast(dict, data).setdefault("licenses", tomlkit.aot())
    relpath = get_relpath(args.directory[0], args.license_file)
    try:
        expression = (
            simplify_license(args.license_expression) if args.license_expression else ""
        )
    except ExpressionError as exc:
        sys.exit(f"Failed to parse license: {exc}")
    entry = LicenseEntry(
        path=str(relpath),
        sha256sum=get_hash(args.license_file),
        expression=expression,
    )
    replace_entry(licenses, entry, relpath)
    tomlkit_dump(loaded, args.config_path)


def generate_buildrequires_command(args: argparse.Namespace) -> None:
    detector: str = args.detector_name
    find_only: bool = args.detector_find_only
    del args

    if not detector:
        # If the detector is not explicitly specified, attempt to fall back to
        # the one whose dependencies are already installed.
        available, missing = get_detectors({}, create_license_config())
        detector = next(iter(available), "") or next(iter(missing))
    elif detector not in DETECTORS:
        sys.exit(f"{detector!r} does not exist! Choices: {tuple(DETECTORS)}")
    detector_cls = DETECTORS[detector]
    for requirement in (
        detector_cls.FIND_PACKAGES_NEEDED if find_only else detector_cls.PACKAGES_NEEDED
    ):
        print(requirement)


def main(argv: list[str] | None = None) -> None:
    args = parseargs(argv)
    with catch_vendor_tools_error():
        if args.subcommand == "report":
            report_command(args)
        elif args.subcommand == "explicit":
            explicit_command(args)
        elif args.subcommand == "install":
            install_command(args)
        elif args.subcommand == "generate_buildrequires":
            generate_buildrequires_command(args)


if __name__ == "__main__":
    main()
