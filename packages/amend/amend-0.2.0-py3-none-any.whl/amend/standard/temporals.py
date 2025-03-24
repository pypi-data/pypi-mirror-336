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

import datetime
from typing import (
    Literal,
    Type,
)
import warnings

from amend.built_in.numbers.integers import amend_integer


def _amend_temporal_value(
    temporal_value_type: (
        Type[datetime.date]
        | Type[datetime.datetime]
        | Type[datetime.time]
        | Type[datetime.timedelta]
    ),
    temporal_value,
    instance_mismatch_action: Literal[
        "error",
        "warning",
    ] = None,
    value_on_cast_error: (
        datetime.date | datetime.datetime | datetime.time | datetime.timedelta
    ) = None,
    minimum_value: (
        datetime.date | datetime.datetime | datetime.time | datetime.timedelta
    ) = None,
    maximum_value: (
        datetime.date | datetime.datetime | datetime.time | datetime.timedelta
    ) = None,
    value_violation_action: Literal[
        "error",
        "warning",
        "clamp",
    ] = None,
    warning_stack_level: int = None,
) -> datetime.date | datetime.datetime | datetime.time | datetime.timedelta:
    if temporal_value_type not in (
        datetime.date,
        datetime.datetime,
        datetime.time,
        datetime.timedelta,
    ):
        raise ValueError(f"Invalid temporal value type {repr(temporal_value_type)}")
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
            temporal_value_type,
        )
    ):
        raise ValueError(f"Invalid value on cast error {repr(value_on_cast_error)}")
    if not (
        minimum_value is None
        or isinstance(
            minimum_value,
            temporal_value_type,
        )
    ):
        raise ValueError(f"Invalid minimum value {repr(minimum_value)}")
    if not (
        maximum_value is None
        or isinstance(
            maximum_value,
            temporal_value_type,
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
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )

    if not isinstance(
        temporal_value,
        temporal_value_type,
    ):
        if instance_mismatch_action is not None:
            message = f"Entity {repr(temporal_value)} isn't a {temporal_value_type}"
            if instance_mismatch_action == "error":
                raise TypeError(message)
            elif instance_mismatch_action == "warning":
                warnings.warn(
                    message,
                    UserWarning,
                    stacklevel=warning_stack_level,
                )
        try:
            temporal_value = vars(temporal_value)
            temporal_value = temporal_value_type(**temporal_value)
        except Exception:
            if value_on_cast_error is None:
                raise TypeError(
                    f"Failed to cast {repr(temporal_value)} to {temporal_value_type}"
                )

            temporal_value = value_on_cast_error

    if minimum_value is not None and temporal_value < minimum_value:
        message = f"Temporal value {temporal_value} is lesser than {minimum_value}"
        if value_violation_action == "error":
            raise ValueError(message)
        elif value_violation_action == "warning":
            warnings.warn(
                message,
                UserWarning,
                warning_stack_level,
            )
        elif value_violation_action == "clamp":
            temporal_value = minimum_value

    if maximum_value is not None and temporal_value > maximum_value:
        message = f"Temporal value {temporal_value} is greater than {maximum_value}"
        if value_violation_action == "error":
            raise ValueError(message)
        elif value_violation_action == "warning":
            warnings.warn(
                message,
                UserWarning,
                warning_stack_level,
            )
        elif value_violation_action == "clamp":
            temporal_value = maximum_value

    return temporal_value


def amend_date(
    date,
    instance_mismatch_action: Literal[
        "error",
        "warning",
    ] = None,
    value_on_cast_error: datetime.date = None,
    minimum_value: datetime.date = None,
    maximum_value: datetime.date = None,
    value_violation_action: Literal[
        "error",
        "warning",
        "clamp",
    ] = None,
    warning_stack_level: int = None,
) -> datetime.date:
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )

    return _amend_temporal_value(
        temporal_value_type=datetime.date,
        temporal_value=date,
        instance_mismatch_action=instance_mismatch_action,
        value_on_cast_error=value_on_cast_error,
        minimum_value=minimum_value,
        maximum_value=maximum_value,
        value_violation_action=value_violation_action,
        warning_stack_level=warning_stack_level + 1,
    )


def amend_date_and_time(
    date_and_time,
    instance_mismatch_action: Literal[
        "error",
        "warning",
    ] = None,
    value_on_cast_error: datetime.date = None,
    minimum_value: datetime.date = None,
    maximum_value: datetime.date = None,
    value_violation_action: Literal[
        "error",
        "warning",
        "clamp",
    ] = None,
    warning_stack_level: int = None,
) -> datetime.datetime:
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )

    return _amend_temporal_value(
        temporal_value_type=datetime.datetime,
        temporal_value=date_and_time,
        instance_mismatch_action=instance_mismatch_action,
        value_on_cast_error=value_on_cast_error,
        minimum_value=minimum_value,
        maximum_value=maximum_value,
        value_violation_action=value_violation_action,
        warning_stack_level=warning_stack_level + 1,
    )


def amend_time(
    time,
    instance_mismatch_action: Literal[
        "error",
        "warning",
    ] = None,
    value_on_cast_error: datetime.date = None,
    minimum_value: datetime.date = None,
    maximum_value: datetime.date = None,
    value_violation_action: Literal[
        "error",
        "warning",
        "clamp",
    ] = None,
    warning_stack_level: int = None,
) -> datetime.time:
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )

    return _amend_temporal_value(
        temporal_value_type=datetime.time,
        temporal_value=time,
        instance_mismatch_action=instance_mismatch_action,
        value_on_cast_error=value_on_cast_error,
        minimum_value=minimum_value,
        maximum_value=maximum_value,
        value_violation_action=value_violation_action,
        warning_stack_level=warning_stack_level + 1,
    )


def amend_temporal_offset(
    temporal_offset,
    instance_mismatch_action: Literal[
        "error",
        "warning",
    ] = None,
    value_on_cast_error: datetime.timedelta = None,
    minimum_value: datetime.timedelta = None,
    maximum_value: datetime.timedelta = None,
    value_violation_action: Literal[
        "error",
        "warning",
        "clamp",
    ] = None,
    warning_stack_level: int = None,
) -> datetime.timedelta:
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )

    return _amend_temporal_value(
        temporal_value_type=datetime.timedelta,
        temporal_value=temporal_offset,
        instance_mismatch_action=instance_mismatch_action,
        value_on_cast_error=value_on_cast_error,
        minimum_value=minimum_value,
        maximum_value=maximum_value,
        value_violation_action=value_violation_action,
        warning_stack_level=warning_stack_level + 1,
    )
