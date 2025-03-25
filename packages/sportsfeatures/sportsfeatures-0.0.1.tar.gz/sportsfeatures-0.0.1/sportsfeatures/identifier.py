"""A description of player representation in the dataframe."""

from .entity_type import EntityType


class Identifier:
    """A way to identify an entity."""

    # pylint: disable=too-many-arguments,too-many-positional-arguments,too-few-public-methods,too-many-instance-attributes

    def __init__(
        self,
        entity_type: EntityType,
        column: str,
        feature_columns: list[str],
        column_prefix: str,
        points_column: str | None = None,
        team_identifier_column: str | None = None,
        field_goals_column: str | None = None,
        assists_column: str | None = None,
        field_goals_attempted_column: str | None = None,
        offensive_rebounds_column: str | None = None,
        turnovers_column: str | None = None,
    ):
        self.entity_type = entity_type
        self.column = column
        self.feature_columns = feature_columns
        self.column_prefix = column_prefix
        self.points_column = points_column
        self.team_identifier_column = team_identifier_column
        self.field_goals_column = field_goals_column
        self.assists_column = assists_column
        self.field_goals_attempted_column = field_goals_attempted_column
        self.offensive_rebounds_column = offensive_rebounds_column
        self.turnovers_column = turnovers_column
