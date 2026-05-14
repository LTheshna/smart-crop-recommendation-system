"""Train a crop prediction model from processed crop dataset."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.metrics import accuracy_score
import joblib

df = pd.read_csv("data/processed/adapted_crop_dataset.csv")
ARTIFACTS_DIR = Path("ml/artifacts")
MODEL_PATH = ARTIFACTS_DIR / "crop_model.pkl"
LABEL_ENCODER_PATH = ARTIFACTS_DIR / "label_encoder.pkl"
FEATURE_COLUMNS_PATH = ARTIFACTS_DIR / "feature_columns.pkl"
PROCESSED_DATA_PATH = "data/processed/adapted_crop_dataset.csv"


def _load_dataset(path: Path) -> pd.DataFrame:
    """Load the processed crop dataset from disk."""
    print(f"Loading processed dataset from {path}")
    try:
        return pd.read_csv(path)
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"Processed dataset not found at '{path}'. Run preprocessing before training."
        ) from exc

def _select_feature_columns(df: pd.DataFrame, target_column: str) -> pd.DataFrame:
    """
    Return only core agronomic feature columns for model training.
    """

    model_features = [
        "N",
        "P",
        "K",
        "temperature",
        "humidity",
        "ph",
        "rainfall"
    ]

    feature_df = df[model_features].copy()

    return feature_df

    # Remove obvious non-feature columns: constant values or likely identifiers.
    for col in feature_columns:
        if feature_df[col].nunique(dropna=False) <= 1:
            print(f"Dropping constant column: {col}")
            feature_df.drop(columns=[col], inplace=True)
            continue

        if feature_df[col].dtype == object and feature_df[col].nunique(dropna=False) == len(feature_df):
            print(f"Dropping likely identifier column: {col}")
            feature_df.drop(columns=[col], inplace=True)

    return feature_df


def _get_categorical_columns(df: pd.DataFrame) -> list[str]:
    """Return the categorical columns that should be one-hot encoded."""
    return df.select_dtypes(include=["object", "category"]).columns.tolist()


def _build_preprocessor(df: pd.DataFrame) -> ColumnTransformer:
    """Build a preprocessing transformer for categorical feature encoding."""
    categorical_columns = _get_categorical_columns(df)
    if categorical_columns:
        print(f"Preparing one-hot encoding for columns: {categorical_columns}")
        transformers = [
            (
                "cat",
               OneHotEncoder(sparse_output=False, handle_unknown="ignore"),
                categorical_columns,
            )
        ]
    else:
        print("No categorical columns found for one-hot encoding")
        transformers = []

    return ColumnTransformer(transformers, remainder="passthrough")


def _prepare_target(df: pd.DataFrame, target_column: str) -> tuple[pd.Series, LabelEncoder]:
    """Prepare the target variable and return encoded labels with its encoder."""
    if target_column not in df.columns:
        raise ValueError(f"Target column '{target_column}' is missing from the dataset.")

    print(f"Encoding target column: {target_column}")
    encoder = LabelEncoder()
    target = encoder.fit_transform(df[target_column].astype(str))
    return pd.Series(target, name=target_column), encoder


def _build_pipeline(preprocessor: ColumnTransformer) -> Pipeline:
    """Build a training pipeline that combines preprocessing and classification."""
    return Pipeline(
        [
            ("preprocessor", preprocessor),
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=200,
                    max_depth=12,
                    random_state=42,
                ),
            ),
        ]
    )


def _save_artifacts(
    model: Pipeline,
    label_encoder: LabelEncoder,
    feature_columns: list[str],
) -> None:
    """Save the trained pipeline, target label encoder, and feature columns."""
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Saving model pipeline to {MODEL_PATH}")
    joblib.dump(model, MODEL_PATH)
    print(f"Saving label encoder to {LABEL_ENCODER_PATH}")
    joblib.dump(label_encoder, LABEL_ENCODER_PATH)
    print(f"Saving feature columns to {FEATURE_COLUMNS_PATH}")
    joblib.dump(feature_columns, FEATURE_COLUMNS_PATH)


def train_crop_model() -> None:
    """Load data, train a RandomForestClassifier pipeline, and save model artifacts."""
    df = _load_dataset(PROCESSED_DATA_PATH)
    target_column = "crop"

    feature_df = _select_feature_columns(df, target_column)
    target, label_encoder = _prepare_target(df, target_column)

    preprocessor = _build_preprocessor(feature_df)
    pipeline = _build_pipeline(preprocessor)

    print("Splitting dataset into training and test sets")
    X_train, X_test, y_train, y_test = train_test_split(
        feature_df, target, test_size=0.2, random_state=42, stratify=target
    )

    print("Training RandomForestClassifier pipeline")
    pipeline.fit(X_train, y_train)

    train_accuracy = accuracy_score(y_train, pipeline.predict(X_train))
    test_accuracy = accuracy_score(y_test, pipeline.predict(X_test))
    print(f"Training accuracy: {train_accuracy:.4f}")
    print(f"Test accuracy: {test_accuracy:.4f}")

    _save_artifacts(pipeline, label_encoder, feature_df.columns.tolist())


if __name__ == "__main__":
    train_crop_model()
