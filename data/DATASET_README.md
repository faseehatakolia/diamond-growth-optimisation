# MPCVD Diamond Growth — Dataset Documentation

## 1. Dataset Overview

**Filename:** `mpcvd_experimental_data_v01.csv`

**Project:** Predictive Modelling and Optimisation of Microwave Plasma CVD Diamond Growth Using Experimental Data

**Dataset status:** Source-traceable, limited experimental dataset; scientific validation of the predictive model remains outstanding.

**Number of observations:** 6

The dataset contains six selected diamond growth-rate observations reported by Martyanov et al. (2023).

The records include methane concentration, substrate temperature and diamond growth rate.

The dataset is used to demonstrate data handling, regression modelling and scientific visualisation.

Although the reported numerical values have been identified in the primary publication, the dataset represents only a small selection of observations and does not fully capture the experimental conditions.

## 2. Dataset Variables

| Variable | Description | Unit |
|---|---|---|
| observation_id | Identifier for each record | None |
| temperature_c | Substrate temperature | °C |
| methane_pct | Methane concentration | % |
| growth_rate_um_h | Diamond growth rate | µm/h |
| series_id | Grouping identifier for the experimental series | None |

## 3. Scientific Source and Dataset Provenance

**Primary source:**

Martyanov et al. (2023).

*Synthesis of Polycrystalline Diamond Films in Microwave Plasma at Ultrahigh Concentrations of Methane.*

Coatings, 13(4), 751.

https://doi.org/10.3390/coatings13040751

### Dataset provenance and verification status

The dataset contains six selected growth-rate observations reported in Section 3.3 of Martyanov et al. (2023), associated with Figure 4(b).

The methane concentrations, substrate temperatures and growth rates have been cross-checked against the published article text.

The selected observations are:

| Temperature (°C) | Methane (%) | Growth rate (µm/h) |
|---|---|---|
| 800 | 4 | 0.60 |
| 800 | 20 | 3.41 |
| 800 | 100 | 0.60 |
| 900 | 3 | 2.80 |
| 900 | 40 | 4.10 |
| 900 | 100 | 2.10 |

These observations represent a small, selected subset of the published results rather than a complete experimental dataset.

The two temperature series involved different reactor operating conditions, including adjustments to pressure and microwave power. These conditions are not fully represented in the current CSV.

The dataset is therefore source-traceable but limited in experimental scope.

It is suitable for demonstrating exploratory regression methods, not for establishing reliable reactor optimisation or independently validated predictions.

## 4. Data Preparation

The dataset is stored in CSV format and loaded into Python using pandas.

The following predictors are currently used in multiple linear regression:

- Methane concentration
- Substrate temperature

The response variable is diamond growth rate.

A separate exploratory quadratic regression model uses methane concentration only.

## 5. Known Limitations

The dataset has several important limitations:

- Only six selected observations are available.
- The dataset does not contain the complete experimental results.
- Reactor pressure and microwave power are not included as model predictors.
- Experimental conditions differ between the temperature series.
- The small sample size limits statistical reliability.
- The model has not undergone independent experimental validation.
- The observations are insufficient for reliable process optimisation.
- Predictions outside the experimental conditions may be physically unrealistic.

## 6. Intended Use

The dataset is intended for:

- Exploratory data analysis
- Demonstrating regression techniques
- Testing software functions
- Developing an interactive engineering prototype
- Investigating mathematical relationships
- Supporting computational reproducibility

It is not intended for selecting real MPCVD reactor operating conditions.

## 7. Future Research and Validation

Before using the model for stronger scientific conclusions:

1. Confirm that the local CSV exactly matches the six published values.
2. Document the corresponding experimental conditions, including pressure and microwave power.
3. Review the original figures and experimental methodology.
4. Expand the dataset using additional reliable measurements.
5. Investigate the effects of additional process variables.
6. Compare alternative mathematical models.
7. Evaluate uncertainty and prediction errors.
8. Perform independent experimental validation where suitable data are available.

## 8. Data Integrity Statement

The six selected numerical observations are traceable to reported values in Martyanov et al. (2023).

However, the dataset is small and does not fully represent the experimental conditions.

Predictions derived from this dataset remain exploratory mathematical outputs rather than independently validated estimates of diamond growth behaviour.

The software prototype should not be interpreted as a validated industrial optimisation system.