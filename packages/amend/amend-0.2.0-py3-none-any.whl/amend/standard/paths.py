# Copyright 2025 Miljenko Šuflaj
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pathlib import Path
from typing import Literal
import warnings

from amend.built_in.numbers.integers import amend_integer


def amend_directory(
    directory,
    instance_mismatch_action: Literal[
        "error",
        "warning",
    ] = None,
    value_on_cast_error: Path = None,
    not_existing_action: Literal[
        "error",
        "warning",
        "make",
    ] = None,
    category_mismatch_action: Literal[
        "error",
        "warning",
        "take-parent",
    ] = None,
    warning_stack_level: int = None,
) -> Path:
    if instance_mismatch_action not in (
        None,
        "error",
        "warning",
    ):
        raise ValueError(
            f"Invalid instance mismatch action {repr(instance_mismatch_action)}"
        )
    if not (
        value_on_cast_error is None
        or (
            isinstance(
                value_on_cast_error,
                Path,
            )
            and (value_on_cast_error.is_dir() or not value_on_cast_error.exists())
        )
    ):
        raise ValueError(f"Invalid value on cast error {repr(value_on_cast_error)}")
    if not_existing_action not in (
        None,
        "error",
        "warning",
        "make",
    ):
        raise ValueError(f"Invalid not-existing action {repr(not_existing_action)}")

    if category_mismatch_action not in (
        None,
        "error",
        "warning",
        "take-parent",
    ):
        raise ValueError(
            f"Invalid category mismatch action {repr(category_mismatch_action)}"
        )
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )

    if not isinstance(
        directory,
        Path,
    ):
        if instance_mismatch_action is not None:
            message = f"Entity {repr(directory)} isn't a pathlib.Path"
            if instance_mismatch_action == "error":
                raise TypeError(message)
            elif instance_mismatch_action == "warning":
                warnings.warn(
                    message,
                    UserWarning,
                    warning_stack_level,
                )
        try:
            directory = str(directory)
            directory = Path(directory)
        except Exception:
            if value_on_cast_error is None:
                raise TypeError(f"Failed to cast {repr(directory)} to pathlib.Path")

            directory = value_on_cast_error

    if not_existing_action is not None and not directory.exists():
        message = f"Directory {directory} is missing"
        if not_existing_action == "error":
            raise OSError(message)
        elif not_existing_action == "warning":
            warnings.warn(
                message,
                UserWarning,
                warning_stack_level,
            )
        elif not_existing_action == "make":
            try:
                directory.mkdir(
                    parents=True,
                    exist_ok=True,
                )
                assert directory.exists()
            except Exception as e:
                raise OSError(f"Failed to make directory {directory}:\n{e}")

    if (
        category_mismatch_action is not None
        and directory.exists()
        and not directory.is_dir()
    ):
        message = f"Path {directory} isn't a directory"
        if category_mismatch_action == "error":
            raise NotADirectoryError(message)
        elif category_mismatch_action == "warning":
            warnings.warn(
                message,
                UserWarning,
                warning_stack_level,
            )
        elif category_mismatch_action == "take-parent":
            try:
                proposed_directory = directory.parent
                assert proposed_directory.is_dir()
                directory = proposed_directory
            except Exception:
                raise OSError(
                    f"Path {directory}'s parent {proposed_directory} isn't a directory"
                )

    return directory


def amend_file(
    file,
    instance_mismatch_action: Literal[
        "error",
        "warning",
    ] = None,
    value_on_cast_error: Path = None,
    not_existing_action: Literal[
        "error",
        "warning",
        "make",
        "make-parent",
    ] = None,
    category_mismatch_action: Literal[
        "error",
        "warning",
    ] = None,
    warning_stack_level: int = None,
) -> Path:
    if instance_mismatch_action not in (
        None,
        "error",
        "warning",
    ):
        raise ValueError(
            f"Invalid instance mismatch action {repr(instance_mismatch_action)}"
        )
    if not (
        value_on_cast_error is None
        or (
            isinstance(
                value_on_cast_error,
                Path,
            )
            and (value_on_cast_error.is_file() or not value_on_cast_error.exists())
        )
    ):
        raise ValueError(f"Invalid value on cast error {repr(value_on_cast_error)}")
    if not_existing_action not in (
        None,
        "error",
        "warning",
        "make",
        "make-parent",
    ):
        raise ValueError(f"Invalid not-existing action {repr(not_existing_action)}")
    if category_mismatch_action not in (
        None,
        "error",
        "warning",
    ):
        raise ValueError(
            f"Invalid category mismatch action {repr(category_mismatch_action)}"
        )
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )

    if (
        not isinstance(
            file,
            Path,
        )
        and instance_mismatch_action is not None
    ):
        message = f"Entity {repr(file)} isn't a pathlib.Path"
        if instance_mismatch_action == "error":
            raise TypeError(message)
        elif instance_mismatch_action == "warning":
            warnings.warn(
                message,
                UserWarning,
                warning_stack_level,
            )

    try:
        file = str(file)
        file = Path(file)
    except Exception:
        if value_on_cast_error is None:
            raise TypeError(f"Failed to cast {repr(file)} to pathlib.Path")

        file = value_on_cast_error

    if not_existing_action is not None and not file.exists():
        message = f"File {file} is missing"
        if not_existing_action == "error":
            raise OSError(message)
        elif not_existing_action == "warning":
            warnings.warn(
                message,
                UserWarning,
                warning_stack_level,
            )
        elif not_existing_action in (
            "make",
            "make-parent",
        ):
            amend_directory(
                directory=file.parent,
                not_existing_action="make",
                warning_stack_level=warning_stack_level + 1,
            )

            if not_existing_action == "make":
                try:
                    with open(
                        file,
                        mode="a",
                    ):
                        pass
                    assert file.exists()
                except Exception as e:
                    raise OSError(f"Failed to make file {file}:\n{e}")

    if category_mismatch_action is not None and file.exists() and not file.is_file():
        message = f"Path {file} isn't a file"
        if category_mismatch_action == "error":
            raise ValueError(message)
        elif category_mismatch_action == "warning":
            warnings.warn(
                message,
                UserWarning,
                warning_stack_level,
            )

    return file
