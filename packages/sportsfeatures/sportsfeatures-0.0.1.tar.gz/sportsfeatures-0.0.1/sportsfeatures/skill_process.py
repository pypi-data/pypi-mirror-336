"""Process the current dataframe by adding skill features."""

# pylint: disable=duplicate-code

import datetime
import hashlib
import os

import pandas as pd
from openskill.models import PlackettLuce, PlackettLuceRating
from pandarallel import pandarallel  # type: ignore

from .cache import sportsfeatures_cache_folder
from .columns import DELIMITER
from .entity_type import EntityType
from .identifier import Identifier

SKILL_COLUMN_PREFIX = "skill"
SKILL_MU_COLUMN = "mu"
SKILL_SIGMA_COLUMN = "sigma"
SKILL_RANKING_COLUMN = "ranking"
SKILL_PROBABILITY_COLUMN = "probability"
TIME_SLICE_ALL = "all"


def _df_hash(df: pd.DataFrame) -> str:
    # Remove all empty columns
    df = df.dropna(how="all", axis=1)
    # Determine hash by the CSV encoding of the dataframe
    csv = df.to_csv()
    return hashlib.sha256(csv.encode("utf-8")).hexdigest()


def _slice_df(
    df: pd.DataFrame,
    date: datetime.date,
    time_slice: datetime.timedelta | None,
    dt_column: str,
) -> pd.DataFrame:
    df_slice = df[df[dt_column].dt.date < date]
    if time_slice is not None:
        start_date = (
            datetime.datetime.combine(date, datetime.datetime.min.time()) - time_slice
        ).date()
        df_slice = df_slice[df_slice[dt_column].dt.date > start_date]
    return df_slice


def _create_ratings(
    df_slice: pd.DataFrame, group: pd.DataFrame, identifiers: list[Identifier]
) -> tuple[PlackettLuce, dict[str, PlackettLuceRating]]:
    rating_model = PlackettLuce()
    ratings = {}
    for identifier in identifiers:
        for df in [df_slice, group]:
            if identifier.column not in df.columns.values:
                continue
            for team_id in df[identifier.column].unique():
                if not isinstance(team_id, str):
                    continue
                ratings[team_id] = rating_model.rating(name=team_id)
    return rating_model, ratings


def _find_matches(
    row: pd.Series,
    teams: dict[str, PlackettLuceRating],
    players: dict[str, PlackettLuceRating],
    team_identifiers: list[Identifier],
    player_identifiers: list[Identifier],
) -> tuple[list[float], list[list[PlackettLuceRating]], list[list[PlackettLuceRating]]]:
    points = []
    team_match = []
    player_match = []
    for team_identifier in team_identifiers:
        if team_identifier.points_column is None:
            continue
        if (
            team_identifier.points_column not in row
            or team_identifier.column not in row
        ):
            continue
        point = row[team_identifier.points_column]
        if pd.isnull(point):
            continue
        points.append(float(point))
        team_match.append([teams[row[team_identifier.column]]])
        player_team = []
        for player_identifier in player_identifiers:
            if player_identifier.team_identifier_column is None:
                continue
            if (
                player_identifier.team_identifier_column not in row
                or player_identifier.column not in row
            ):
                continue
            player_team_identifier = row[player_identifier.team_identifier_column]
            if pd.isnull(player_team_identifier):
                continue
            if player_team_identifier != team_identifier:
                continue
            player_team.append(players[row[player_identifier.column]])
        player_match.append(player_team)
    return points, team_match, player_match


def _rate_match(
    model: PlackettLuce,
    match: list[list[PlackettLuceRating]],
    points: list[float],
    ratings: dict[str, PlackettLuceRating],
) -> dict[str, PlackettLuceRating]:
    if not match:
        return ratings
    for team in match:
        if not team:
            return ratings
    output = model.rate(match, scores=points)
    for team in output:
        for player in team:
            name = player.name
            if name is None:
                continue
            ratings[name] = player
    return ratings


def _simulate_games(
    df_slice: pd.DataFrame,
    model_team: tuple[PlackettLuce, dict[str, PlackettLuceRating]],
    model_players: tuple[PlackettLuce, dict[str, PlackettLuceRating]],
    team_identifiers: list[Identifier],
    player_identifiers: list[Identifier],
) -> tuple[
    tuple[PlackettLuce, dict[str, PlackettLuceRating]],
    tuple[PlackettLuce, dict[str, PlackettLuceRating]],
]:
    team_model, teams = model_team
    player_model, players = model_players

    def _simulate_match(row: pd.Series) -> pd.Series:
        nonlocal team_identifiers
        nonlocal player_identifiers
        nonlocal teams
        nonlocal players
        nonlocal team_model
        nonlocal player_model
        points, team_match, player_match = _find_matches(
            row, teams, players, team_identifiers, player_identifiers
        )
        teams = _rate_match(team_model, team_match, points, teams)
        players = _rate_match(player_model, player_match, points, players)
        return row

    df_slice.apply(_simulate_match, axis=1)

    return (team_model, teams), (player_model, players)


def _find_team_team(
    team_identifier: Identifier,
    row: pd.Series,
    year_col: str,
    teams: dict[str, PlackettLuceRating],
) -> tuple[list[PlackettLuceRating], pd.Series]:
    if team_identifier.column not in row:
        return [], row
    team_id = row[team_identifier.column]
    if pd.isnull(team_id):
        return [], row
    team_skill_col_prefix = DELIMITER.join(
        [team_identifier.column_prefix, SKILL_COLUMN_PREFIX, year_col]
    )
    team_mu_col = DELIMITER.join([team_skill_col_prefix, SKILL_MU_COLUMN])
    team_sigma_col = DELIMITER.join([team_skill_col_prefix, SKILL_SIGMA_COLUMN])
    team = teams[team_id]
    row[team_mu_col] = team.mu
    row[team_sigma_col] = team.sigma
    return [team], row


def _find_player_team(
    identifiers: list[Identifier],
    players: dict[str, PlackettLuceRating],
    row: pd.Series,
    team_identifier: Identifier,
) -> list[PlackettLuceRating]:
    player_team: list[PlackettLuceRating] = []
    if team_identifier.column not in row:
        return player_team
    team_id = row[team_identifier.column]
    if pd.isnull(team_id):
        return player_team

    for identifier in identifiers:
        if identifier.team_identifier_column is None:
            continue
        if identifier.column not in row:
            continue
        player_id = row[identifier.column]
        if pd.isnull(player_id):
            continue
        if identifier.team_identifier_column not in row:
            continue
        player_team_id = row[identifier.team_identifier_column]
        if pd.isnull(player_team_id):
            continue
        if player_team_id != team_id:
            continue
        player = players[player_id]
        player_team.append(player)

    return player_team


def _find_row_matches(
    row: pd.Series,
    identifiers: tuple[list[Identifier], list[Identifier]],
    time_col: str,
    teams: dict[str, PlackettLuceRating],
    players: dict[str, PlackettLuceRating],
) -> tuple[pd.Series, list[list[PlackettLuceRating]], list[list[PlackettLuceRating]]]:
    team_identifiers, player_identifiers = identifiers
    team_match = []
    player_match = []
    for team_identifier in team_identifiers:
        team, row = _find_team_team(team_identifier, row, time_col, teams)
        if not team:
            continue
        team_match.append(team)
        player_team = _find_player_team(
            player_identifiers, players, row, team_identifier
        )
        player_match.append(player_team)
    return row, team_match, player_match


def _rank_predictions(
    match: list[list[PlackettLuceRating]],
    row: pd.Series,
    model: PlackettLuce,
    year_col: str,
    identifiers: list[Identifier],
) -> pd.Series:
    if not match:
        return row
    for team in match:
        if not team:
            return row
    rank_team_predictions = model.predict_rank(match)
    for i, (rank, prob) in enumerate(rank_team_predictions):
        for rating in match[i]:
            for identifier in identifiers:
                if identifier.column not in row:
                    continue
                identifier_id = row[identifier.column]
                if pd.isnull(identifier_id):
                    continue
                if identifier_id != rating.name:
                    continue
                team_ranking_col = DELIMITER.join(
                    [identifier.column_prefix, SKILL_RANKING_COLUMN, year_col]
                )
                team_prob_col = DELIMITER.join(
                    [identifier.column_prefix, SKILL_PROBABILITY_COLUMN, year_col]
                )
                row[team_ranking_col] = rank
                row[team_prob_col] = prob
                break
    return row


def _create_feature_cols(
    group: pd.DataFrame,
    time_slice: datetime.timedelta | None,
    identifiers: tuple[list[Identifier], list[Identifier]],
    model_team: tuple[PlackettLuce, dict[str, PlackettLuceRating]],
    model_players: tuple[PlackettLuce, dict[str, PlackettLuceRating]],
) -> pd.DataFrame:
    time_col = str(time_slice.days) if time_slice is not None else TIME_SLICE_ALL
    team_model, teams = model_team
    player_model, players = model_players
    team_identifiers, player_identifiers = identifiers

    def _apply_group_skills_features(row: pd.Series) -> pd.Series:
        row, team_match, player_match = _find_row_matches(
            row, (team_identifiers, player_identifiers), time_col, teams, players
        )
        row = _rank_predictions(team_match, row, team_model, time_col, team_identifiers)
        row = _rank_predictions(
            player_match, row, player_model, time_col, player_identifiers
        )
        return row

    return group.apply(_apply_group_skills_features, axis=1)


def skill_process(
    df: pd.DataFrame,
    dt_column: str,
    identifiers: list[Identifier],
    windows: list[datetime.timedelta | None],
) -> pd.DataFrame:
    """Add skill features to the dataframe."""
    pandarallel.initialize(progress_bar=True)
    team_identifiers = [x for x in identifiers if x.entity_type == EntityType.TEAM]
    player_identifiers = [x for x in identifiers if x.entity_type == EntityType.PLAYER]

    def calculate_skills(group: pd.DataFrame) -> pd.DataFrame:
        nonlocal df
        nonlocal team_identifiers
        nonlocal player_identifiers

        df_hash = _df_hash(group)
        df_cache_file = os.path.join(
            sportsfeatures_cache_folder(), f"{df_hash}.parquet.gzip"
        )
        if os.path.exists(df_cache_file):
            return pd.read_parquet(df_cache_file)

        dates = group[dt_column].dt.date.values.tolist()
        if not dates:
            return group
        date = dates[0]
        for time_slice in windows:
            df_slice = _slice_df(df, date, time_slice, dt_column)
            if df_slice.empty:
                continue
            team_model, teams = _create_ratings(df_slice, group, team_identifiers)
            player_model, players = _create_ratings(df_slice, group, player_identifiers)
            (team_model, teams), (player_model, players) = _simulate_games(
                df_slice,
                (team_model, teams),
                (player_model, players),
                team_identifiers,
                player_identifiers,
            )
            group = _create_feature_cols(
                group,
                time_slice,
                (team_identifiers, player_identifiers),
                (team_model, teams),
                (player_model, players),
            )

        group.to_parquet(df_cache_file, compression="gzip")

        return group

    attrs = df.attrs
    df = (
        df.groupby(  # type: ignore
            [df[dt_column].dt.date]
        )
        .parallel_apply(calculate_skills)
        .reset_index(drop=True)
    )
    df.attrs = attrs
    return df
