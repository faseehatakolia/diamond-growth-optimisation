from sklearn.preprocessing import PolynomialFeatures

from pathlib import Path

import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

# Locate the dataset relative to this Python file
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "mpcvd_experimental_data_v01.csv"


def load_data():
	"""Load the provisional MPCVD dataset."""

	data = pd.read_csv(DATA_PATH)

	return data


def train_model(data):
	"""Fit a multiple linear regression model."""

	X = data[["methane_pct", "temperature_c"]]
	y = data["growth_rate_um_h"]

	model = LinearRegression()
	model.fit(X, y)

	return model


def predict_growth(model, methane_pct, temperature_c):
	"""Calculate an illustrative diamond growth-rate prediction."""

	inputs = pd.DataFrame({
		"methane_pct": [methane_pct],
		"temperature_c": [temperature_c]
	})

	prediction = model.predict(inputs)[0]

	return float(prediction)


def calculate_thickness(growth_rate, time_hours):
	"""Estimate thickness assuming constant growth rate."""

	return growth_rate * time_hours


def train_quadratic_model(data):
    """Fit a quadratic model using methane concentration only."""

    X = data[["methane_pct"]]
    y = data["growth_rate_um_h"]

    poly = PolynomialFeatures(
        degree=2,
        include_bias=False
    )

    X_poly = poly.fit_transform(X)

    model = LinearRegression()
    model.fit(X_poly, y)

    return model, poly


def predict_quadratic_growth(model, poly, methane_pct):
    """Return an illustrative quadratic prediction."""

    inputs = pd.DataFrame({
        "methane_pct": [methane_pct]
    })

    inputs_poly = poly.transform(inputs)

    prediction = model.predict(inputs_poly)[0]

    return float(prediction)




def explore_growth_scenarios(
    model,
    methane_min=3,
    methane_max=100,
    temperature_min=800,
    temperature_max=900,
    methane_points=20,
    temperature_points=11
):
    """
    Compare illustrative regression predictions over
    a bounded grid of input combinations.

    This is not validated reactor optimisation.
    """

    methane_values = np.linspace(
        methane_min,
        methane_max,
        methane_points
    )

    temperature_values = np.linspace(
        temperature_min,
        temperature_max,
        temperature_points
    )

    scenarios = []

    for temperature in temperature_values:
        for methane in methane_values:

            prediction = predict_growth(
                model,
                methane_pct=methane,
                temperature_c=temperature
            )

            scenarios.append({
                "methane_pct": methane,
                "temperature_c": temperature,
                "predicted_growth_um_h": prediction
            })

    results = pd.DataFrame(scenarios)

    # Exclude negative deposition-rate predictions
    valid_results = results[
        results["predicted_growth_um_h"] >= 0
    ].copy()

    if valid_results.empty:
        return results, None

    best_index = valid_results[
        "predicted_growth_um_h"
    ].idxmax()

    best_scenario = valid_results.loc[best_index]

    return results, best_scenario


if __name__ == "__main__":

	data = load_data()
	model = train_model(data)

	growth_rate = predict_growth(
		model,
		methane_pct=20,
		temperature_c=800
	)

	thickness = calculate_thickness(
		growth_rate,
		time_hours=5
	)

	print("Illustrative predicted growth rate:", growth_rate, "µm/h")
	print("Estimated thickness:", thickness, "µm")
	print("Warning: Predictions are not experimentally validated.")
