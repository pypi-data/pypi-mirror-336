#!/usr/bin/env python3
#
# Generates src/uts46/_data.py from:
# - The UTS46 section 5 IDNA Mapping Table data found at
#   https://www.unicode.org/Public/idna/16.0.0/IdnaMappingTable.txt

import sys
import textwrap
from collections.abc import Iterator
from dataclasses import dataclass
from itertools import chain
from pathlib import Path
from typing import Any
from unicodedata import unidata_version

try:
    # Running as a module (or type checking)
    from tools import unicode_data_utils as udu
except ImportError:
    # Running as script
    import unicode_data_utils as udu  # type: ignore[import, no-redef]

try:
    import tomllib  # type: ignore[import-not-found]
except ImportError:
    import tomli as tomllib  # type: ignore[import-not-found]


# Output file
OUTPUT_PATH = Path(__file__).parent.parent / "src" / "uts46" / "_data.py"


def get_package_config() -> dict[str, Any]:
    """Return the package configuration from pyproject.toml as a dict."""
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    if not pyproject_path.exists():
        raise FileNotFoundError(f"Could not find `pyproject.toml` at {pyproject_path}")

    with pyproject_path.open("rb") as f:
        pyproject_data = tomllib.load(f)

    try:
        package_name = pyproject_data["project"]["name"]
    except KeyError as e:
        raise KeyError("Couldn't find [project] name in pyproject.toml") from e

    try:
        result = pyproject_data["tool"][package_name]["generate-data"]
    except KeyError as e:
        raise KeyError(
            f"Couldn't find [tool.{package_name}.generate-data] name in pyproject.toml"
        ) from e

    assert isinstance(result, dict)
    return result


CodePoint = int
CodePointRange = tuple[CodePoint, CodePoint]


@dataclass
class IdnaMappingEntry:
    """Parsed line of UTS46 mapping table data."""

    start: CodePoint
    end: CodePoint
    status: str
    mapping: str | None = None
    line_num: int | None = None
    comment: str | None = None

    # Difference between mapping's codepoint and start,
    # if start == end and mapping is a single character
    offset: int | None = None

    def __post_init__(self) -> None:
        if self.status == "deviation" and self.mapping is None:
            # An empty deviation maps to empty string, not None
            self.mapping = ""
        if self.status in {"mapped", "deviation"}:
            # Mapped and deviation define a mapping
            assert self.mapping is not None, f"Range missing mapping: {self}"
        else:
            assert self.mapping is None, f"Range has unexpected mapping: {self}"

        if (
            self.status == "mapped"
            and self.start == self.end
            and self.mapping is not None
            and len(self.mapping) == 1
        ):
            self.offset = ord(self.mapping) - self.start

    def __str__(self) -> str:
        info = f"start=0x{self.start:04X}, end=0x{self.end:04X}, status={self.status!r}"
        if self.mapping is not None:
            info += f", mapping={self.mapping!r}"
        if self.line_num is not None:
            info += f", line_num={self.line_num}"
        if self.offset is not None:
            info += f", offset={self.offset}"
        if self.comment is not None:
            info += f", comment={self.comment!r}"
        return f"{self.__class__.__name__}({info})"

    def merge(self, other: "IdnaMappingEntry") -> None:
        """
        Update self to combine other's start-end range and comment.

        Caller is responsible for ensuring remaining properties are compatible.
        """
        self.start = min(self.start, other.start)
        self.end = max(self.end, other.end)

        if self.comment is None:
            self.comment = other.comment
        elif other.comment is not None:
            # Merge comments.
            left, *_ = self.comment.split("..")
            *_, right = other.comment.rsplit("..")
            self.comment = f"{left}..{right}"


def parse_mapping_table(file_path: Path) -> list[IdnaMappingEntry]:
    """Parse the UTS46 mapping table data file."""
    ranges = []
    for line_num, content, comment in udu.parse_data_file(file_path):
        fields = udu.parse_semicolon_fields(content)
        start, end = udu.parse_codepoint_field(fields[0])
        status = fields[1]

        mapping = None
        if len(fields) >= 3 and fields[2]:
            mapping = udu.parse_codepoint_sequence_field(fields[2])

        if status == "valid":
            assert mapping is None, (
                f"Unexpected mapping for valid range: {line_num}: {content}"
            )

        ranges.append(
            IdnaMappingEntry(
                start,
                end,
                status,
                mapping,
                line_num=line_num,
                comment=comment,
            )
        )

    return ranges


def extract_deviations(ranges: list[IdnaMappingEntry]) -> dict[CodePoint, str]:
    """
    Extract the deviation mapping for transitional processing,
    and modify the ranges in place for non-transitional processing.
    """
    deviations: dict[CodePoint, str] = {}
    for r in ranges:
        if r.status == "deviation":
            for cp in range(r.start, r.end + 1):
                assert r.mapping is not None, f"Missing mapping for {r}"
                deviations[cp] = r.mapping
            r.status = "valid"
            r.mapping = None

    # Special case for U+1E9E capital sharp s (ẞ) (see UTS46 section 4 step 1)
    deviations[0x1E9E] = "ss"
    return deviations


def optimize_ranges(ranges: list[IdnaMappingEntry]) -> list[IdnaMappingEntry]:
    """
    Optimize by combining ranges where possible.
    """
    print(f"Optimizing {len(ranges)} ranges...", file=sys.stderr)

    # Ranges should already be sorted, but just in case...
    ranges.sort(key=lambda r: r.start)

    # Pass 1: Merge adjacent ranges with compatible properties.
    merged_ranges: list[IdnaMappingEntry] = []
    last: IdnaMappingEntry | None = None
    for curr in ranges:
        if last:
            # Combine equivalent entries
            if last.status == curr.status and last.mapping == curr.mapping:
                last.merge(curr)
                continue
            # Optimization: combine mapped entries with the same offset,
            # to reduce the number of individual items in the `mapped` dict.
            # (Occurs frequently for alphabetic ranges.)
            if (
                curr.status == "mapped"
                and curr.offset is not None
                and last.status in {"offset", "mapped"}
                and last.offset == curr.offset
            ):
                last.status = "offset"
                last.mapping = None
                last.merge(curr)
                continue
        merged_ranges.append(curr)
        last = curr

    print(f"  {len(merged_ranges)} ranges after merging", file=sys.stderr)

    # Pass 2: Merge compatible ranges that are separated only by "mapped" entries.
    # This works because Uts46MappingTable always checks the `mapped` dict first.
    elided_ranges: list[IdnaMappingEntry] = []
    last = None
    for curr in merged_ranges:
        if curr.status == "mapped":
            elided_ranges.append(curr)
            continue
        if (
            last is not None
            and last.status == curr.status
            and last.mapping == curr.mapping
            and last.offset == curr.offset
        ):
            last.merge(curr)
            continue
        elided_ranges.append(curr)
        last = curr

    print(
        f"  {len(elided_ranges)} ranges after eliding around 'mapped'", file=sys.stderr
    )

    return elided_ranges


def generate_dict_arg(
    name: str, mapping: dict[CodePoint, str], *, indent: int = 4
) -> Iterator[str]:
    """Generate argument initializer for a Unicode mapping dict literal."""
    space = " " * indent
    yield f"{space}{name}={{"
    for cp, value in mapping.items():
        vrepr = repr(value)
        # Use double quotes if possible (matching ruff)
        if vrepr.startswith("'") and vrepr.endswith("'") and '"' not in vrepr[1:-1]:
            vrepr = f'"{vrepr[1:-1]}"'
        yield f"{space}{space}0x{cp:04X}: {vrepr},"
    yield f"{space}}},"


def generate_rangelist_arg(
    name: str, ranges: list[CodePointRange] | list[IdnaMappingEntry], *, indent: int = 4
) -> Iterator[str]:
    """Generate argument initializer for a CodePointList."""
    space = " " * indent
    yield f"{space}{name}=["
    for r in ranges:
        start, end = (r.start, r.end) if isinstance(r, IdnaMappingEntry) else r
        if start == end:
            # Compact single codepoint form
            yield f"{space}{space}0x{start:04X},"
        else:
            yield f"{space}{space}(0x{start:04X}, 0x{end:04X}),"
    yield f"{space}],"


def generate_offsetlist_arg(
    name: str, ranges: list[IdnaMappingEntry], *, indent: int = 4
) -> Iterator[str]:
    """Generate argument initializer for an offset list."""
    space = " " * indent
    yield f"{space}{name}=["
    for r in ranges:
        yield f"{space}{space}((0x{r.start:04X}, 0x{r.end:04X}), {r.offset}),"
    yield f"{space}],"


def generate_file_header() -> Iterator[str]:
    """Generate the header for the _data.py file."""
    yield "# DO NOT EDIT! This file is generated by tools/generate-data.py."


def extract_header_comment(file_path: Path) -> Iterator[str]:
    """Extract the header comment block from a Unicode data file."""
    with file_path.open(encoding="utf-8") as f:
        lookahead: list[str] = []  # lines containing only "#"
        for line in f:
            if not line.startswith("#"):
                # End of header comment block
                break
            line = line.rstrip()
            if line == "#":
                # Blank comment line -- wait to see if any non-blank lines follow.
                lookahead.append(line)
            else:
                if lookahead:
                    yield from lookahead
                    lookahead = []
                yield line
        # Any leftover lookahead is trailing blank comment lines -- just skip it.


line_width = 80
comment_wrapper = textwrap.TextWrapper(
    width=line_width - 2,  # leave a little right margin
    initial_indent="# ",
    subsequent_indent="# ",
    break_long_words=False,
    break_on_hyphens=False,
)


def generate_source_header(
    section: str, source_path: Path, source_url: str
) -> Iterator[str]:
    horizontal_rule = "# " + "-" * (line_width - 2)

    yield ""
    yield horizontal_rule
    yield from comment_wrapper.wrap(section)
    yield f"# {source_url}"  # (don't try to wrap an url)
    # Inline the source data's header comment block
    yield horizontal_rule
    for comment in extract_header_comment(source_path):
        if comment.startswith("# "):
            yield from comment_wrapper.wrap(comment[2:])
        else:
            yield comment
    yield horizontal_rule


def generate_imports() -> Iterator[str]:
    """Generate import statements for the _data.py file."""
    yield "from ._datamodels import ("
    yield "    JoiningTypes,"
    yield "    Uts46MappingTable,"
    yield "    Uts46TransitionalMappingTable,"
    yield ")"


def generate_uts46_mapping(
    ranges: list[IdnaMappingEntry], data_version: str
) -> Iterator[str]:
    """Generate initializer for the non-transitional mapping."""
    # Partition by status
    status_ranges: dict[str, list[IdnaMappingEntry]] = {}
    for r in ranges:
        status_ranges.setdefault(r.status, []).append(r)
    mapped: dict[CodePoint, str] = {
        cp: r.mapping if r.mapping is not None else ""
        for r in status_ranges.get("mapped", [])
        for cp in range(r.start, r.end + 1)
    }

    yield ""
    yield "uts46_mapping = Uts46MappingTable("
    yield f'    data_version="{data_version}",'
    yield f'    unidata_version="{unidata_version}",'

    # Emit non-mapped statuses as range lists (skipping default disallowed status)
    yield from generate_rangelist_arg("valid", status_ranges.get("valid", []))
    yield from generate_rangelist_arg("ignored", status_ranges.get("ignored", []))

    # Emit mapped statuses
    yield from generate_offsetlist_arg("offset", status_ranges.get("offset", []))
    yield from generate_dict_arg("mapped", mapped)

    yield ")"


def generate_uts46_transitional_mapping(
    deviations: dict[CodePoint, str],
) -> Iterator[str]:
    """Generate initializer for the transitional mapping."""
    yield ""
    yield "uts46_transitional_mapping = Uts46TransitionalMappingTable("
    yield "    base=uts46_mapping,"
    yield from generate_dict_arg("deviations", deviations)
    yield ")"


def parse_joining_types(file_path: Path) -> list[tuple[CodePointRange, str]]:
    """Parse the DerivedJoiningType.txt file."""
    ranges = []
    for _, content, _ in udu.parse_data_file(file_path):
        fields = udu.parse_semicolon_fields(content)
        start, end = udu.parse_codepoint_field(fields[0])
        joining_type = fields[1]
        ranges.append(((start, end), joining_type))

    return ranges


def generate_joining_types(
    ranges: list[tuple[CodePointRange, str]], data_version: str
) -> Iterator[str]:
    """Generate initializer for the joining types RangeMap."""
    # Partition ranges by joining type
    ranges_by_type: dict[str, list[CodePointRange]] = {}
    for (start, end), joining_type in ranges:
        ranges_by_type.setdefault(joining_type, []).append((start, end))

    yield ""
    yield "joining_types = JoiningTypes("
    yield f'    data_version="{data_version}",'
    for joining_type, ranges_for_type in ranges_by_type.items():
        yield from generate_rangelist_arg(joining_type.lower(), ranges_for_type)
    yield ")"


def generate_data_file() -> None:
    """Generate the UTS46 mapping tables."""

    package_config = get_package_config()
    uts46_data_version = package_config["uts46-data-version"]
    joining_types_data_version = package_config["joining-types-data-version"]

    # Download and parse the mapping table
    mapping_path, mapping_url = udu.get_unicode_file(
        udu.IDNA_MAPPING_TABLE_URL, version=uts46_data_version
    )
    ranges = parse_mapping_table(mapping_path)
    deviations = extract_deviations(ranges)
    ranges = optimize_ranges(ranges)

    # Download and parse the joining types table
    joining_path, joining_url = udu.get_unicode_file(
        udu.DERIVED_JOINING_TYPE_URL, version=joining_types_data_version
    )
    joining_ranges = parse_joining_types(joining_path)

    # Generate the Python code
    code_lines = chain(
        generate_file_header(),
        generate_imports(),
        generate_source_header("UTS46 IDNA Mapping Tables", mapping_path, mapping_url),
        generate_uts46_mapping(ranges, uts46_data_version),
        generate_uts46_transitional_mapping(deviations),
        generate_source_header("Unicode Joining Types", joining_path, joining_url),
        generate_joining_types(joining_ranges, joining_types_data_version),
    )

    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        for line in code_lines:
            f.write(line + "\n")

    print(f"Generated {OUTPUT_PATH}", file=sys.stderr)


if __name__ == "__main__":
    generate_data_file()
