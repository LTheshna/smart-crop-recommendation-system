"""Data cleaning utilities for smart crop recommendation preprocessing."""

from __future__ import annotations

import pandas as pd


def _fill_numeric_missing(df: pd.DataFrame) -> pd.DataFrame:
    """Fill missing numeric values using median per column."""
    numeric_columns = df.select_dtypes(include=["number"]).columns

    for column in numeric_columns:
        median_value = df[column].median(skipna=True)
        if pd.notna(median_value):
            df[column] = df[column].fillna(median_value)

    return df


def _fill_categorical_missing(df: pd.DataFrame) -> pd.DataFrame:
    """Fill missing categorical values using mode per column."""
    categorical_columns = df.select_dtypes(include=["object", "category"]).columns

    for column in categorical_columns:
        mode_series = df[column].mode(dropna=True)
        if not mode_series.empty:
            df[column] = df[column].fillna(mode_series.iloc[0])

    return df


def _find_first_existing_column(df: pd.DataFrame, candidates: list[str]) -> str | None:
    """Return the first candidate column name that exists in the DataFrame."""
    for candidate in candidates:
        if candidate in df.columns:
            return candidate
    return None


def _validate_column_range(df: pd.DataFrame, column: str, min_value: float, max_value: float) -> None:
    """Validate that values in a column fall within a bounded range."""
    if column not in df.columns:
        return

    invalid_mask = df[column].notna() & ~df[column].between(min_value, max_value)
    if invalid_mask.any():
        invalid_values = df.loc[invalid_mask, column].unique()
        raise ValueError(
            f"Column '{column}' contains values outside the range [{min_value}, {max_value}]: "
            f"{invalid_values.tolist()}"
        )


def load_and_clean_csv(file_path: str) -> pd.DataFrame:
    """Load a CSV file and return a cleaned pandas DataFrame.

    Cleaning steps:
    - load CSV from the provided file path
    - drop duplicate rows
    - fill missing numeric values with the column median
    - fill missing categorical values with the column mode
    - validate pH and humidity ranges when those columns exist

    Args:
        file_path: Path to the CSV file to load.

    Returns:
        Cleaned pandas DataFrame.

    Raises:
        ValueError: If the file cannot be parsed or validation fails.
    """
    try:
        df = pd.read_csv(file_path)
    except (FileNotFoundError, pd.errors.EmptyDataError, pd.errors.ParserError) as exc:
        raise ValueError(f"Unable to load CSV file '{file_path}': {exc}") from exc

    df = df.drop_duplicates().reset_index(drop=True)
    df = _fill_numeric_missing(df)
    df = _fill_categorical_missing(df)

    pH_column = _find_first_existing_column(df, ["pH", "ph"])
    if pH_column:
        _validate_column_range(df, pH_column, 0.0, 14.0)

    _validate_column_range(df, "humidity", 0.0, 100.0)

    return df
