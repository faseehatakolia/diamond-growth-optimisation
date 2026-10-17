
# Predictive Modelling and Optimisation of Microwave Plasma CVD Diamond Growth Using Experimental Data

**Independent computational materials-engineering research project**

**Status:** Version 0.1 — Exploratory research prototype

**Technologies:** Python · scikit-learn · pandas · NumPy · Matplotlib · Streamlit · pytest · Jupyter

---

## 1. Project Overview

This project investigates the application of mathematical modelling and Python-based computational methods to microwave plasma chemical vapour deposition (MPCVD) diamond growth.

It explores relationships between selected experimental process variables and diamond growth rate using regression models, scientific visualisations and an interactive Streamlit application.

The current implementation demonstrates computational modelling and exploratory scenario comparison. It is not an experimentally validated reactor optimisation system.

## 2. Research Motivation

Lab-grown diamonds have engineering applications in thermal management, electronics, optics and industrial materials.

MPCVD diamond growth is influenced by several interacting variables, including:

- Methane concentration and gas composition
- Substrate temperature
- Reactor pressure
- Microwave power
- Substrate and seed characteristics

Understanding these relationships could support more reliable and efficient diamond manufacturing.

This project explores how computational methods might contribute to that research.

## 3. Research Objectives

1. Investigate the scientific principles underlying MPCVD diamond growth.
2. Identify and document published experimental growth-rate observations.
3. Develop and compare exploratory mathematical models.
4. Implement an interactive application for investigating model outputs.
5. Assess model performance and computational reproducibility.
6. Identify limitations and requirements for future scientific validation.

## 4. Dataset and Provenance

The project uses six selected experimental observations reported by Martyanov et al. (2023).

**Dataset:** `data/mpcvd_experimental_data_v01.csv`

The dataset contains:

- Observation identifier
- Substrate temperature (°C)
- Methane concentration (%)
- Diamond growth rate (µm/h)
- Experimental series identifier

The observations represent two reported temperature series: 800°C and 900°C.

**Primary source:**

Martyanov et al. (2023), *Synthesis of Polycrystalline Diamond Films in Microwave Plasma at Ultrahigh Concentrations of Methane*.

https://doi.org/10.3390/coatings13040751

The six numerical observations were checked against the published article text.

However, the provisional dataset does not fully encode the original experimental conditions. In particular, pressure and microwave power differed between the reported series and are not included as predictors.

Consequently, differences between the series cannot be attributed to temperature alone.

Further information is provided in `data/DATASET_README.md`.

## 5. Mathematical Methods

### 5.1 Multiple Linear Regression

The initial model estimates diamond growth rate using methane concentration and substrate temperature:

Predicted growth rate = β₀ + β₁ × methane concentration + β₂ × substrate temperature

Coefficients are estimated using ordinary least squares.

The model is exploratory because the dataset is small and the recorded temperature values are associated with other changes in reactor conditions.

### 5.2 Quadratic Methane Regression

A second model investigates a nonlinear relationship with methane concentration:

Predicted growth rate = β₀ + β₁ × X + β₂ × X²

where X is methane concentration.

This model does not include substrate temperature and pools observations from the two experimental series.

Its fitted relationship should not be interpreted as an isolated physical methane effect.

### 5.3 Thickness Estimation

Illustrative diamond thickness is estimated as:

Estimated thickness = Predicted growth rate × Deposition duration

This calculation assumes that the predicted growth rate remains constant throughout deposition.

It does not account for transient reactor behaviour, changes in growth rate or experimentally measured thickness.

### 5.4 Scenario Comparison

The software evaluates combinations of methane concentration and substrate temperature within specified demonstration bounds.

It identifies the highest non-negative linear-model prediction among the evaluated combinations.

This represents a comparison of mathematical model outputs, not an experimentally verified optimum or recommended reactor setting.

## 6. Model Evaluation

Model performance was assessed using in-sample fitting metrics and leave-one-out cross-validation (LOOCV).

### 6.1 In-Sample Results

| Model | MAE (µm/h) | RMSE (µm/h) | R² |
|---|---:|---:|---:|
| Multiple linear regression | 0.8890 | 1.0164 | 0.4117 |
| Quadratic methane regression | 0.6743 | 0.7992 | 0.6363 |

The quadratic model achieves lower in-sample errors on these six observations.

However, these results describe fit to the data used to estimate the models.

### 6.2 Leave-One-Out Cross-Validation

| Model | LOOCV MAE (µm/h) | LOOCV RMSE (µm/h) | LOOCV R² |
|---|---:|---:|---:|
| Multiple linear regression | 1.6663 | 1.8040 | -0.8534 |
| Quadratic methane regression | 1.3012 | 1.5232 | -0.3212 |

Both models produce negative cross-validated R² values.

This indicates poor held-out predictive performance relative to a simple baseline under this evaluation procedure.

The quadratic model performs better on the reported metrics, but neither model has demonstrated reliable generalisation.

Given the very small dataset and incomplete reactor-condition information, these findings should be treated as preliminary.

The evaluation can be reproduced using:

```bash
python tests/model_results_check.py
```

## 7. Interactive Application

The Streamlit prototype provides:

- Adjustable methane concentration
- Adjustable substrate temperature
- Adjustable deposition duration
- Linear regression growth-rate predictions
- Quadratic methane regression predictions
- Illustrative thickness estimates
- Scientific visualisations
- Exploratory scenario comparison
- Warnings about model limitations and unvalidated outputs

The application is intended for educational research and software demonstration.

It must not be used to select real MPCVD operating conditions.

## 8. Scientific Figures

The project generates three primary figures:

**Figure 1 — Experimental MPCVD Growth Rates**

`results/figure_1_experimental_growth.png`

Displays the six reported observations, grouped by temperature series.

**Figure 2 — Observed vs Fitted Diamond Growth Rates**

`results/figure_2_model_comparison.png`

Compares observed growth rates with in-sample fitted values from both regression models.

**Figure 3 — Illustrative Predicted Diamond Thickness**

`results/figure_3_predicted_thickness.png`

Shows estimated thickness against deposition duration under constant predicted growth rate.

Figures can be regenerated using:

```bash
python src/plot_experimental_data.py
python src/plot_model_comparison.py
python src/plot_predicted_thickness.py
```

## 9. Project Structure

```text
diamond-growth-optimisation/
├── data/
│   ├── DATASET_README.md
│   └── mpcvd_experimental_data_v01.csv
├── notebooks/
│   └── 01_exploratory_analysis.ipynb
├── results/
│   ├── figure_1_experimental_growth.png
│   ├── figure_2_model_comparison.png
│   ├── figure_3_predicted_thickness.png
│   └── linear_regression_results.csv
├── src/
│   ├── app.py
│   ├── model.py
│   ├── plot_experimental_data.py
│   ├── plot_model_comparison.py
│   └── plot_predicted_thickness.py
├── tests/
│   ├── model_results_check.py
│   ├── reproducibility_check.py
│   └── test_model.py
├── .gitignore
├── README.md
└── requirements.txt
```

The structure above shows the principal project files and excludes local development files and backups.

## 10. Installation and Usage

### 10.1 Clone or Open the Project

Clone the repository from GitHub after publication, or open the existing project directory in Visual Studio Code.

### 10.2 Create a Virtual Environment

```bash
python3 -m venv .venv
```

Activate on macOS or Linux:

```bash
source .venv/bin/activate
```

### 10.3 Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 10.4 Run the Streamlit Application

```bash
python -m streamlit run src/app.py
```

Open the local URL displayed in the terminal.

### 10.5 Run the Jupyter Notebook

```bash
python -m jupyter notebook
```

Open `notebooks/01_exploratory_analysis.ipynb`.

## 11. Testing and Reproducibility

### 11.1 Automated Tests

Run:

```bash
python -m pytest tests/test_model.py -v
```

At the latest verified test run, all **19 automated tests passed**.

These tests examine software behaviour, including data loading, model functions, thickness calculations, scenario exploration and input validation.

Passing software tests does not establish experimental predictive accuracy.

### 11.2 Reproducibility Check

Run:

```bash
python tests/reproducibility_check.py
```

The reference inputs are:

- Methane concentration: 20%
- Substrate temperature: 800°C
- Deposition duration: 5 hours

The resulting outputs are:

| Output | Value |
|---|---:|
| Linear predicted growth rate | 1.762 µm/h |
| Estimated thickness | 8.810 µm |
| Quadratic predicted growth rate | 3.230 µm/h |

The reproducibility script has been executed successfully with all assertions passing.

These results establish consistency of the implemented calculations with the provisional dataset and fitted models.

They do not establish agreement with new experimental observations.

### 11.3 Environment Reproducibility

Dependencies are listed in `requirements.txt`.

The dependency versions are not currently pinned, so exact reproduction across different computing environments is not guaranteed.

## 12. Scientific Limitations

The current project has important limitations:

1. Only six selected experimental observations are available.
2. Reactor conditions are incompletely represented.
3. Pressure and microwave power are omitted from the regression predictors.
4. Temperature is confounded with other differences between experimental series.
5. The quadratic model pools observations across different reactor conditions.
6. Both models show poor held-out performance under LOOCV.
7. Regression outputs may not represent physically achievable growth conditions.
8. Constant-rate thickness estimates are not experimentally validated.
9. No validated diamond-quality, energy-consumption or manufacturing-cost model has been developed.
10. The scenario-comparison feature does not establish a physically meaningful optimum.

The prototype must not be used for real reactor control, process design or operational recommendations.

## 13. Future Development

Potential future improvements include:

1. Expanding the experimental dataset using documented primary sources.
2. Incorporating reactor pressure, microwave power and additional process variables.
3. Distinguishing between experimental systems and reactor configurations.
4. Investigating more appropriate modelling approaches for larger datasets.
5. Quantifying prediction uncertainty.
6. Introducing scientifically justified physical constraints.
7. Exploring diamond quality, energy consumption and manufacturing costs when suitable data become available.
8. Improving environment reproducibility through tested dependency versions.
9. Validating predictions against independent experimental observations.

## 14. Project Significance

This independent project demonstrates the integration of mathematical modelling, scientific data analysis, Python programming and materials-engineering research.

It provides a foundation for further investigation into computational methods for synthetic diamond manufacturing.

Its principal contribution at this stage is an exploratory, documented and tested modelling workflow rather than a validated diamond-growth optimisation system.

---

**Project type:** Independent research and software-development portfolio project

**Development status:** Version 0.1 — Exploratory prototype
