import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import streamlit as st

from model import (
    load_data,
    train_model,
    predict_growth,
    calculate_thickness,
    train_quadratic_model,
    predict_quadratic_growth,
     explore_growth_scenarios
)


# Configure the application
st.set_page_config(
	page_title="Diamond Growth Predictor",
	page_icon="💎",
	layout="wide"
)


# Title and introduction
st.title("💎 MPCVD Diamond Growth Predictor")

st.write(
	"An educational prototype exploring how methane "
	"concentration and substrate temperature relate "
	"to diamond growth rate."
)


st.warning(
    "Research prototype only. The regression models use "
    "six selected published observations and have not "
    "been independently validated. Predictions must not "
    "be used to select real MPCVD reactor conditions."
)



# Load the dataset and train the model
@st.cache_resource
def get_model():
	data = load_data()
	model = train_model(data)
	return model


model = get_model()
@st.cache_resource
def get_quadratic_model():
    data = load_data()
    return train_quadratic_model(data)


quadratic_model, poly = get_quadratic_model()

# User inputs
st.header("1. Process Conditions")

methane = st.slider(
	"Methane concentration (%)",
	min_value=3,
	max_value=100,
	value=20,
	step=1
)

temperature = st.slider(
	"Substrate temperature (°C)",
	min_value=800,
	max_value=900,
	value=800,
	step=10
)

time_hours = st.slider(
	"Growth duration (hours)",
	min_value=1,
	max_value=24,
	value=5,
	step=1
)


# Explain limitations of the selected experimental data
st.info(
    "The dataset contains only six selected published "
    "observations. The two temperature series involved "
    "different reactor conditions, including pressure "
    "and microwave power. These variables are not "
    "included in the regression model."
)

# Check whether the exact input pair appears in the dataset
observed_data = load_data()

exact_match = observed_data[
    (observed_data["methane_pct"] == methane)
    & (observed_data["temperature_c"] == temperature)
]

if exact_match.empty:
    st.warning(
        "This exact methane-temperature combination "
        "is not represented in the six selected observations. "
        "The result is a regression estimate, not a "
        "directly measured experimental value."
    )
else:
    st.caption(
        "This input combination appears in the selected "
        "experimental dataset. The displayed prediction "
        "is still a fitted model output, not the "
        "measured growth rate."
    )



# Calculate the predicted growth rate
growth_rate = predict_growth(
    model,
    methane_pct=methane,
    temperature_c=temperature
)

# Check whether the prediction is physically appropriate
valid_prediction = growth_rate >= 0

if valid_prediction:
    thickness = calculate_thickness(
        growth_rate,
        time_hours
    )
else:
    thickness = None


# Display results
st.header("2. Predicted Results")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Predicted growth rate",
        f"{growth_rate:.3f} µm/h"
    )

with col2:
    if valid_prediction:
        st.metric(
            "Estimated thickness",
            f"{thickness:.3f} µm"
        )
    else:
        st.metric(
            "Estimated thickness",
            "Not available"
        )

if not valid_prediction:
    st.error(
        "The regression model has predicted a negative "
        "growth rate. Deposited thickness has therefore "
        "not been calculated."
    )




# Explain the calculations
st.header("3. Model Information")

st.write(
	"The application uses multiple linear regression "
	"with methane concentration and substrate temperature "
	"as input variables."
)

st.write(
	"Estimated thickness = Predicted growth rate × Growth duration"
)

st.caption(
	"Scientific limitation: The model is not independently "
	"validated, and its predictions may be physically unrealistic."
)


# ----------------------------------------
# 4. Scientific Visualisations
# ----------------------------------------

st.header("4. Scientific Visualisations")

st.write(
    "Explore how the fitted regression models respond "
    "to changes in methane concentration."
)

data = load_data()

# Create methane values within the observed range
methane_values = np.linspace(
    data["methane_pct"].min(),
    data["methane_pct"].max(),
    100
)

linear_predictions = []
quadratic_predictions = []

for methane_value in methane_values:

    linear_rate = predict_growth(
        model,
        methane_pct=methane_value,
        temperature_c=temperature
    )

    quadratic_rate = predict_quadratic_growth(
        quadratic_model,
        poly,
        methane_pct=methane_value
    )

    linear_predictions.append(linear_rate)
    quadratic_predictions.append(quadratic_rate)


# Plot 1: Linear regression
fig1, ax1 = plt.subplots()

ax1.plot(
    methane_values,
    linear_predictions,
    label=f"Linear model at {temperature} °C"
)

ax1.set_xlabel("Methane concentration (%)")
ax1.set_ylabel("Predicted growth rate (µm/h)")
ax1.set_title("Multiple Linear Regression")
ax1.grid(True)
ax1.legend()

st.pyplot(fig1)
plt.close(fig1)


# Plot 2: Model comparison
fig2, ax2 = plt.subplots()

ax2.plot(
    methane_values,
    linear_predictions,
    label="Linear model"
)

ax2.plot(
    methane_values,
    quadratic_predictions,
    label="Quadratic model"
)

ax2.set_xlabel("Methane concentration (%)")
ax2.set_ylabel("Predicted growth rate (µm/h)")
ax2.set_title("Linear vs Quadratic Regression")
ax2.grid(True)
ax2.legend()

st.pyplot(fig2)
plt.close(fig2)


# ----------------------------------------
# 5. Scientific Limitations
# ----------------------------------------

st.header("5. Scientific Limitations")

if growth_rate < 0:
    st.error(
        "The model has produced a negative growth-rate "
        "prediction. This result should not be interpreted "
        "as a valid positive diamond-deposition rate."
    )

st.info(
    "The quadratic model uses methane concentration only, "
    "whereas the linear model also includes temperature. "
    "Their predictions are not directly equivalent."
)

st.warning(
    "The dataset contains only six provisional observations. "
    "The curves are mathematical demonstrations and have "
    "not been validated against independent experiments."
)

# ----------------------------------------
# 6. Exploratory Scenario Comparison
# ----------------------------------------

st.header("6. Exploratory Scenario Comparison")

st.write(
    "Compare the mathematical predictions of the "
    "linear regression model across a grid of "
    "methane concentrations and temperatures."
)

st.warning(
    "This is an educational scenario comparison, "
    "not a validated reactor optimisation tool. "
    "The input combinations have not all been "
    "experimentally tested."
)

if st.button("Compare Scenarios"):

    results, best = explore_growth_scenarios(model)

    st.write(
        f"Number of scenarios evaluated: {len(results)}"
    )

    if best is None:

        st.error(
            "No non-negative predicted growth rates "
            "were found in the evaluated scenarios."
        )

    else:

        st.subheader("Highest Model-Predicted Scenario")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Methane concentration",
                f"{best['methane_pct']:.2f}%"
            )

        with col2:
            st.metric(
                "Substrate temperature",
                f"{best['temperature_c']:.0f} °C"
            )

        with col3:
            st.metric(
                "Predicted growth rate",
                f"{best['predicted_growth_um_h']:.3f} µm/h"
            )

        st.caption(
            "This is the highest mathematical prediction "
            "among the evaluated grid points. It is not "
            "a recommended MPCVD operating condition."
        )

    st.subheader("Scenario Results")

    st.dataframe(
        results,
        use_container_width=True
    )
