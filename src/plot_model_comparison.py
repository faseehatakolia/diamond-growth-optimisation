
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from model import (
    load_data,
    train_model,
    train_quadratic_model,
)


# ============================================================
# 1. LOAD EXPERIMENTAL DATA
# ============================================================

data = load_data()


# ============================================================
# 2. TRAIN REGRESSION MODELS
# ============================================================

linear_model = train_model(data)

quadratic_model, poly = train_quadratic_model(data)


# ============================================================
# 3. GENERATE FITTED PREDICTIONS
# ============================================================

X_linear = data[["methane_pct", "temperature_c"]]
X_quadratic = data[["methane_pct"]]

observed = data["growth_rate_um_h"].to_numpy()

linear_pred = linear_model.predict(X_linear)

quadratic_pred = quadratic_model.predict(
    poly.transform(X_quadratic)
)


# ============================================================
# 4. CREATE MODEL COMPARISON FIGURE
# ============================================================

fig, ax = plt.subplots(figsize=(7.5, 6))

ax.scatter(
    observed,
    linear_pred,
    s=85,
    marker="o",
    label="Multiple linear regression",
)

ax.scatter(
    observed,
    quadratic_pred,
    s=85,
    marker="s",
    label="Quadratic methane regression",
)


# ============================================================
# 5. PERFECT AGREEMENT REFERENCE LINE
# ============================================================

limit = max(
    np.max(observed),
    np.max(linear_pred),
    np.max(quadratic_pred),
) + 0.3

ax.plot(
    [0, limit],
    [0, limit],
    linestyle="--",
    color="black",
    linewidth=1,
    label="Perfect agreement",
)


# ============================================================
# 6. SCIENTIFIC FORMATTING
# ============================================================

ax.set_xlabel("Observed growth rate (µm/h)")
ax.set_ylabel("Fitted growth rate (µm/h)")
ax.set_title("Observed vs Fitted Diamond Growth Rates")

ax.set_xlim(0, limit)
ax.set_ylim(0, limit)

ax.set_aspect("equal", adjustable="box")
ax.grid(True, alpha=0.25)
ax.legend()

fig.tight_layout()


# ============================================================
# 7. SAVE FIGURE
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RESULTS_DIR = PROJECT_ROOT / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

output_path = RESULTS_DIR / "figure_2_model_comparison.png"

fig.savefig(
    output_path,
    dpi=300,
    bbox_inches="tight",
)

plt.show()
plt.close(fig)

print(f"Figure saved to: {output_path}")
print(
    "Note: This figure shows in-sample fitted values, "
    "not independently validated predictions."
)
