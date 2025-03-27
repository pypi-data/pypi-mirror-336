"""Module contains functions for open and resolve yaml schema files.

Exemple:

>>> schema = open_schema("api.yaml")
"""
from __future__ import annotations

from typing import Any
from pathlib import Path

from urllib.parse import urlparse
import yaml
try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader

from .schema import Schema
from .exceptions import RefNotFoundError


def open_schema(root_file_path: Path | str) -> Schema:
    """Open schema."""
    root_file_path = Path(root_file_path).resolve()
    schema_files = open_schema_file(root_file_path)
    resolve_value(
        schema_files,
        root_file_path,
        schema_files[root_file_path],
        {},
    )
    return Schema(schema_files[root_file_path])


def open_schema_file(file_path: Path) -> dict:
    """Open and parse schema file. Function open recuesive other files,
    if the file contains refs.
    """
    files = {}
    unresolved = [file_path]
    while unresolved:
        file_path_ = unresolved.pop()
        with Path.open(file_path_, encoding="utf-8") as fp:
            value = yaml.load(fp, Loader=SafeLoader)
        files[file_path_] = value
        unresolved.extend(
            x for x in {ref[0] for ref in get_refs(files, file_path_, value)}
            if x not in files
        )
    return files


def get_refs(files: dict[Path, Any], base_path: Path, value: Any) -> set:
    """Get all refs from value."""
    result = set()
    if isinstance(value, dict):
        for k, v in value.items():
            if k == "$ref":
                result.add(create_ref(base_path, v))
            else:
                result |= get_refs(files, base_path, v)
        # resolve discriminator mapping
        if "mapping" in value and isinstance(value["mapping"], dict):
            result |= {
                create_ref(base_path, v) for v in value["mapping"].values()
            }
    if isinstance(value, list):
        for i in value:
            result |= get_refs(files, base_path, i)
    return result


def resolve_ref(
    files: dict[Path, Any],
    ref: tuple[Path, str],
    cache: dict[tuple[Path, str], Any],
) -> Any:
    """Get and resolve value referenced by ref."""
    if ref in cache:
        return cache[ref]
    value = get_value_by_ref(files, ref)
    if value is None:
        return None
    resolve_value(files, ref[0], value, cache)
    cache[ref] = value
    return value


def resolve_value(
    files: dict[Path, Any],
    file_path: Path,
    value: Any,
    cache: dict[tuple[Path, str], Any],
) -> None:
    """Recurcive find and replace $ref in value."""
    if isinstance(value, dict):
        _resolve_dict(files, file_path, value, cache)
    if isinstance(value, list):
        for i in value:
            if isinstance(i, (list, dict)):
                resolve_value(files, file_path, i, cache)


def _resolve_dict(
    files: dict[Path, Any],
    file_path: Path,
    value: dict[str, Any],
    cache: dict[tuple[Path, str], Any],
) -> None:
    resolved_keys = set()
    if "$ref" in value:
        ref = value.pop("$ref")
        ref_value = resolve_ref(files, create_ref(file_path, ref), cache)
        if ref_value is None:
            raise RefNotFoundError(file_path, ref)
        resolved_keys = set(ref_value) - set(value)
        value.update({**ref_value, **value})
    # resolve discriminator mapping
    if "mapping" in value and isinstance(value["mapping"], dict):
        value["mapping"].update({
            k: resolve_ref(files, create_ref(file_path, v), cache)
            for k, v in value["mapping"].items()
            if isinstance(v, str)
        })
    for k, v in value.items():
        if k in resolved_keys:
            continue
        if isinstance(v, (list, dict)):
            resolve_value(files, file_path, v, cache)


def get_value_by_ref(
    files: dict[Path, Any],
    ref: tuple[Path, str],
) -> dict | None:
    """Get value referenced by ref."""
    value = files.get(ref[0])
    if value is None:
        return None
    for key in ref[1].split("/")[1:]:
        try:
            value = value[key]
        except KeyError as exc:
            raise RefNotFoundError(ref[0], ref[1][1:]) from exc
        if value is None:
            return None
    return value


def create_ref(file_path: Path, ref_str: str) -> tuple[Path, str]:
    """Create ref obj from ref string."""
    ref = urlparse(ref_str)
    if not (ref.fragment and not ref.netloc and not ref.query):
        msg = f"Cannot resolve ref: {ref_str}"
        raise ValueError(msg)
    path = Path(file_path).parent / ref.path if ref.path else file_path
    return path, ref.fragment
