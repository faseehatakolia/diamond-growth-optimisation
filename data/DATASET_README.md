# MPCVD Diamond Growth — Dataset Documentation

## 1. Dataset Overview

**Filename:** `mpcvd_experimental_data_v01.csv`

**Project:** Predictive Modelling and Optimisation of Microwave Plasma CVD Diamond Growth Using Experimental Data

**Dataset status:** Source-traceable, limited experimental dataset. Independent scientific validation of the predictive models remains outstanding.

**Number of observations:** 6

This dataset contains six selected diamond growth-rate observations attributed to Martyanov et al. (2023).

The records include methane concentration, substrate temperature and diamond growth rate. They are used to demonstrate experimental data handling, exploratory regression modelling, mathematical analysis and scientific visualisation.

Although the numerical values have been identified from the primary publication, the dataset represents only a small selection of the reported experimental results and does not fully capture the reactor operating conditions.

Consequently, the dataset supports the development of an exploratory computational prototype rather than a scientifically validated diamond-growth optimisation system.

## 2. Dataset Variables

| Variable | Description | Unit |
|---|---|---|
| `observation_id` | Unique identifier for each observation | None |
| `temperature_c` | Reported substrate temperature | °C |
| `methane_pct` | Reported methane concentration | % |
| `growth_rate_um_h` | Reported diamond growth rate | µm/h |
| `series_id` | Identifier for the experimental series | None |

The variables `methane_pct` and `temperature_c` are used as predictors in the multiple linear regression model.

The variable `growth_rate_um_h` is the response variable.

The variable `series_id` identifies the experimental series but is not currently included as a model predictor.

## 3. Scientific Source and Dataset Provenance

**Primary source:**

Martyanov et al. (2023).

*Synthesis of Polycrystalline Diamond Films in Microwave Plasma at Ultrahigh Concentrations of Methane.*

*Coatings*, 13(4), 751.

DOI: https://doi.org/10.3390/coatings13040751

### Dataset provenance and verification status

The dataset contains six selected growth-rate observations associated with Section 3.3 and Figure 4(b) of Martyanov et al. (2023).

The selected numerical values were identified from the published article and associated experimental results. Their correspondence with the original experimental conditions should be verified before further scientific use.

The selected observations are:

| Temperature (°C) | Methane (%) | Growth rate (µm/h) |
|---|---|---|
| 800 | 4 | 0.60 |
| 800 | 20 | 3.41 |
| 800 | 100 | 0.60 |
| 900 | 3 | 2.80 |
| 900 | 40 | 4.10 |
| 900 | 100 | 2.10 |

These observations represent a small, selected subset of the published experimental results rather than a complete experimental dataset.

Importantly, the two temperature series involved different reactor operating conditions, including changes in reactor pressure and microwave power.

These additional experimental variables are not fully represented in the current CSV.

Therefore, differences in observed growth rates between the two temperature series cannot be attributed solely to substrate temperature.

The dataset is source-traceable but limited in experimental scope. It is suitable for demonstrating exploratory regression techniques, not for establishing reliable reactor optimisation or independently validated growth-rate predictions.

## 4. Data Preparation and Modelling

The dataset is stored in CSV format and loaded into Python using the pandas library.

### Multiple linear regression

The multiple linear regression model uses:

- Methane concentration (%)
- Substrate temperature (°C)

The response variable is diamond growth rate (µm/h).

The model estimates a linear relationship between the two predictors and the observed growth rates.

### Quadratic methane regression

A separate exploratory quadratic regression model uses methane concentration as its only predictor.

The quadratic model includes a squared methane-concentration term to investigate possible non-linear behaviour in the selected observations.

Because the quadratic model does not explicitly account for substrate temperature or other reactor operating conditions, its predictions should not be interpreted as a complete physical representation of MPCVD diamond growth.

Both models are fitted using the six selected observations.

Their reported performance metrics describe their fit to the available dataset and do not establish predictive reliability on independent experimental data.

## 5. Known Limitations

The dataset has several important limitations:

- Only six selected experimental observations are included.
- The dataset does not contain the complete published experimental results.
- Reactor pressure and microwave power are not included as model predictors.
- Experimental operating conditions differ between the two temperature series.
- The small sample size limits statistical reliability and model generalisation.
- The quadratic regression model does not explicitly account for temperature.
- The regression models have not undergone independent experimental validation.
- The observations are insufficient for reliable industrial process optimisation.
- Predictions outside the observed predictor ranges, or for reactor conditions not adequately represented in the dataset, may be unreliable or physically unrealistic.
- The dataset does not provide sufficient information to assess diamond quality, defects, energy consumption or production costs.

These limitations must be considered when interpreting model predictions, comparing regression performance and discussing potential engineering applications.

## 6. Intended Use

The dataset is intended for:

- Exploratory data analysis
- Demonstrating regression modelling techniques
- Testing and verifying software functions
- Developing an interactive engineering prototype
- Investigating mathematical relationships between selected variables
- Producing scientific visualisations
- Supporting computational reproducibility
- Identifying limitations and opportunities for further research

The dataset is not intended for selecting real MPCVD reactor operating conditions or making validated predictions of industrial diamond-growth performance.

The software should be regarded as an exploratory computational demonstration.

## 7. Future Research and Validation

Before using the models to support stronger scientific conclusions, further work would be required.

1. Independently verify the local CSV values against the original publication and associated experimental results.
2. Document the corresponding experimental conditions, particularly reactor pressure and microwave power.
3. Review the original experimental methodology, figures and measurement procedures.
4. Expand the dataset using additional reliable experimental observations.
5. Investigate additional process variables, including gas composition, substrate characteristics and deposition time.
6. Compare alternative regression and machine-learning approaches using a sufficiently large dataset.
7. Evaluate prediction uncertainty, model sensitivity and out-of-sample prediction errors.
8. Investigate relationships between growth rate and diamond quality.
9. Perform independent experimental validation when suitable data become available.
10. Assess whether a more comprehensive model could support scientifically justified process optimisation.

These developments would be necessary before considering practical engineering recommendations.

## 8. Data Integrity Statement

The six selected numerical observations are attributed to experimental results reported by Martyanov et al. (2023).

However, the dataset is small, represents only a subset of the published observations and does not fully describe the corresponding reactor operating conditions.

The regression models developed using this dataset provide exploratory mathematical estimates rather than independently validated predictions of diamond-growth behaviour.

Model performance should therefore be interpreted within the limitations of the available observations.

**The software prototype must not be interpreted as a validated industrial diamond-growth optimisation system or used to determine real reactor operating conditions without further experimental evidence.**