import sys
from pathlib import Path

# Locate the project
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from model import (
	load_data,
	train_model,
	predict_growth,
	calculate_thickness,
)


def main():
	data = load_data()
	model = train_model(data)

	methane = 20
	temperature = 800
	duration = 5

	growth_rate = predict_growth(
		model,
		methane_pct=methane,
		temperature_c=temperature,
	)
	thickness = calculate_thickness(growth_rate, duration)

	print("MPCVD Reproducibility Check")
	print("--------------------------")
	print("Observations:", len(data))
	print("Methane concentration:", methane, "%")
	print("Substrate temperature:", temperature, "°C")
	print("Growth duration:", duration, "hours")
	print("Predicted growth rate:", round(growth_rate, 3), "µm/h")
	print("Estimated thickness:", round(thickness, 3), "µm")
	print(
		"Warning: Results are illustrative "
		"and not experimentally validated."
	)


if __name__ == "__main__":
	main()
