import sys
from pathlib import Path

import pytest

# Allow tests to import the modelling module
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from model import (  # noqa: E402
	calculate_thickness,
	explore_growth_scenarios,
	load_data,
	predict_growth,
	train_model,
	train_quadratic_model,
predict_quadratic_growth,
)


def test_data_loads():
	data = load_data()

	assert not data.empty
	assert "methane_pct" in data.columns
	assert "temperature_c" in data.columns
	assert "growth_rate_um_h" in data.columns


def test_known_prediction():
	data = load_data()
	model = train_model(data)

	prediction = predict_growth(
		model,
		methane_pct=20,
		temperature_c=800,
	)

	assert prediction == pytest.approx(1.7620877135, abs=0.001)


def test_thickness_calculation():
	result = calculate_thickness(growth_rate=2, time_hours=5)

	assert result == 10


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


def test_quadratic_prediction():
    data = load_data()
    model, poly = train_quadratic_model(data)

    prediction = predict_quadratic_growth(
        model,
        poly,
        methane_pct=20,
    )

    assert prediction == pytest.approx(3.229972, abs=0.001)


def test_thickness_zero_duration():
    result = calculate_thickness(
        growth_rate=2,
        time_hours=0,
    )

    assert result == 0


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
