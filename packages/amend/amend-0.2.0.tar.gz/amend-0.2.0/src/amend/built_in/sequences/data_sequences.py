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

from typing import (
    Iterable,
    Literal,
    Type,
)
import warnings

from amend.built_in.numbers.integers import amend_integer
from amend.utilities.normalization import (
    _normalize_length_of_data_sequence,
    determine_length_normalization_strategy,
)


def _amend_data_sequence(
    data_sequence_type: Type[bytearray] | Type[bytes] | Type[str],
    data_sequence,
    instance_mismatch_action: Literal[
        "error",
        "warning",
    ] = None,
    value_on_cast_error: bytes | str = None,
    minimum_length: int = None,
    maximum_length: int = None,
    length_is_multiple_of: Iterable[int] = None,
    length_violation_action: Literal[
        "error",
        "warning",
        "truncate-and-pad",
    ] = None,
    truncation_side: Literal[
        "left",
        "right",
        "both-but-prioritize-left",
        "both-but-prioritize-right",
    ] = None,
    padding_side: Literal[
        "left",
        "right",
        "both-but-prioritize-left",
        "both-but-prioritize-right",
    ] = None,
    padding_value: bytearray | bytes | str = None,
    warning_stack_level: int = None,
) -> bytearray | bytes | str:
    if data_sequence_type not in (
        bytearray,
        bytes,
        str,
    ):
        raise ValueError(f"Invalid data sequence type {repr(data_sequence_type)}")
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
            data_sequence_type
            in (
                bytearray,
                bytes,
            )
            and isinstance(
                value_on_cast_error,
                bytes,
            )
        )
        or (
            data_sequence == str
            and isinstance(
                value_on_cast_error,
                str,
            )
        )
    ):
        raise ValueError(f"Invalid value on cast error {repr(value_on_cast_error)}")
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )
    if length_violation_action not in (
        None,
        "error",
        "warning",
        "truncate-and-pad",
    ):
        raise ValueError(
            f"Invalid length violation action {repr(length_violation_action)}"
        )
    if not isinstance(
        data_sequence,
        data_sequence_type,
    ):
        if instance_mismatch_action is not None:
            message = f"Entity {repr(data_sequence)} isn't {data_sequence_type}"
            if instance_mismatch_action == "error":
                raise TypeError(message)
            elif instance_mismatch_action == "warning":
                warnings.warn(
                    message,
                    UserWarning,
                    warning_stack_level,
                )
        try:
            data_sequence = data_sequence_type(data_sequence)
        except Exception:
            if value_on_cast_error is None:
                raise TypeError(
                    f"Failed to cast {repr(data_sequence)} to {data_sequence_type}"
                )

            data_sequence = value_on_cast_error
            data_sequence = data_sequence_type(data_sequence)

    proposed_length_changes = determine_length_normalization_strategy(
        length=len(data_sequence),
        minimum_length=minimum_length,
        maximum_length=maximum_length,
        length_is_multiple_of=length_is_multiple_of,
        truncation_side=truncation_side,
        padding_side=padding_side,
        warning_stack_level=warning_stack_level + 1,
    )
    if proposed_length_changes != (
        0,
        0,
    ):
        message = (
            f"Entity {repr(data_sequence)} has incorrect length {len(data_sequence)}"
        )
        if length_violation_action == "error":
            raise ValueError(message)
        elif length_violation_action == "warning":
            warnings.warn(
                message,
                UserWarning,
                warning_stack_level,
            )
        else:
            if proposed_length_changes == None:
                raise ValueError(
                    "".join(
                        (
                            "Impossible to satisfy length constraints for ",
                            f"{repr(data_sequence)}",
                        )
                    )
                )

        data_sequence = _normalize_length_of_data_sequence(
            data_sequence_type=data_sequence_type,
            data_sequence=data_sequence,
            proposed_length_change=proposed_length_changes,
            padding_value=padding_value,
            warning_stack_level=warning_stack_level + 1,
        )

    return data_sequence


def amend_immutable_binary(
    immutable_binary,
    instance_mismatch_action: Literal[
        "error",
        "warning",
    ] = None,
    value_on_cast_error: bytes = None,
    minimum_length: int = None,
    maximum_length: int = None,
    length_is_multiple_of: Iterable[int] = None,
    length_violation_action: Literal[
        "error",
        "warning",
        "truncate-and-pad",
    ] = None,
    truncation_side: Literal[
        "left",
        "right",
        "both-but-prioritize-left",
        "both-but-prioritize-right",
    ] = None,
    padding_side: Literal[
        "left",
        "right",
        "both-but-prioritize-left",
        "both-but-prioritize-right",
    ] = None,
    padding_value: bytes = None,
    warning_stack_level: int = None,
) -> bytes:
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )

    return _amend_data_sequence(
        data_sequence_type=bytes,
        data_sequence=immutable_binary,
        instance_mismatch_action=instance_mismatch_action,
        value_on_cast_error=value_on_cast_error,
        minimum_length=minimum_length,
        maximum_length=maximum_length,
        length_is_multiple_of=length_is_multiple_of,
        length_violation_action=length_violation_action,
        truncation_side=truncation_side,
        padding_side=padding_side,
        padding_value=padding_value,
        warning_stack_level=warning_stack_level + 1,
    )


def amend_mutable_binary(
    mutable_binary,
    instance_mismatch_action: Literal[
        "error",
        "warning",
    ] = None,
    value_on_cast_error: bytearray = None,
    minimum_length: int = None,
    maximum_length: int = None,
    length_is_multiple_of: Iterable[int] = None,
    length_violation_action: Literal[
        "error",
        "warning",
        "truncate-and-pad",
    ] = None,
    truncation_side: Literal[
        "left",
        "right",
        "both-but-prioritize-left",
        "both-but-prioritize-right",
    ] = None,
    padding_side: Literal[
        "left",
        "right",
        "both-but-prioritize-left",
        "both-but-prioritize-right",
    ] = None,
    padding_value: bytearray = None,
    warning_stack_level: int = None,
) -> bytearray:
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )

    return _amend_data_sequence(
        data_sequence_type=bytearray,
        data_sequence=mutable_binary,
        instance_mismatch_action=instance_mismatch_action,
        value_on_cast_error=value_on_cast_error,
        minimum_length=minimum_length,
        maximum_length=maximum_length,
        length_is_multiple_of=length_is_multiple_of,
        length_violation_action=length_violation_action,
        truncation_side=truncation_side,
        padding_side=padding_side,
        padding_value=padding_value,
        warning_stack_level=warning_stack_level + 1,
    )


def amend_text(
    text,
    instance_mismatch_action: Literal[
        "error",
        "warning",
    ] = None,
    value_on_cast_error: str = None,
    minimum_length: int = None,
    maximum_length: int = None,
    length_is_multiple_of: Iterable[int] = None,
    length_violation_action: Literal[
        "error",
        "warning",
        "truncate-and-pad",
    ] = None,
    truncation_side: Literal[
        "left",
        "right",
        "both-but-prioritize-left",
        "both-but-prioritize-right",
    ] = None,
    padding_side: Literal[
        "left",
        "right",
        "both-but-prioritize-left",
        "both-but-prioritize-right",
    ] = None,
    padding_value: str = None,
    warning_stack_level: int = None,
) -> str:
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )

    return _amend_data_sequence(
        data_sequence_type=str,
        data_sequence=text,
        instance_mismatch_action=instance_mismatch_action,
        value_on_cast_error=value_on_cast_error,
        minimum_length=minimum_length,
        maximum_length=maximum_length,
        length_is_multiple_of=length_is_multiple_of,
        length_violation_action=length_violation_action,
        truncation_side=truncation_side,
        padding_side=padding_side,
        padding_value=padding_value,
        warning_stack_level=warning_stack_level + 1,
    )
