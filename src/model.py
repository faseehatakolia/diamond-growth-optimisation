
from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures


# ============================================================
# DATASET LOCATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "mpcvd_experimental_data_v01.csv"

REQUIRED_COLUMNS = [
    "observation_id",
    "temperature_c",
    "methane_pct",
    "growth_rate_um_h",
    "series_id",
]


# ============================================================
# DATA LOADING AND VALIDATION
# ============================================================

def load_data():
    """Load and validate the selected MPCVD experimental data."""

    data = pd.read_csv(DATA_PATH)

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Dataset is missing required columns: {missing_columns}"
        )

    if data.empty:
        raise ValueError("The experimental dataset is empty.")

    if data[REQUIRED_COLUMNS].isnull().any().any():
        raise ValueError("The dataset contains missing values.")

    numeric_columns = [
        "temperature_c",
        "methane_pct",
        "growth_rate_um_h",
    ]

    for column in numeric_columns:
        data[column] = pd.to_numeric(
            data[column],
            errors="raise",
        )

    if not np.isfinite(data[numeric_columns].to_numpy()).all():
        raise ValueError("The dataset contains non-finite values.")

    if not data["methane_pct"].between(0, 100).all():
        raise ValueError(
            "Methane concentration must be between 0 and 100%."
        )

    if (data["growth_rate_um_h"] < 0).any():
        raise ValueError(
            "Experimental growth rates cannot be negative."
        )

    if data["observation_id"].duplicated().any():
        raise ValueError("Duplicate observation IDs found.")

    return data


# ============================================================
# MULTIPLE LINEAR REGRESSION
# ============================================================

def train_model(data):
    """Fit a multiple linear regression model."""

    X = data[["methane_pct", "temperature_c"]]
    y = data["growth_rate_um_h"]

    model = LinearRegression()
    model.fit(X, y)

    return model


def predict_growth(model, methane_pct, temperature_c):
    """Return an illustrative linear-regression prediction."""

    if not np.isfinite(methane_pct):
        raise ValueError("Methane concentration must be finite.")

    if not np.isfinite(temperature_c):
        raise ValueError("Substrate temperature must be finite.")

    if not 0 <= methane_pct <= 100:
        raise ValueError(
            "Methane concentration must be between 0 and 100%."
        )

    if temperature_c <= 0:
        raise ValueError(
            "Substrate temperature must be positive."
        )

    inputs = pd.DataFrame({
        "methane_pct": [methane_pct],
        "temperature_c": [temperature_c],
    })

    prediction = float(model.predict(inputs)[0])

    if not np.isfinite(prediction):
        raise ValueError("Model returned a non-finite prediction.")

    return prediction


# ============================================================
# DIAMOND THICKNESS
# ============================================================

def calculate_thickness(growth_rate, time_hours):
    """Estimate thickness assuming a constant growth rate."""

    if not np.isfinite(growth_rate):
        raise ValueError("Growth rate must be finite.")

    if not np.isfinite(time_hours):
        raise ValueError("Growth duration must be finite.")

    if growth_rate < 0:
        raise ValueError("Growth rate cannot be negative.")

    if time_hours < 0:
        raise ValueError("Growth duration cannot be negative.")

    return float(growth_rate * time_hours)


# ============================================================
# QUADRATIC METHANE REGRESSION
# ============================================================

def train_quadratic_model(data):
    """Fit a quadratic regression using methane concentration."""

    X = data[["methane_pct"]]
    y = data["growth_rate_um_h"]

    poly = PolynomialFeatures(
        degree=2,
        include_bias=False,
    )

    X_poly = poly.fit_transform(X)

    model = LinearRegression()
    model.fit(X_poly, y)

    return model, poly


def predict_quadratic_growth(model, poly, methane_pct):
    """Return an illustrative quadratic methane prediction."""

    if not np.isfinite(methane_pct):
        raise ValueError("Methane concentration must be finite.")

    if not 0 <= methane_pct <= 100:
        raise ValueError(
            "Methane concentration must be between 0 and 100%."
        )

    inputs = pd.DataFrame({
        "methane_pct": [methane_pct],
    })

    inputs_poly = poly.transform(inputs)
    prediction = float(model.predict(inputs_poly)[0])

    if not np.isfinite(prediction):
        raise ValueError("Model returned a non-finite prediction.")

    return prediction


# ============================================================
# EXPLORATORY SCENARIO COMPARISON
# ============================================================

def explore_growth_scenarios(
    model,
    methane_min=3,
    methane_max=100,
    temperature_min=800,
    temperature_max=900,
    methane_points=20,
    temperature_points=11,
):
    """
    Compare regression predictions across a bounded grid.

    This is an exploratory mathematical comparison,
    not validated reactor optimisation.
    """

    if not all(
        np.isfinite(value)
        for value in [
            methane_min,
            methane_max,
            temperature_min,
            temperature_max,
        ]
    ):
        raise ValueError("Scenario bounds must be finite.")

    if not 0 <= methane_min <= methane_max <= 100:
        raise ValueError("Invalid methane concentration range.")

    if not 0 < temperature_min <= temperature_max:
        raise ValueError("Invalid temperature range.")

    if (
        not isinstance(methane_points, (int, np.integer))
        or not isinstance(temperature_points, (int, np.integer))
        or isinstance(methane_points, (bool, np.bool_))
        or isinstance(temperature_points, (bool, np.bool_))
        or methane_points < 2
        or temperature_points < 2
    ):
        raise ValueError(
            "Scenario grid dimensions must be integers of at least 2."
        )

    methane_values = np.linspace(
        methane_min,
        methane_max,
        methane_points,
    )

    temperature_values = np.linspace(
        temperature_min,
        temperature_max,
        temperature_points,
    )

    scenarios = []

    for temperature in temperature_values:
        for methane in methane_values:

            prediction = predict_growth(
                model,
                methane_pct=float(methane),
                temperature_c=float(temperature),
            )

            scenarios.append({
                "methane_pct": float(methane),
                "temperature_c": float(temperature),
                "predicted_growth_um_h": prediction,
            })

    results = pd.DataFrame(scenarios)

    valid_results = results[
        np.isfinite(results["predicted_growth_um_h"])
        & (results["predicted_growth_um_h"] >= 0)
    ].copy()

    if valid_results.empty:
        return results, None

    best_index = valid_results["predicted_growth_um_h"].idxmax()
    best_scenario = valid_results.loc[best_index]

    return results, best_scenario


# ============================================================
# DIRECT EXECUTION TEST
# ============================================================

if __name__ == "__main__":

    data = load_data()
    model = train_model(data)

    growth_rate = predict_growth(
        model,
        methane_pct=20,
        temperature_c=800,
    )

    thickness = calculate_thickness(
        growth_rate,
        time_hours=5,
    )

    print(
        "Illustrative predicted growth rate:",
        round(growth_rate, 3),
        "µm/h",
    )

    print(
        "Estimated thickness:",
        round(thickness, 3),
        "µm",
    )

    print(
        "Warning: Predictions are not experimentally validated."
    )
