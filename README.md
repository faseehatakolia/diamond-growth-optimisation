# Predictive Modelling and Optimisation of Microwave Plasma CVD Diamond Growth Using Experimental Data

**An independent computational materials-engineering research project**

**Status:** Version 0.1 — Exploratory prototype

**Technologies:** Python · scikit-learn · pandas · NumPy · Matplotlib · Streamlit · pytest

---

## 1. Project Overview

This project explores the application of mathematical modelling and Python-based computational methods to microwave plasma chemical vapour deposition (MPCVD) diamond growth.

The aim is to investigate how selected process variables may relate to diamond growth rate and to develop an interactive software prototype for exploring mathematical predictions.

The project combines materials-science research, regression modelling, scientific visualisation and software development.

The current implementation is an educational research prototype and is not a validated reactor optimisation system.

## 2. Research Motivation

Lab-grown diamonds have important applications in advanced engineering, including thermal management, electronics, optical technologies and industrial materials.

Microwave plasma chemical vapour deposition is a method of producing synthetic diamond through the deposition of carbon-containing species onto a substrate.

The growth process is influenced by several variables, including:

- Methane concentration
- Substrate temperature
- Reactor pressure
- Microwave power
- Gas composition
- Substrate and seed characteristics

Understanding the relationships between these variables and diamond growth is important for developing more reliable and efficient manufacturing processes.

This project investigates how computational modelling could contribute to that understanding.

## 3. Research Objectives

The project has five principal objectives:

1. Investigate the physical principles underlying MPCVD diamond growth.
2. Identify and organise relevant experimental growth data.
3. Develop mathematical models relating selected process variables to diamond growth rate.
4. Build an interactive application for exploring model predictions.
5. Evaluate model limitations and identify requirements for more rigorous scientific validation.

## 4. Mathematical Modelling

### 4.1 Multiple Linear Regression

The initial model uses methane concentration and substrate temperature as predictors.

**Predicted growth rate = β₀ + β₁(Methane concentration) + β₂(Substrate temperature)**

The coefficients are estimated using ordinary least squares.

### 4.2 Quadratic Regression

A second exploratory model includes a quadratic methane-concentration term.

**Predicted growth rate = β₀ + β₁X + β₂X²**

Here, X represents methane concentration.

The quadratic model does not include substrate temperature. Consequently, its predictions are not directly equivalent to those of the multiple linear regression model.

### 4.3 Thickness Estimation

An illustrative thickness estimate is calculated using:

**Estimated thickness = Predicted growth rate × Growth duration**

This assumes a constant growth rate throughout the deposition period.

## 5. Dataset

The current demonstration dataset contains six provisional observations representing methane concentration, substrate temperature and diamond growth rate.

The dataset is stored in:

`data/mpcvd_experimental_data_v01.csv`

The observations require verification against the original scientific literature before they can be treated as reliable experimental measurements.

**Potential source for verification:**

Martyanov et al. (2023), *Synthesis of Polycrystalline Diamond Films in Microwave Plasma at Ultrahigh Concentrations of Methane*.

https://www.mdpi.com/2079-6412/13/4/751

The current data should not be described as a verified extraction from this publication until the reported experimental values and conditions have been checked.

## 6. Software Features

The prototype includes:

- Loading and processing the demonstration dataset
- Multiple linear regression modelling
- Quadratic regression modelling
- Interactive methane-concentration and temperature inputs
- Growth-duration controls
- Illustrative growth-rate predictions
- Estimated deposited thickness
- Scientific visualisations
- Exploratory comparison of regression models
- Bounded scenario comparison
- Warnings about invalid or unvalidated predictions


## 7. Project Structure

```text
diamond-growth-optimisation/
├── data/
│   └── mpcvd_experimental_data_v01.csv
├── notebooks/
│   └── 01_exploratory_analysis.ipynb
├── results/
├── src/
│   ├── app.py
│   └── model.py
├── tests/
│   └── test_model.py
├── .gitignore
├── README.md
└── requirements.txt
```

## 8. Installation and Usage

### Clone the Repository

Once the repository has been published, clone it using its GitHub URL.

Alternatively, open the existing project folder in Visual Studio Code.

### Create a Virtual Environment

```bash
python3 -m venv .venv
```

Activate the environment on macOS or Linux:

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Run the Application

```bash
python -m streamlit run src/app.py
```

Streamlit will display the local application address in the terminal.

### Run Automated Tests

```bash
python -m pytest tests/ -v
```

At the current development stage, the five initial automated tests have passed.

These tests establish software consistency with the current implementation, not experimental predictive accuracy.

## 9. Exploratory Scenario Comparison

The application evaluates a grid of methane concentrations and substrate temperatures.

The initial grid contains 220 input combinations.

The scenario-comparison feature identifies the highest non-negative growth-rate prediction among those evaluated.

This is a mathematical comparison of model outputs, not an experimentally verified optimum.

The bounds used in the demonstration reflect the overall ranges of the provisional dataset and should not be interpreted as safe or recommended reactor operating conditions.

## 10. Scientific Limitations

The current prototype has several important limitations:

- Only six provisional observations are available.
- The dataset has not yet been fully verified against the primary source.
- Relevant process variables, including pressure and microwave power, are not adequately represented.
- Reactor conditions may differ between observations.
- The regression models have not been independently validated.
- The small dataset creates substantial risks of overfitting and misleading relationships.
- The scenario-comparison feature evaluates mathematical predictions rather than physical feasibility.
- No experimentally validated growth-quality, energy or cost optimisation has been implemented.

The software is intended for educational exploration and methodological development.

It must not be used to recommend real MPCVD reactor operating conditions.

## 11. Future Development

Future work will focus on:

1. Verifying the experimental data against primary scientific publications.
2. Expanding the dataset with documented reactor conditions.
3. Introducing suitable model evaluation and uncertainty analysis.
4. Investigating physically meaningful constraints.
5. Exploring growth-quality, energy and cost trade-offs where suitable data are available.
6. Improving software testing and reproducibility.

## 12. Project Significance

This project demonstrates an interdisciplinary approach combining mathematical modelling, Python programming and materials-engineering research.

It provides a foundation for further investigation of computational methods in synthetic diamond manufacturing while explicitly recognising the limitations of the current experimental evidence.

---

**Project type:** Independent research and software-development portfolio project

**Development status:** Exploratory prototype — Version 0.1
