"""The process for removing lookahead features."""

import pandas as pd

from .identifier import Identifier


def remove_process(df: pd.DataFrame, identifiers: list[Identifier]) -> pd.DataFrame:
    """Remove the features from the dataframe."""
    drop_columns: set[str] = set()
    for identifier in identifiers:
        for feature_col in identifier.feature_columns:
            drop_columns.add(feature_col)
    return df.drop(columns=list(drop_columns))
