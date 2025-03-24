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
    Dict,
    Literal,
    Tuple,
    Type,
)
import warnings

from amend.built_in.numbers.integers import amend_integer


def _amend_data_mapping(
    data_mapping_type: Type[dict],
    data_mapping,
    instance_mismatch_action: Literal[
        "error",
        "warning",
    ] = None,
    value_on_cast_error: Tuple[
        Tuple[Any, Any],
        ...,
    ] = None,
    minimum_length: int = None,
    maximum_length: int = None,
    length_violation_action: Literal[
        "error",
        "warning",
    ] = None,
    warning_stack_level: int = None,
) -> Dict[Any, Any]:
    if data_mapping_type not in (dict,):
        raise ValueError(f"Invalid data mapping type {repr(data_mapping_type)}")
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
                tuple,
            )
            and all(
                isinstance(
                    element,
                    tuple,
                )
                for element in value_on_cast_error
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
    if minimum_length is not None:
        minimum_length = amend_integer(
            integer=minimum_length,
            instance_mismatch_action="error",
            minimum_value=0,
            value_violation_action="error",
            warning_stack_level=warning_stack_level + 1,
        )
    if maximum_length is not None:
        maximum_length = amend_integer(
            integer=maximum_length,
            instance_mismatch_action="error",
            minimum_value=0,
            value_violation_action="error",
            warning_stack_level=warning_stack_level + 1,
        )
    if length_violation_action not in (
        None,
        "error",
        "warning",
    ):
        raise ValueError(
            f"Invalid length violation action {repr(length_violation_action)}"
        )

    if not isinstance(
        data_mapping,
        data_mapping_type,
    ):
        if instance_mismatch_action is not None:
            message = f"Entity {repr(data_mapping)} isn't a {data_mapping_type}"
            if instance_mismatch_action == "error":
                raise TypeError(message)
            elif instance_mismatch_action == "warning":
                warnings.warn(
                    message,
                    UserWarning,
                    warning_stack_level,
                )
        try:
            data_mapping = data_mapping_type(data_mapping)
        except Exception:
            if value_on_cast_error is None:
                raise TypeError(
                    f"Failed to cast {repr(data_mapping)} to {data_mapping_type}"
                )

            data_mapping = value_on_cast_error
            data_mapping = data_mapping_type(data_mapping)

    if length_violation_action is not None:
        if minimum_length is not None and len(data_mapping) < minimum_length:
            message = "".join(
                (
                    f"Data mapping has length {len(data_mapping)} smaller than ",
                    f"minimum length {minimum_length}",
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

        if maximum_length is not None and len(data_mapping) > maximum_length:
            message = "".join(
                (
                    f"Data mapping has length {len(data_mapping)} greater than ",
                    f"maximum length {maximum_length}",
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

    return data_mapping


def amend_mutable_data_mapping(
    mutable_data_mapping,
    instance_mismatch_action: Literal[
        "error",
        "warning",
    ] = None,
    value_on_cast_error: Tuple[
        Tuple[Any, Any],
        ...,
    ] = None,
    minimum_length: int = None,
    maximum_length: int = None,
    length_violation_action: Literal[
        "error",
        "warning",
    ] = None,
    warning_stack_level: int = None,
) -> Dict[Any, Any]:
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )

    return _amend_data_mapping(
        data_mapping_type=dict,
        data_mapping=mutable_data_mapping,
        instance_mismatch_action=instance_mismatch_action,
        value_on_cast_error=value_on_cast_error,
        minimum_length=minimum_length,
        maximum_length=maximum_length,
        length_violation_action=length_violation_action,
        warning_stack_level=warning_stack_level,
    )
