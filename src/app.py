
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

from model import (
    load_data,
    train_model,
    predict_growth,
    calculate_thickness,
    train_quadratic_model,
    predict_quadratic_growth,
    explore_growth_scenarios,
)


# ============================================================
# APPLICATION CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Diamond Growth Predictor",
    page_icon="💎",
    layout="wide",
)

st.title("💎 MPCVD Diamond Growth Predictor")

st.write(
    "An educational research prototype exploring how methane "
    "concentration and substrate temperature relate to "
    "microwave plasma CVD diamond growth rate."
)

st.warning(
    "Research prototype only. The regression models use six "
    "selected published observations and have not been "
    "independently validated. Predictions must not be used "
    "to select real MPCVD reactor operating conditions."
)


# ============================================================
# LOAD DATA AND TRAIN MODELS
# ============================================================

@st.cache_data
def get_data():
    return load_data()


@st.cache_resource
def get_linear_model():
    data = load_data()
    return train_model(data)


@st.cache_resource
def get_quadratic_model():
    data = load_data()
    return train_quadratic_model(data)


data = get_data()
linear_model = get_linear_model()
quadratic_model, poly = get_quadratic_model()


# ============================================================
# 1. PROCESS CONDITIONS
# ============================================================

st.header("1. Process Conditions")

methane = st.slider(
    "Methane concentration (%)",
    min_value=3,
    max_value=100,
    value=20,
    step=1,
)

temperature = st.slider(
    "Substrate temperature (°C)",
    min_value=800,
    max_value=900,
    value=800,
    step=10,
)

time_hours = st.slider(
    "Growth duration (hours)",
    min_value=1,
    max_value=24,
    value=5,
    step=1,
)

st.info(
    "The dataset contains only six selected published "
    "observations. The 800°C and 900°C experimental series "
    "involved different reactor conditions, including "
    "pressure and microwave power. These additional "
    "variables are not included in the regression models."
)


# ============================================================
# CHECK INPUTS AGAINST EXPERIMENTAL DATA
# ============================================================

exact_match = data[
    (data["methane_pct"] == methane)
    & (data["temperature_c"] == temperature)
]

if exact_match.empty:
    st.warning(
        "This exact methane-temperature combination is not "
        "represented in the six selected observations. "
        "The result is a regression estimate rather than "
        "a directly measured experimental value."
    )
else:
    st.caption(
        "This input combination appears in the selected "
        "experimental dataset. The displayed prediction "
        "is still a fitted model output, not the "
        "measured experimental growth rate."
    )

observed_temperatures = data["temperature_c"].unique()

if temperature not in observed_temperatures:
    st.warning(
        "The selected substrate temperature was not directly "
        "represented in the dataset. The prediction interpolates "
        "between temperature series that used different reactor "
        "operating conditions."
    )

observed_methane_values = data["methane_pct"].unique()

if methane not in observed_methane_values:
    st.caption(
        "The selected methane concentration does not exactly "
        "match any of the six recorded methane concentrations."
    )


# ============================================================
# 2. PREDICTED RESULTS
# ============================================================

st.header("2. Predicted Results")

growth_rate = predict_growth(
    linear_model,
    methane_pct=methane,
    temperature_c=temperature,
)

valid_prediction = np.isfinite(growth_rate) and growth_rate >= 0

if valid_prediction:
    thickness = calculate_thickness(
        growth_rate,
        time_hours,
    )
else:
    thickness = None

col1, col2 = st.columns(2)

with col1:
    if valid_prediction:
        st.metric(
            "Predicted growth rate",
            f"{growth_rate:.3f} µm/h",
        )
    else:
        st.metric(
            "Predicted growth rate",
            "Not available",
        )

with col2:
    if valid_prediction and np.isfinite(thickness):
        st.metric(
            "Estimated thickness",
            f"{thickness:.3f} µm",
        )
    else:
        st.metric(
            "Estimated thickness",
            "Not available",
        )

if not valid_prediction:
    st.error(
        "The regression model produced a negative or non-finite "
        "growth-rate prediction. A physically meaningful "
        "deposited thickness cannot be calculated from it."
    )


# ============================================================
# 3. MODEL INFORMATION
# ============================================================

st.header("3. Model Information")

st.write(
    "The main prediction uses multiple linear regression "
    "with methane concentration and substrate temperature "
    "as input variables."
)

st.write(
    "**Estimated thickness = Predicted growth rate × Growth duration**"
)

st.caption(
    "The thickness calculation assumes that the predicted "
    "growth rate remains constant throughout the selected "
    "duration. This assumption has not been experimentally "
    "validated by the current dataset."
)

st.caption(
    "The temperature coefficient cannot be interpreted as "
    "an isolated physical temperature effect because other "
    "reactor conditions differed between the experimental series."
)


# ============================================================
# 4. SCIENTIFIC VISUALISATIONS
# ============================================================

st.header("4. Scientific Visualisations")

st.write(
    "The graphs below illustrate how the fitted mathematical "
    "models respond to changes in methane concentration."
)

methane_values = np.linspace(
    data["methane_pct"].min(),
    data["methane_pct"].max(),
    100,
)

linear_predictions = []
quadratic_predictions = []

for methane_value in methane_values:

    linear_rate = predict_growth(
        linear_model,
        methane_pct=float(methane_value),
        temperature_c=temperature,
    )

    quadratic_rate = predict_quadratic_growth(
        quadratic_model,
        poly,
        methane_pct=float(methane_value),
    )

    linear_predictions.append(linear_rate)
    quadratic_predictions.append(quadratic_rate)


# Plot 1: Multiple linear regression

fig1, ax1 = plt.subplots(figsize=(8, 5))

ax1.plot(
    methane_values,
    linear_predictions,
    label=f"Linear model at {temperature} °C",
)

ax1.set_xlabel("Methane concentration (%)")
ax1.set_ylabel("Predicted growth rate (µm/h)")
ax1.set_title("Multiple Linear Regression")
ax1.grid(True, alpha=0.3)
ax1.legend()

fig1.tight_layout()

st.pyplot(fig1)
plt.close(fig1)


# Plot 2: Linear versus quadratic regression

fig2, ax2 = plt.subplots(figsize=(8, 5))

ax2.plot(
    methane_values,
    linear_predictions,
    label=f"Linear model at {temperature} °C",
)

ax2.plot(
    methane_values,
    quadratic_predictions,
    label="Quadratic methane model",
)

ax2.set_xlabel("Methane concentration (%)")
ax2.set_ylabel("Predicted growth rate (µm/h)")
ax2.set_title("Linear vs Quadratic Regression")
ax2.grid(True, alpha=0.3)
ax2.legend()

fig2.tight_layout()

st.pyplot(fig2)
plt.close(fig2)

st.caption(
    "The linear model includes methane concentration and "
    "substrate temperature. The quadratic model includes "
    "methane concentration only and pools observations from "
    "both temperature series. The curves are not directly "
    "equivalent physical process models."
)


# ============================================================
# 5. SCIENTIFIC LIMITATIONS
# ============================================================

st.header("5. Scientific Limitations")

if not valid_prediction:
    st.error(
        "The selected inputs produced a negative or non-finite "
        "model prediction. This must not be interpreted as "
        "a valid positive diamond-deposition rate."
    )

st.info(
    "The regression models describe mathematical relationships "
    "within six selected observations. They do not account "
    "fully for reactor pressure, microwave power, gas chemistry, "
    "substrate properties or diamond quality."
)

st.warning(
    "The fitted curves and thickness estimates are exploratory "
    "mathematical outputs. They have not been validated against "
    "independent experimental measurements."
)


# ============================================================
# 6. EXPLORATORY SCENARIO COMPARISON
# ============================================================

st.header("6. Exploratory Scenario Comparison")

st.write(
    "Compare the multiple linear regression model's predictions "
    "across a grid of methane concentrations and temperatures."
)

st.warning(
    "This is an educational scenario comparison, not a "
    "validated reactor optimisation tool. The scenario grid "
    "includes combinations that were not experimentally tested. "
    "The highest predicted growth rate is a mathematical result "
    "and must not be interpreted as an optimal or recommended "
    "reactor setting."
)

if st.button("Compare Scenarios"):

    results, best = explore_growth_scenarios(linear_model)

    st.write(
        f"Number of scenarios evaluated: {len(results)}"
    )

    if best is None:

        st.error(
            "No non-negative predicted growth rates were "
            "found in the evaluated scenarios."
        )

    else:

        st.subheader("Highest Model-Predicted Scenario")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Methane concentration",
                f"{best['methane_pct']:.2f}%",
            )

        with col2:
            st.metric(
                "Substrate temperature",
                f"{best['temperature_c']:.0f} °C",
            )

        with col3:
            st.metric(
                "Predicted growth rate",
                f"{best['predicted_growth_um_h']:.3f} µm/h",
            )

        st.caption(
            "This is the highest mathematical prediction among "
            "the evaluated grid points. It is not a recommended "
            "MPCVD operating condition."
        )

    st.subheader("Scenario Results")

    st.dataframe(
        results,
        use_container_width=True,
    )
