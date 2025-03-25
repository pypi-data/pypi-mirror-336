"""A process function for determing offensive efficiency of entities."""

import pandas as pd

from .columns import DELIMITER
from .identifier import Identifier

OFFENSIVE_EFFICIENCY_COLUMN = "offensiveefficiency"


def offensive_efficiency_process(
    df: pd.DataFrame, identifiers: list[Identifier]
) -> pd.DataFrame:
    """Process a dataframe for offensive efficiency."""

    def record_offensive_efficiency(row: pd.Series) -> pd.Series:
        nonlocal identifiers
        for identifier in identifiers:
            if identifier.field_goals_column is None:
                continue
            field_goals = float(row[identifier.field_goals_column])
            if identifier.assists_column is None:
                continue
            assists = float(row[identifier.assists_column])
            if identifier.field_goals_attempted_column is None:
                continue
            field_goals_attempted = float(row[identifier.field_goals_attempted_column])
            if identifier.offensive_rebounds_column is None:
                continue
            offensive_rebounds = float(row[identifier.offensive_rebounds_column])
            if identifier.turnovers_column is None:
                continue
            turnovers = float(row[identifier.turnovers_column])
            offensive_efficiency_column = DELIMITER.join(
                [identifier.column_prefix, OFFENSIVE_EFFICIENCY_COLUMN]
            )
            row[offensive_efficiency_column] = (float(field_goals) + float(assists)) / (
                float(field_goals_attempted)
                - float(offensive_rebounds)
                + float(assists)
                + float(turnovers)
            )
            if offensive_efficiency_column not in identifier.feature_columns:
                identifier.feature_columns.append(offensive_efficiency_column)
        return row

    return df.apply(record_offensive_efficiency, axis=1)
