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
    Any,
    Iterable,
    List,
    Literal,
    Tuple,
    Type,
)
import warnings

from amend.built_in.numbers.integers import amend_integer
from amend.utilities.normalization import (
    _normalize_length_of_sequence_container,
    determine_length_normalization_strategy,
)


def _amend_sequence_container(
    sequence_container_type: Type[list] | Type[tuple],
    sequence_container,
    instance_mismatch_action: Literal[
        "error",
        "warning",
    ] = None,
    value_on_cast_error: Tuple[Any, ...] = None,
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
    padding_value: Tuple[Any, ...] = None,
    warning_stack_level: int = None,
) -> List[Any] | Tuple[Any, ...]:
    if sequence_container_type not in (
        list,
        tuple,
    ):
        raise ValueError(
            f"Invalid sequence container type {repr(sequence_container_type)}"
        )
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
        or isinstance(
            value_on_cast_error,
            tuple,
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
    if (
        not isinstance(
            sequence_container,
            sequence_container_type,
        )
        and instance_mismatch_action is not None
    ):
        message = f"Entity {repr(sequence_container)} isn't {sequence_container_type}"
        if instance_mismatch_action == "error":
            raise TypeError(message)
        elif instance_mismatch_action == "warning":
            warnings.warn(
                message,
                UserWarning,
                warning_stack_level,
            )

    try:
        sequence_container = sequence_container_type(sequence_container)
    except Exception:
        if value_on_cast_error is None:
            raise TypeError(
                "".join(
                    (
                        f"Failed to cast {repr(sequence_container)} to ",
                        f"{sequence_container_type}",
                    )
                )
            )

        sequence_container = value_on_cast_error
        sequence_container = sequence_container_type(sequence_container)

    proposed_length_changes = determine_length_normalization_strategy(
        length=len(sequence_container),
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
        message = "".join(
            (
                f"Entity {repr(sequence_container)} has incorrect length ",
                f"{len(sequence_container)}",
            )
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
                            f"{repr(sequence_container)}",
                        )
                    )
                )

        sequence_container = _normalize_length_of_sequence_container(
            sequence_container=sequence_container,
            proposed_length_change=proposed_length_changes,
            padding_value=padding_value,
            warning_stack_level=warning_stack_level + 1,
        )

    return sequence_container


def amend_immutable_sequence(
    immutable_sequence,
    instance_mismatch_action: Literal[
        "error",
        "warning",
    ] = None,
    value_on_cast_error: Tuple[Any, ...] = None,
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
    padding_value: Tuple[Any, ...] = None,
    warning_stack_level: int = None,
) -> Tuple[Any, ...]:
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )

    return tuple(
        _amend_sequence_container(
            sequence_container_type=tuple,
            sequence_container=immutable_sequence,
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
    )


def amend_mutable_sequence(
    mutable_sequence,
    instance_mismatch_action: Literal[
        "error",
        "warning",
    ] = None,
    value_on_cast_error: Tuple[Any, ...] = None,
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
    padding_value: Tuple[Any, ...] = None,
    warning_stack_level: int = None,
) -> List[Any]:
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )

    return list(
        _amend_sequence_container(
            sequence_container_type=tuple,
            sequence_container=mutable_sequence,
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
    )
