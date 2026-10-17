
import sys
from pathlib import Path

import numpy as np
import pytest

# Allow tests to import the modelling module
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from model import (  # noqa: E402
    calculate_thickness,
    explore_growth_scenarios,
    load_data,
    predict_growth,
    predict_quadratic_growth,
    train_model,
    train_quadratic_model,
)


# ============================================================
# 1. DATASET TESTS
# ============================================================

def test_data_loads():
    data = load_data()

    assert not data.empty
    assert len(data) == 6

    assert "methane_pct" in data.columns
    assert "temperature_c" in data.columns
    assert "growth_rate_um_h" in data.columns

    assert not data.isnull().any().any()


def test_data_contains_expected_temperatures():
    data = load_data()

    assert set(data["temperature_c"]) == {800, 900}


# ============================================================
# 2. LINEAR REGRESSION TESTS
# ============================================================

def test_known_prediction():
    data = load_data()
    model = train_model(data)

    prediction = predict_growth(
        model,
        methane_pct=20,
        temperature_c=800,
    )

    assert prediction == pytest.approx(
        1.7620877135,
        abs=0.001,
    )


def test_linear_prediction_is_finite():
    data = load_data()
    model = train_model(data)

    prediction = predict_growth(
        model,
        methane_pct=40,
        temperature_c=900,
    )

    assert np.isfinite(prediction)


def test_negative_methane_rejected():
    data = load_data()
    model = train_model(data)

    with pytest.raises(ValueError):
        predict_growth(
            model,
            methane_pct=-5,
            temperature_c=800,
        )


def test_methane_above_100_rejected():
    data = load_data()
    model = train_model(data)

    with pytest.raises(ValueError):
        predict_growth(
            model,
            methane_pct=105,
            temperature_c=800,
        )


def test_nonfinite_prediction_input_rejected():
    data = load_data()
    model = train_model(data)

    with pytest.raises(ValueError):
        predict_growth(
            model,
            methane_pct=float("nan"),
            temperature_c=800,
        )


# ============================================================
# 3. QUADRATIC REGRESSION TESTS
# ============================================================

def test_quadratic_prediction():
    data = load_data()
    model, poly = train_quadratic_model(data)

    prediction = predict_quadratic_growth(
        model,
        poly,
        methane_pct=20,
    )

    assert prediction == pytest.approx(
        3.229972,
        abs=0.001,
    )


def test_quadratic_invalid_methane_rejected():
    data = load_data()
    model, poly = train_quadratic_model(data)

    with pytest.raises(ValueError):
        predict_quadratic_growth(
            model,
            poly,
            methane_pct=-10,
        )


# ============================================================
# 4. THICKNESS TESTS
# ============================================================

def test_thickness_calculation():
    result = calculate_thickness(
        growth_rate=2,
        time_hours=5,
    )

    assert result == 10


def test_thickness_zero_duration():
    result = calculate_thickness(
        growth_rate=2,
        time_hours=0,
    )

    assert result == 0


def test_negative_growth_rate_rejected():
    with pytest.raises(ValueError):
        calculate_thickness(-2, 5)


def test_negative_duration_rejected():
    with pytest.raises(ValueError):
        calculate_thickness(2, -5)


def test_nonfinite_thickness_inputs_rejected():
    with pytest.raises(ValueError):
        calculate_thickness(float("nan"), 5)

    with pytest.raises(ValueError):
        calculate_thickness(2, float("inf"))


# ============================================================
# 5. SCENARIO COMPARISON TESTS
# ============================================================

def test_scenario_count():
    data = load_data()
    model = train_model(data)

    results, best = explore_growth_scenarios(model)

    assert len(results) == 220


def test_scenario_columns():
    data = load_data()
    model = train_model(data)

    results, best = explore_growth_scenarios(model)

    assert "methane_pct" in results.columns
    assert "temperature_c" in results.columns
    assert "predicted_growth_um_h" in results.columns


def test_best_scenario_is_highest_valid_prediction():
    data = load_data()
    model = train_model(data)

    results, best = explore_growth_scenarios(model)

    valid_results = results[
        results["predicted_growth_um_h"] >= 0
    ]

    assert best is not None

    assert best["predicted_growth_um_h"] == pytest.approx(
        valid_results["predicted_growth_um_h"].max()
    )


def test_invalid_scenario_range_rejected():
    data = load_data()
    model = train_model(data)

    with pytest.raises(ValueError):
        explore_growth_scenarios(
            model,
            methane_min=100,
            methane_max=3,
        )


def test_invalid_scenario_grid_size_rejected():
    data = load_data()
    model = train_model(data)

    with pytest.raises(ValueError):
        explore_growth_scenarios(
            model,
            methane_points=1,
        )
