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

from typing import Literal
import warnings


def amend_integer(
    integer,
    instance_mismatch_action: Literal[
        "error",
        "warning",
    ] = None,
    value_on_cast_error: int = None,
    minimum_value: int = None,
    maximum_value: int = None,
    value_violation_action: Literal[
        "error",
        "warning",
        "clamp",
    ] = None,
    warning_stack_level: int = None,
) -> int:
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
            int,
        )
    ):
        raise ValueError(f"Invalid value on cast error {repr(value_on_cast_error)}")
    if not (
        minimum_value is None
        or isinstance(
            minimum_value,
            int,
        )
    ):
        raise ValueError(f"Invalid minimum value {repr(minimum_value)}")
    if not (
        maximum_value is None
        or isinstance(
            maximum_value,
            int,
        )
    ):
        raise ValueError(f"Invalid maximum value {repr(maximum_value)}")
    if value_violation_action not in (
        None,
        "error",
        "warning",
        "clamp",
    ):
        raise ValueError(
            f"Invalid value violation action {repr(value_violation_action)}"
        )
    try:
        warning_stack_level = int(warning_stack_level)
        assert warning_stack_level > 1
    except Exception:
        warning_stack_level = 2

    if not isinstance(
        integer,
        int,
    ):
        if instance_mismatch_action is not None:
            message = f"Entity {repr(integer)} isn't an int"
            if instance_mismatch_action == "error":
                raise TypeError(message)
            elif instance_mismatch_action == "warning":
                warnings.warn(
                    message,
                    UserWarning,
                    stacklevel=warning_stack_level,
                )
        try:
            integer = int(integer)
        except Exception:
            if value_on_cast_error is None:
                raise TypeError(f"Failed to cast {repr(integer)} to int")

            integer = value_on_cast_error

    if minimum_value is not None and integer < minimum_value:
        message = f"Integer {integer} is smaller than minimum value {minimum_value}"
        if value_violation_action == "error":
            raise ValueError(message)
        elif value_violation_action == "warning":
            warnings.warn(
                message,
                UserWarning,
                stacklevel=warning_stack_level,
            )
        elif value_violation_action == "clamp":
            integer = minimum_value

    if maximum_value is not None and integer > maximum_value:
        message = f"Integer {integer} is greater than minimum value {maximum_value}"
        if value_violation_action == "error":
            raise ValueError(message)
        elif value_violation_action == "warning":
            warnings.warn(
                message,
                UserWarning,
                stacklevel=warning_stack_level,
            )
        elif value_violation_action == "clamp":
            integer = maximum_value

    return integer
