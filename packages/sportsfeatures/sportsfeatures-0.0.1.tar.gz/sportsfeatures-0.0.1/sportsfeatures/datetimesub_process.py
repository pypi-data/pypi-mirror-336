"""A processor for subbing any datetimes with the dt column."""

import pandas as pd
from feature_engine.datetime import DatetimeSubtraction


def datetimesub_process(df: pd.DataFrame, dt_column: str) -> pd.DataFrame:
    """Process date time subtractions."""
    columns = (
        df.drop(columns=[dt_column])
        .select_dtypes(include=["datetime64"])
        .columns.values
    )
    if columns:
        dts = DatetimeSubtraction(variables=columns, reference=[dt_column])  # type: ignore
        df = dts.fit_transform(df)
    return df
