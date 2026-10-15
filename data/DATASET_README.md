# MPCVD Diamond Growth — Dataset Documentation

## 1. Dataset Overview

**Filename:** mpcvd_experimental_data_v01.csv

**Project:** Predictive Modelling and Optimisation of Microwave Plasma CVD Diamond Growth Using Experimental Data

**Dataset status:** Provisional, unverified demonstration dataset

**Number of observations:** 6

The dataset contains illustrative records of methane concentration, substrate temperature and diamond growth rate.

It is used to demonstrate data handling, regression modelling and scientific visualisation.

The dataset must not be described as a verified experimental dataset until its values and associated conditions have been checked against the primary scientific source.

## 2. Dataset Variables

| Variable | Description | Unit |
|---|---|---|
| observation_id | Identifier for each record | None |
| temperature_c | Substrate temperature | °C |
| methane_pct | Methane concentration | % |
| growth_rate_um_h | Diamond growth rate | µm/h |
| series_id | Provisional grouping identifier | None |

## 3. Potential Scientific Source

Martyanov et al. (2023).

*Synthesis of Polycrystalline Diamond Films in Microwave Plasma at Ultrahigh Concentrations of Methane.*

Coatings, 13(4), 751.

https://www.mdpi.com/2079-6412/13/4/751

This publication is a candidate primary source for verifying the dataset.

The six records have not yet been confirmed as accurate extractions from the publication.

## 4. Data Preparation

The dataset is stored in CSV format and loaded into Python using pandas.

The following predictors are currently used in multiple linear regression:

- Methane concentration
- Substrate temperature

The response variable is diamond growth rate.

A separate exploratory quadratic regression model uses methane concentration only.

## 5. Known Limitations

The dataset has several important limitations:

- Only six provisional observations are available.
- Values have not been independently verified.
- Reactor pressure and microwave power are not adequately documented.
- Experimental conditions may differ between observations.
- The dataset may not represent a consistent experimental design.
- The small sample size limits model reliability.
- The available information is insufficient for validated process optimisation.

## 6. Intended Use

The dataset is intended for:

- Python programming practice
- Exploratory data analysis
- Demonstrating regression techniques
- Testing software functions
- Developing an interactive engineering prototype

It is not intended for selecting real MPCVD reactor operating conditions.

## 7. Future Verification

Before using the dataset for scientific conclusions:

1. Inspect the original publication.
2. Identify the relevant figures and tables.
3. Verify each numerical observation.
4. Confirm the units and experimental conditions.
5. Record the source location of each observation.
6. Correct or replace any unsupported records.
7. Expand the dataset where reliable measurements are available.

## 8. Data Integrity Statement

The current records are provisional and have not been independently validated.

Predictions derived from this dataset are illustrative mathematical outputs rather than experimentally established growth-rate estimates.