from pathlib import Path

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures

# Locate the dataset relative to this script.
project_root = Path(__file__).resolve().parents[1]
data_path = project_root / "data" / "mpcvd_experimental_data_v01.csv"

df = pd.read_csv(data_path)

# Model A: Multiple linear regression
X_linear = df[["methane_pct", "temperature_c"]]
y = df["growth_rate_um_h"]

linear_model = LinearRegression()
linear_model.fit(X_linear, y)
linear_predictions = linear_model.predict(X_linear)

# Model B: Quadratic regression using methane only
X_methane = df[["methane_pct"]]
polynomial = PolynomialFeatures(degree=2, include_bias=False)
X_quadratic = polynomial.fit_transform(X_methane)

quadratic_model = LinearRegression()
quadratic_model.fit(X_quadratic, y)
quadratic_predictions = quadratic_model.predict(X_quadratic)


def report_metrics(name, actual, predicted):
	mae = mean_absolute_error(actual, predicted)
	rmse = mean_squared_error(actual, predicted) ** 0.5
	r_squared = r2_score(actual, predicted)

	print(f"\n{name}")
	print(f"MAE:  {mae:.4f} µm/h")
	print(f"RMSE: {rmse:.4f} µm/h")
	print(f"R²:   {r_squared:.4f}")


report_metrics("Multiple linear regression", y, linear_predictions)
report_metrics("Quadratic methane regression", y, quadratic_predictions)

results = df.copy()
results["linear_prediction"] = linear_predictions
results["quadratic_prediction"] = quadratic_predictions

print("\nObserved versus fitted values:")
print(results.to_string(index=False))

# Reproduce the reference input using this fitted linear model.
reference = pd.DataFrame(
	{"methane_pct": [20], "temperature_c": [800]}
)

growth = float(linear_model.predict(reference)[0])
thickness = growth * 5

print("\nReference calculation:")
print(f"Growth rate: {growth:.3f} µm/h")
print(f"Thickness:   {thickness:.3f} µm")
