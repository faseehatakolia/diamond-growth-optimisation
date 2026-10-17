
from pathlib import Path

import matplotlib.pyplot as plt

from model import load_data


# ============================================================
# 1. LOAD EXPERIMENTAL DATA
# ============================================================

data = load_data()


# ============================================================
# 2. CREATE RESULTS DIRECTORY
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RESULTS_DIR = PROJECT_ROOT / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 3. CREATE EXPERIMENTAL GROWTH FIGURE
# ============================================================

fig, ax = plt.subplots(figsize=(8, 5.5))

for temperature, group in data.groupby("temperature_c"):

    ax.scatter(
        group["methane_pct"],
        group["growth_rate_um_h"],
        s=85,
        label=f"{temperature:.0f} °C",
    )


# ============================================================
# 4. SCIENTIFIC FORMATTING
# ============================================================

ax.set_xlabel("Methane concentration (%)")
ax.set_ylabel("Diamond growth rate (µm/h)")
ax.set_title("Experimental MPCVD Diamond Growth Rates")

ax.legend(title="Reported temperature")
ax.grid(True, alpha=0.25)

ax.set_xlim(0, 105)
ax.set_ylim(bottom=0)

fig.tight_layout()


# ============================================================
# 5. SAVE FIGURE
# ============================================================

output_path = RESULTS_DIR / "figure_1_experimental_growth.png"

fig.savefig(
    output_path,
    dpi=300,
    bbox_inches="tight",
)

plt.show()
plt.close(fig)

print(f"Figure saved to: {output_path}")
