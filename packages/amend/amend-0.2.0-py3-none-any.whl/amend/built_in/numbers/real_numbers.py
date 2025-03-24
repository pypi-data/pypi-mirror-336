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
from typing import Literal
import warnings

from amend.built_in.numbers.integers import amend_integer


def amend_real_number(
    real_number,
    instance_mismatch_action: Literal[
        "error",
        "warning",
    ] = None,
    value_on_cast_error: float = None,
    minimum_value: float = None,
    maximum_value: float = None,
    value_violation_action: Literal[
        "error",
        "warning",
        "clamp",
    ] = None,
    infinite_value_action: Literal[
        "error",
        "warning",
    ] = None,
    not_a_number_value_action: Literal[
        "error",
        "warning",
    ] = None,
    number_of_rounding_decimals: int = None,
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
            float,
        )
    ):
        raise ValueError(f"Invalid value on cast error {repr(value_on_cast_error)}")
    if not (
        minimum_value is None
        or isinstance(
            minimum_value,
            float,
        )
    ):
        raise ValueError(f"Invalid minimum value {repr(minimum_value)}")
    if not (
        maximum_value is None
        or isinstance(
            maximum_value,
            float,
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
    if infinite_value_action not in (
        None,
        "error",
        "warning",
    ):
        raise ValueError(f"Invalid infinite value action {repr(infinite_value_action)}")
    if not_a_number_value_action not in (
        None,
        "error",
        "warning",
    ):
        raise ValueError(
            f"Invalid not-a-number value action {repr(not_a_number_value_action)}"
        )
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )
    if number_of_rounding_decimals is not None:
        number_of_rounding_decimals = amend_integer(
            integer=number_of_rounding_decimals,
            instance_mismatch_action="warning",
            warning_stack_level=warning_stack_level + 1,
        )

    if not isinstance(
        real_number,
        float,
    ):
        if instance_mismatch_action is not None:
            message = f"Entity {repr(real_number)} isn't a float"
            if instance_mismatch_action == "error":
                raise TypeError(message)
            elif instance_mismatch_action == "warning":
                warnings.warn(
                    message,
                    UserWarning,
                    stacklevel=warning_stack_level,
                )
        try:
            real_number = float(real_number)
        except Exception:
            if value_on_cast_error is None:
                raise TypeError(f"Failed to cast {repr(real_number)} to float")

            real_number = value_on_cast_error

    if minimum_value is not None and real_number < minimum_value:
        message = "".join(
            (
                f"Real number {real_number} is smaller than minimum value ",
                f"{minimum_value}",
            )
        )
        if value_violation_action == "error":
            raise ValueError(message)
        elif value_violation_action == "warning":
            warnings.warn(
                message,
                UserWarning,
                stacklevel=warning_stack_level,
            )
        elif value_violation_action == "clamp":
            real_number = minimum_value

    if maximum_value is not None and real_number > maximum_value:
        message = "".join(
            (
                f"Real number {real_number} is greater than minimum value ",
                f"{maximum_value}",
            )
        )
        if value_violation_action == "error":
            raise ValueError(message)
        elif value_violation_action == "warning":
            warnings.warn(
                message,
                UserWarning,
                stacklevel=warning_stack_level,
            )
        elif value_violation_action == "clamp":
            real_number = maximum_value

    if infinite_value_action is not None and math.isinf(real_number):
        message = f"Real number {real_number} is an infinity"
        if infinite_value_action == "error":
            raise ValueError(message)
        elif infinite_value_action == "warning":
            warnings.warn(
                message,
                UserWarning,
                stacklevel=warning_stack_level,
            )

    if not_a_number_value_action is not None and math.isinf(not_a_number_value_action):
        message = f"Real number {real_number} isn't a number"
        if not_a_number_value_action == "error":
            raise ValueError(message)
        elif not_a_number_value_action == "warning":
            warnings.warn(
                message,
                UserWarning,
                stacklevel=warning_stack_level,
            )

    if number_of_rounding_decimals is not None:
        real_number = round(
            real_number,
            number_of_rounding_decimals,
        )

    return real_number
