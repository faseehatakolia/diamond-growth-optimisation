
from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.model_selection import LeaveOneOut, cross_val_predict
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures


# ============================================================
# 1. LOAD EXPERIMENTAL DATA
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "mpcvd_experimental_data_v01.csv"

df = pd.read_csv(DATA_PATH)

X_linear = df[["methane_pct", "temperature_c"]]
X_methane = df[["methane_pct"]]
y = df["growth_rate_um_h"]


# ============================================================
# 2. FIT MULTIPLE LINEAR REGRESSION
# ============================================================

linear_model = LinearRegression()
linear_model.fit(X_linear, y)

linear_predictions = linear_model.predict(X_linear)


# ============================================================
# 3. FIT QUADRATIC METHANE REGRESSION
# ============================================================

quadratic_model = make_pipeline(
    PolynomialFeatures(degree=2, include_bias=False),
    LinearRegression(),
)

quadratic_model.fit(X_methane, y)

quadratic_predictions = quadratic_model.predict(X_methane)


# ============================================================
# 4. MODEL PERFORMANCE METRICS
# ============================================================

def report_metrics(name, actual, predicted):
    """Calculate and display model performance metrics."""

    mae = mean_absolute_error(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))
    r_squared = r2_score(actual, predicted)

    print(f"\n{name}")
    print(f"MAE:  {mae:.4f} µm/h")
    print(f"RMSE: {rmse:.4f} µm/h")
    print(f"R²:   {r_squared:.4f}")


print("\n=== IN-SAMPLE MODEL PERFORMANCE ===")

report_metrics(
    "Multiple linear regression",
    y,
    linear_predictions,
)

report_metrics(
    "Quadratic methane regression",
    y,
    quadratic_predictions,
)


# ============================================================
# 5. LEAVE-ONE-OUT CROSS-VALIDATION
# ============================================================

loo = LeaveOneOut()

linear_cv_predictions = cross_val_predict(
    LinearRegression(),
    X_linear,
    y,
    cv=loo,
)

quadratic_cv_predictions = cross_val_predict(
    make_pipeline(
        PolynomialFeatures(degree=2, include_bias=False),
        LinearRegression(),
    ),
    X_methane,
    y,
    cv=loo,
)

print("\n=== LEAVE-ONE-OUT CROSS-VALIDATION ===")

report_metrics(
    "Multiple linear regression (LOOCV)",
    y,
    linear_cv_predictions,
)

report_metrics(
    "Quadratic methane regression (LOOCV)",
    y,
    quadratic_cv_predictions,
)


# ============================================================
# 6. OBSERVED VERSUS PREDICTED VALUES
# ============================================================

results = df.copy()

results["linear_prediction"] = linear_predictions
results["quadratic_prediction"] = quadratic_predictions

results["linear_loocv_prediction"] = linear_cv_predictions
results["quadratic_loocv_prediction"] = quadratic_cv_predictions

print("\n=== OBSERVED VERSUS PREDICTED VALUES ===")
print(results.to_string(index=False))


# ============================================================
# 7. REFERENCE PREDICTION
# ============================================================

reference = pd.DataFrame({
    "methane_pct": [20],
    "temperature_c": [800],
})

growth_rate = float(linear_model.predict(reference)[0])
thickness = growth_rate * 5

print("\n=== REFERENCE CALCULATION ===")
print(f"Growth rate: {growth_rate:.3f} µm/h")
print(f"Thickness:   {thickness:.3f} µm")


# ============================================================
# 8. SCIENTIFIC INTERPRETATION
# ============================================================

print("\n=== SCIENTIFIC LIMITATIONS ===")

print(
    "All models use only six selected experimental observations."
)

print(
    "In-sample metrics measure fit to the training data "
    "and are not independent validation."
)

print(
    "LOOCV provides a small-sample diagnostic but does not "
    "replace independent experimental validation."
)

print(
    "The two temperature series used different reactor "
    "conditions, so the linear model cannot isolate "
    "a causal temperature effect."
)

print(
    "The quadratic model uses methane concentration only "
    "and pools observations from both temperature series."
)
