# Vehicle Validation Test Analysis

A data analysis project that simulates a simplified automotive validation workflow.

---

## Project Overview

During vehicle development, engineering teams collect operational data from road tests to verify that all systems perform within safe limits. This project simulates that process by generating realistic test data, analyzing it with Python, detecting abnormal operating conditions, and producing a plain-text engineering report.

The workflow is similar to what a junior validation engineer might perform when reviewing data collected from a test vehicle.

---

## Objectives

- Analyze vehicle test data collected from road sessions
- Detect abnormal operating conditions (overheating, high fuel consumption)
- Generate a clear engineering summary report
- Visualize key parameters over the test period

---

## Features

- **CSV Data Processing** – Loads and merges multiple test run files automatically
- **Statistical Analysis** – Calculates averages and maximum values for key parameters
- **Critical Event Detection** – Flags readings that exceed defined safety thresholds
- **Automated Report Generation** – Writes a plain-text summary to `reports/test_summary.txt`
- **Data Visualization** – Saves time-series plots for speed, engine temperature, and brake temperature

---

## Technologies

| Tool       | Purpose                        |
|------------|-------------------------------|
| Python 3   | Core scripting language        |
| Pandas     | Data loading and analysis      |
| Matplotlib | Plot generation                |
| NumPy      | Numerical support (optional)   |

---

## Repository Structure

```
vehicle-validation-test-analysis/
│
├── data/                    # Raw CSV test files
│   ├── test_run_01.csv
│   └── test_run_02.csv
│
├── src/                     # Python scripts
│   ├── generate_data.py     # Generates simulated test data
│   └── analyze.py           # Main analysis script
│
├── reports/                 # Auto-generated text report
│   └── test_summary.txt
│
├── images/                  # Auto-generated plots
│   ├── vehicle_speed.png
│   ├── engine_temperature.png
│   └── brake_temperature.png
│
├── requirements.txt         # Python dependencies
└── README.md
```

---

## Installation

Clone the repository and install the required dependencies:

```bash
git clone https://github.com/nog01/vehicle-validation-test-analysis.git
cd vehicle-validation-test-analysis
pip install -r requirements.txt
```

---

## Generate Sample Data

Run the data generation script to create the two CSV test files:

```bash
python src/generate_data.py
```

This will generate `data/test_run_01.csv` and `data/test_run_02.csv`, each containing approximately 300 rows of simulated vehicle data.

---

## Run Analysis

Run the main analysis script:

```bash
python src/analyze.py
```

The script will:
1. Load and merge all CSV files from the `data/` folder
2. Calculate and display descriptive statistics
3. Detect and count critical events
4. Save plots to the `images/` folder
5. Write the summary report to `reports/test_summary.txt`

---

## Example Console Output

```
── Loading data ──────────────────────────────────

  Loaded: data/test_run_01.csv  (300 rows)
  Loaded: data/test_run_02.csv  (300 rows)

  Total rows after merge: 600

── Calculating statistics ────────────────────────

=============================================
VEHICLE TEST STATISTICS
=============================================
  Average Speed          : 72.4 km/h
  Maximum Speed          : 130.0 km/h
  Average Engine Temp    : 87.6 °C
  Maximum Engine Temp    : 113.2 °C
  Average Brake Temp     : 68.3 °C
  Maximum Brake Temp     : 207.4 °C
  Average Fuel Rate      : 7.91 L/h
=============================================

CRITICAL EVENTS DETECTED
---------------------------------------------
  Engine Overheating  (>105 °C)  : 3 event(s)
  Brake Overheating   (>180 °C)  : 2 event(s)
  High Fuel Rate      (>15 L/h)  : 4 event(s)
---------------------------------------------

── Generating visualizations ─────────────────────
  Saved plot: images/vehicle_speed.png
  Saved plot: images/engine_temperature.png
  Saved plot: images/brake_temperature.png

── Writing report ────────────────────────────────
  Report saved: reports/test_summary.txt

✓ Analysis complete.
```

---

## Example Report (`reports/test_summary.txt`)

```
VEHICLE TEST SUMMARY
=============================================

Average Speed              : 72.4 km/h
Maximum Speed              : 130.0 km/h

Average Engine Temperature : 87.6 °C
Maximum Engine Temperature : 113.2 °C

Average Brake Temperature  : 68.3 °C
Maximum Brake Temperature  : 207.4 °C

Average Fuel Consumption   : 7.91 L/h

=============================================
CRITICAL EVENTS
=============================================

Critical Engine Temperature Events : 3
Critical Brake Temperature Events  : 2
High Fuel Consumption Events       : 4

=============================================
CONCLUSION
=============================================

The vehicle operated within normal conditions for most of the test period.

A small number of overheating and high fuel consumption events were detected.

Further investigation is recommended to determine the root causes of these events.
```

---
