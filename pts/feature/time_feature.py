from abc import ABC, abstractmethod
from typing import List

import numpy as np
import pandas as pd

from .utils import get_granularity

class TimeFeature(ABC):
    def __init__(self, normalized: bool = True):
        self.normalized = normalized

    @abstractmethod
    def __call__(self, index: pd.DatetimeIndex) -> np.ndarray:
        pass


class MinuteOfHour(TimeFeature):
    """
    Minute of hour encoded as value between [-0.5, 0.5]
    """
    def __call__(self, index: pd.DatetimeIndex) -> np.ndarray:
        if self.normalized:
            return index.minute / 59.0 - 0.5
        else:
            return index.minute.map(float)


class HourOfDay(TimeFeature):
    """
    Hour of day encoded as value between [-0.5, 0.5]
    """
    def __call__(self, index: pd.DatetimeIndex) -> np.ndarray:
        if self.normalized:
            return index.hour / 23.0 - 0.5
        else:
            return index.hour.map(float)


class DayOfWeek(TimeFeature):
    """
    Hour of day encoded as value between [-0.5, 0.5]
    """
    def __call__(self, index: pd.DatetimeIndex) -> np.ndarray:
        if self.normalized:
            return index.dayofweek / 6.0 - 0.5
        else:
            return index.dayofweek.map(float)


class DayOfMonth(TimeFeature):
    """
    Day of month encoded as value between [-0.5, 0.5]
    """
    def __call__(self, index: pd.DatetimeIndex) -> np.ndarray:
        if self.normalized:
            return index.day / 30.0 - 0.5
        else:
            return index.day.map(float)


class DayOfYear(TimeFeature):
    """
    Day of year encoded as value between [-0.5, 0.5]
    """
    def __call__(self, index: pd.DatetimeIndex) -> np.ndarray:
        if self.normalized:
            return index.dayofyear / 364.0 - 0.5
        else:
            return index.dayofyear.map(float)


class MonthOfYear(TimeFeature):
    """
    Month of year encoded as value between [-0.5, 0.5]
    """
    def __call__(self, index: pd.DatetimeIndex) -> np.ndarray:
        if self.normalized:
            return index.month / 11.0 - 0.5
        else:
            return index.month.map(float)


class WeekOfYear(TimeFeature):
    """
    Week of year encoded as value between [-0.5, 0.5]
    """
    def __call__(self, index: pd.DatetimeIndex) -> np.ndarray:
        if self.normalized:
            return index.weekofyear / 51.0 - 0.5
        else:
            return index.weekofyear.map(float)


def time_features_from_frequency_str(freq_str: str) -> List[TimeFeature]:
    """
    Returns a list of time features that will be appropriate for the given frequency string.

    Parameters
    ----------

    freq_str
        Frequency string of the form [multiple][granularity] such as "12H", "5min", "1D" etc.

    """
    _, granularity = get_granularity(freq_str)
    if granularity == "M":
        feature_classes = [MonthOfYear]
    elif granularity == "W":
        feature_classes = [DayOfMonth, WeekOfYear]
    elif granularity in ["D", "B"]:
        feature_classes = [DayOfWeek, DayOfMonth, DayOfYear]
    elif granularity == "H":
        feature_classes = [HourOfDay, DayOfWeek, DayOfMonth, DayOfYear]
    elif granularity in ["min", "T"]:
        feature_classes = [
            MinuteOfHour, HourOfDay, DayOfWeek, DayOfMonth, DayOfYear
        ]
    else:
        supported_freq_msg = f"""
        Unsupported frequency {freq_str}

        The following frequencies are supported:

            M   - monthly
            W   - week
            D   - daily
            H   - hourly
            min - minutely
        """
        raise RuntimeError(supported_freq_msg)

    return [cls() for cls in feature_classes]