
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from model import (
    load_data,
    train_model,
    predict_growth,
    calculate_thickness,
)


# ============================================================
# 1. LOAD DATA AND TRAIN MODEL
# ============================================================

data = load_data()
model = train_model(data)


# ============================================================
# 2. DEFINE REFERENCE CONDITIONS
# ============================================================

methane_pct = 20
temperature_c = 800
duration_h = 5


# ============================================================
# 3. CALCULATE PREDICTED GROWTH RATE
# ============================================================

growth_rate = predict_growth(
    model,
    methane_pct=methane_pct,
    temperature_c=temperature_c,
)

if not np.isfinite(growth_rate) or growth_rate < 0:
    raise ValueError(
        "The model produced an invalid growth-rate prediction."
    )


# ============================================================
# 4. CALCULATE PREDICTED THICKNESS
# ============================================================

time_h = np.linspace(
    0,
    duration_h,
    100,
)

thickness_um = np.array([
    calculate_thickness(growth_rate, time)
    for time in time_h
])

final_thickness = calculate_thickness(
    growth_rate,
    duration_h,
)


# ============================================================
# 5. CREATE THICKNESS FIGURE
# ============================================================

fig, ax = plt.subplots(figsize=(8, 5))

ax.plot(
    time_h,
    thickness_um,
    color="navy",
    linewidth=2.5,
    label="Predicted diamond thickness",
)

ax.scatter(
    duration_h,
    final_thickness,
    color="darkred",
    s=70,
    zorder=3,
)

ax.annotate(
    f"{final_thickness:.3f} µm at {duration_h} h",
    xy=(duration_h, final_thickness),
    xytext=(-145, -35),
    textcoords="offset points",
    arrowprops={"arrowstyle": "->"},
)


# ============================================================
# 6. SCIENTIFIC FORMATTING
# ============================================================

ax.set_title("Illustrative Predicted Diamond Thickness")
ax.set_xlabel("Deposition time (hours)")
ax.set_ylabel("Predicted diamond thickness (µm)")

ax.set_xlim(0, duration_h + 0.3)
ax.set_ylim(bottom=0)

ax.grid(True, alpha=0.3)
ax.legend(loc="upper left")

fig.tight_layout()


# ============================================================
# 7. SAVE FIGURE
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RESULTS_DIR = PROJECT_ROOT / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

output_path = RESULTS_DIR / "figure_3_predicted_thickness.png"

fig.savefig(
    output_path,
    dpi=300,
    bbox_inches="tight",
)

print(f"Figure saved to: {output_path}")
print(f"Predicted growth rate: {growth_rate:.3f} µm/h")
print(
    f"Predicted thickness after {duration_h} hours: "
    f"{final_thickness:.3f} µm"
)

print(
    "Warning: Thickness assumes a constant growth rate "
    "and has not been experimentally validated."
)

plt.show()
plt.close(fig)
