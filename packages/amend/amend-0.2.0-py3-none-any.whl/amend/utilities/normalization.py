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

import math
from typing import (
    Any,
    Generator,
    Iterable,
    List,
    Literal,
    Tuple,
    Type,
)

from amend.built_in.numbers.integers import amend_integer
from amend.built_in.mappings.data_mappings import amend_mutable_data_mapping


def find_least_common_multiplier(
    multiples: Iterable[int] = None,
    warning_stack_level: int = None,
) -> int:
    if multiples is None:
        return 1
    try:
        multiples = iter(multiples)
    except Exception:
        raise TypeError(f"Multiples {repr(multiples)} isn't iterable")
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )

    multiples = tuple(
        amend_integer(
            multiple,
            instance_mismatch_action="warning",
            minimum_value=1,
            value_violation_action="error",
            warning_stack_level=warning_stack_level,
        )
        for multiple in multiples
    )
    if len(multiples) == 0:
        return 1

    least_common_multiplier = multiples[0]
    for element in multiples[1:]:
        least_common_multiplier = (least_common_multiplier * element) // math.gcd(
            least_common_multiplier,
            element,
        )

    return least_common_multiplier


def iterate_over_lengths_satisfying_constraints(
    length: int,
    minimum_length: int = None,
    maximum_length: int = None,
    length_is_multiple_of: Iterable[int] = None,
    warning_stack_level: int = None,
) -> Generator[
    int,
    None,
    None,
]:
    length = amend_integer(
        length,
        instance_mismatch_action="error",
        minimum_value=0,
        value_violation_action="error",
        warning_stack_level=3,
    )
    minimum_length = amend_integer(
        minimum_length,
        value_on_cast_error=0,
        minimum_value=0,
        value_violation_action="clamp",
    )
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )
    if maximum_length is not None:
        maximum_length = amend_integer(
            maximum_length,
            instance_mismatch_action="warning",
            minimum_value=0,
            value_violation_action="clamp",
            warning_stack_level=warning_stack_level + 1,
        )

    if length_is_multiple_of is None:
        differential = 1
    else:
        differential = find_least_common_multiplier(
            multiples=length_is_multiple_of,
            warning_stack_level=warning_stack_level + 1,
        )

    truncation_proposal = length - (length % differential)
    padding_proposal = length + differential - (length % differential)

    while True:
        if minimum_length <= truncation_proposal and (
            maximum_length is None or truncation_proposal <= maximum_length
        ):
            yield truncation_proposal - length
            truncation_proposal = truncation_proposal - differential

        if minimum_length <= padding_proposal and (
            maximum_length is None or padding_proposal <= maximum_length
        ):
            yield padding_proposal - length
            padding_proposal = padding_proposal + differential

        if truncation_proposal < minimum_length and (
            maximum_length is not None and padding_proposal > maximum_length
        ):
            break
    return


def determine_length_normalization_strategy(
    length: int,
    minimum_length: int = None,
    maximum_length: int = None,
    length_is_multiple_of: Iterable[int] = None,
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
    warning_stack_level: int = None,
) -> (
    Tuple[
        int,
        int,
    ]
    | None
):
    if truncation_side is not None and truncation_side not in (
        "left",
        "right",
        "both-but-prioritize-left",
        "both-but-prioritize-right",
    ):
        raise ValueError(f"Invalid truncation side {repr(truncation_side)}")
    if padding_side is not None and padding_side not in (
        "left",
        "right",
        "both-but-prioritize-left",
        "both-but-prioritize-right",
    ):
        raise ValueError(f"Invalid padding side {repr(padding_side)}")
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )

    for proposed_length_change in iterate_over_lengths_satisfying_constraints(
        length=length,
        minimum_length=minimum_length,
        maximum_length=maximum_length,
        length_is_multiple_of=length_is_multiple_of,
        warning_stack_level=warning_stack_level + 1,
    ):
        if proposed_length_change == 0:
            return (
                0,
                0,
            )

        side_to_look_at = (
            truncation_side if proposed_length_change < 0 else padding_side
        )
        if side_to_look_at is None:
            continue

        if side_to_look_at == "left":
            return (
                proposed_length_change,
                0,
            )
        elif side_to_look_at == "right":
            return (
                0,
                proposed_length_change,
            )
        elif side_to_look_at == "both-but-prioritize-left":
            return (
                (proposed_length_change + 1) // 2,
                proposed_length_change // 2,
            )

        return (
            proposed_length_change // 2,
            (proposed_length_change + 1) // 2,
        )

    return None


def _normalize_length_of_data_sequence(
    data_sequence_type: Type[bytearray] | Type[bytes] | Type[str],
    data_sequence: bytearray | bytes | str,
    proposed_length_change: Tuple[
        int,
        int,
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
    if not isinstance(
        data_sequence,
        data_sequence_type,
    ):
        raise TypeError(f"Entity {repr(data_sequence)} isn't {data_sequence_type}")
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )
    if proposed_length_change is None:
        proposed_length_change = (
            0,
            0,
        )
    elif not isinstance(
        proposed_length_change,
        tuple,
    ):
        raise TypeError(
            f"Proposed length change {repr(proposed_length_change)} isn't a tuple"
        )
    elif len(proposed_length_change) != 2:
        raise ValueError(
            f"Proposed length change has length {len(proposed_length_change)}, not 2"
        )
    else:
        proposed_length_change = tuple(
            amend_integer(
                integer=length_change,
                instance_mismatch_action="warning",
                warning_stack_level=warning_stack_level + 1,
            )
            for length_change in proposed_length_change
        )
    if padding_value is None:
        if isinstance(
            data_sequence,
            bytearray,
        ):
            padding_value = bytearray(b"\0")
        elif isinstance(
            data_sequence,
            bytes,
        ):
            padding_value = b"\0"
        else:
            padding_value = "_"
    elif not isinstance(
        padding_value,
        data_sequence_type,
    ):
        raise TypeError(
            f"Padding value {repr(padding_value)} isn't {data_sequence_type}"
        )

    (
        left_change,
        right_change,
    ) = proposed_length_change

    if left_change < 0:
        data_sequence = data_sequence[abs(left_change) :]
    elif left_change > 0:
        left_padding = (left_change + len(padding_value) - 1) // len(padding_value)
        left_padding = padding_value * left_padding
        left_padding = left_padding[:left_change]

        data_sequence = left_padding + data_sequence

    if right_change < 0:
        data_sequence = data_sequence[:right_change]
    elif right_change > 0:
        right_padding = (right_change + len(padding_value) - 1) // len(padding_value)
        right_padding = padding_value * right_padding
        right_padding = right_padding[:right_change]

        data_sequence = data_sequence + right_padding

    return data_sequence


def normalize_length_of_immutable_binary(
    immutable_binary: bytes,
    proposed_length_change: Tuple[
        int,
        int,
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

    return _normalize_length_of_data_sequence(
        data_sequence_type=bytes,
        data_sequence=immutable_binary,
        proposed_length_change=proposed_length_change,
        padding_value=padding_value,
        warning_stack_level=warning_stack_level + 1,
    )


def normalize_length_of_mutable_binary(
    mutable_binary: bytearray,
    proposed_length_change: Tuple[
        int,
        int,
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

    return _normalize_length_of_data_sequence(
        data_sequence_type=bytearray,
        data_sequence=mutable_binary,
        proposed_length_change=proposed_length_change,
        padding_value=padding_value,
        warning_stack_level=warning_stack_level + 1,
    )


def normalize_length_of_text(
    text: str,
    proposed_length_change: Tuple[
        int,
        int,
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

    return _normalize_length_of_data_sequence(
        data_sequence_type=str,
        data_sequence=text,
        proposed_length_change=proposed_length_change,
        padding_value=padding_value,
        warning_stack_level=warning_stack_level + 1,
    )


def _normalize_length_of_sequence_container(
    sequence_container: List[Any] | Tuple[Any, ...],
    proposed_length_change: Tuple[
        int,
        int,
    ] = None,
    padding_value: Tuple[Any, ...] = None,
    warning_stack_level: int = None,
) -> List[Any]:
    try:
        sequence_container = list(sequence_container)
    except Exception:
        raise TypeError(
            f"Sequence container {repr(sequence_container)} can't become a list"
        )
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )
    if proposed_length_change is None:
        proposed_length_change = (
            0,
            0,
        )
    elif not isinstance(
        proposed_length_change,
        tuple,
    ):
        raise TypeError(
            f"Proposed length change {repr(proposed_length_change)} isn't a tuple"
        )
    elif len(proposed_length_change) != 2:
        raise ValueError(
            f"Proposed length change has length {len(proposed_length_change)}, not 2"
        )
    else:
        proposed_length_change = tuple(
            amend_integer(
                integer=length_change,
                instance_mismatch_action="warning",
                warning_stack_level=warning_stack_level + 1,
            )
            for length_change in proposed_length_change
        )
    if padding_value is None:
        padding_value = [None]
    elif not isinstance(
        padding_value,
        tuple,
    ):
        raise TypeError(f"Padding value {repr(padding_value)} isn't a tuple")
    else:
        padding_value = list(padding_value)

    (
        left_change,
        right_change,
    ) = proposed_length_change

    if left_change < 0:
        sequence_container = sequence_container[abs(left_change) :]
    elif left_change > 0:
        left_padding = (left_change + len(padding_value) - 1) // len(padding_value)
        left_padding = padding_value * left_padding
        left_padding = left_padding[:left_change]

        sequence_container = left_padding + sequence_container

    if right_change < 0:
        sequence_container = sequence_container[:right_change]
    elif right_change > 0:
        right_padding = (right_change + len(padding_value) - 1) // len(padding_value)
        right_padding = padding_value * right_padding
        right_padding = right_padding[:right_change]

        sequence_container = sequence_container + right_padding

    return sequence_container


def normalize_length_of_immutable_sequence(
    immutable_sequence: Tuple[Any, ...],
    proposed_length_change: Tuple[
        int,
        int,
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
        _normalize_length_of_sequence_container(
            sequence_container=immutable_sequence,
            proposed_length_change=proposed_length_change,
            padding_value=padding_value,
            warning_stack_level=warning_stack_level + 1,
        )
    )


def normalize_length_of_mutable_sequence(
    mutable_sequence: List[Any],
    proposed_length_change: Tuple[
        int,
        int,
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
        _normalize_length_of_sequence_container(
            sequence_container=mutable_sequence,
            proposed_length_change=proposed_length_change,
            padding_value=padding_value,
            warning_stack_level=warning_stack_level + 1,
        )
    )


def get_immutable_mapping(
    mapping,
    warning_stack_level: int = None,
) -> Tuple[
    Tuple[
        Any,
        Any,
    ],
    ...,
]:
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )
    mapping = amend_mutable_data_mapping(
        mutable_data_mapping=mapping,
        warning_stack_level=3,
    )

    mapping = mapping.items()
    mapping = (tuple(pair) for pair in mapping)
    mapping = tuple(mapping)

    return mapping
