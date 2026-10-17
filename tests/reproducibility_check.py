
import sys
from pathlib import Path

import numpy as np

# ============================================================
# 1. LOCATE THE PROJECT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from model import (  # noqa: E402
    load_data,
    train_model,
    predict_growth,
    calculate_thickness,
    train_quadratic_model,
    predict_quadratic_growth,
)


# ============================================================
# 2. REPRODUCIBILITY CHECK
# ============================================================

def main():
    """Verify the dataset and reproduce reference predictions."""

    data = load_data()

    # Check the expected dataset structure
    assert len(data) == 6, "Unexpected number of observations."

    # Train the linear model
    linear_model = train_model(data)

    # Reference conditions
    methane = 20
    temperature = 800
    duration = 5

    # Calculate linear prediction
    growth_rate = predict_growth(
        linear_model,
        methane_pct=methane,
        temperature_c=temperature,
    )

    thickness = calculate_thickness(
        growth_rate,
        duration,
    )

    # Train and evaluate quadratic model
    quadratic_model, poly = train_quadratic_model(data)

    quadratic_growth = predict_quadratic_growth(
        quadratic_model,
        poly,
        methane_pct=methane,
    )

    # ========================================================
    # 3. VERIFY EXPECTED RESULTS
    # ========================================================

    assert np.isclose(
        growth_rate,
        1.7620877135,
        atol=0.001,
        rtol=0,
    ), "Linear prediction differs from the reference."

    assert np.isclose(
        thickness,
        8.8104385675,
        atol=0.001,
        rtol=0,
    ), "Thickness differs from the reference."

    assert np.isclose(
        quadratic_growth,
        3.229972,
        atol=0.001,
        rtol=0,
    ), "Quadratic prediction differs from the reference."

    # ========================================================
    # 4. DISPLAY RESULTS
    # ========================================================

    print("\nMPCVD Reproducibility Check")
    print("---------------------------")

    print("Observations:", len(data))
    print("Methane concentration:", methane, "%")
    print("Substrate temperature:", temperature, "°C")
    print("Growth duration:", duration, "hours")

    print(
        "Linear predicted growth rate:",
        f"{growth_rate:.3f} µm/h",
    )

    print(
        "Estimated thickness:",
        f"{thickness:.3f} µm",
    )

    print(
        "Quadratic predicted growth rate:",
        f"{quadratic_growth:.3f} µm/h",
    )

    print("\nAll reproducibility checks passed.")

    print(
        "Warning: Results are illustrative and "
        "have not been independently validated."
    )


# ============================================================
# 5. RUN SCRIPT
# ============================================================

if __name__ == "__main__":
    main()
