"""The main process function."""

import datetime

import pandas as pd

from .datetime_process import datetime_process
from .datetimesub_process import datetimesub_process
from .identifier import Identifier
from .offensive_efficiency_process import offensive_efficiency_process
from .remove_process import remove_process
from .skill_process import skill_process
from .timeseries_process import timeseries_process


def process(
    df: pd.DataFrame,
    dt_column: str,
    identifiers: list[Identifier],
    windows: list[datetime.timedelta | None],
) -> pd.DataFrame:
    """Process the dataframe for sports features."""
    df = skill_process(df, dt_column, identifiers, windows)
    df = offensive_efficiency_process(df, identifiers)
    df = datetimesub_process(df, dt_column)
    df = timeseries_process(df, identifiers, windows, dt_column)
    df = datetime_process(df)
    df = remove_process(df, identifiers)
    return df
