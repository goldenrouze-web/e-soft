import pandas as pd  # noqa: F401


def clean_data(df):
    df = df.drop_duplicates()
    df = df.fillna(0)
    return df


def analyze_data(df):
    stats = {}
    numeric_cols = df.select_dtypes(include=["number"]).columns

    for col in numeric_cols:
        stats[col] = {
            "mean": df[col].mean(),
            "median": df[col].median()
        }

    stats["correlation"] = df[numeric_cols].corr().to_dict()
    return stats
