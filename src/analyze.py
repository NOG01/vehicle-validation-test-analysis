"""
analyze.py
----------
Loads vehicle test data, calculates statistics, detects critical events,
generates plots, and writes an engineering summary report.

Workflow:
  1. Load CSV files from the data/ folder
  2. Merge all datasets into one DataFrame
  3. Calculate basic statistics
  4. Detect critical events (overheating / high fuel consumption)
  5. Generate and save plots
  6. Write a plain-text summary report
"""

import os
import glob
import pandas as pd
import matplotlib.pyplot as plt

# ── Paths ─────────────────────────────────────────────────────────────────────
DATA_FOLDER    = "data"
IMAGES_FOLDER  = "images"
REPORTS_FOLDER = "reports"

# ── Thresholds for critical event detection ───────────────────────────────────
ENGINE_TEMP_LIMIT = 105   # °C
BRAKE_TEMP_LIMIT  = 180   # °C
FUEL_RATE_LIMIT   = 15    # L/h


# =============================================================================
# STEP 1 & 2 – Load and merge data
# =============================================================================

def load_all_csv_files(folder):
    """Find and load every CSV file in the given folder."""
    csv_files = glob.glob(os.path.join(folder, "*.csv"))

    if not csv_files:
        print(f"[ERROR] No CSV files found in '{folder}'. Run generate_data.py first.")
        exit(1)

    dataframes = []
    for filepath in sorted(csv_files):
        df = pd.read_csv(filepath)
        # Keep track of which file each row came from
        df["source_file"] = os.path.basename(filepath)
        dataframes.append(df)
        print(f"  Loaded: {filepath}  ({len(df)} rows)")

    return dataframes


def merge_dataframes(dataframes):
    """Combine all DataFrames into a single one."""
    combined = pd.concat(dataframes, ignore_index=True)
    print(f"\n  Total rows after merge: {len(combined)}\n")
    return combined


# =============================================================================
# STEP 3 – Calculate statistics
# =============================================================================

def calculate_statistics(df):
    """Calculate and display basic descriptive statistics."""

    avg_speed        = df["speed_kmh"].mean()
    max_speed        = df["speed_kmh"].max()

    avg_engine_temp  = df["engine_temp"].mean()
    max_engine_temp  = df["engine_temp"].max()

    avg_brake_temp   = df["brake_temp"].mean()
    max_brake_temp   = df["brake_temp"].max()

    avg_fuel_rate    = df["fuel_rate"].mean()

    stats = {
        "avg_speed":       round(avg_speed, 1),
        "max_speed":       round(max_speed, 1),
        "avg_engine_temp": round(avg_engine_temp, 1),
        "max_engine_temp": round(max_engine_temp, 1),
        "avg_brake_temp":  round(avg_brake_temp, 1),
        "max_brake_temp":  round(max_brake_temp, 1),
        "avg_fuel_rate":   round(avg_fuel_rate, 2),
    }

    print("=" * 45)
    print("VEHICLE TEST STATISTICS")
    print("=" * 45)
    print(f"  Average Speed          : {stats['avg_speed']} km/h")
    print(f"  Maximum Speed          : {stats['max_speed']} km/h")
    print(f"  Average Engine Temp    : {stats['avg_engine_temp']} °C")
    print(f"  Maximum Engine Temp    : {stats['max_engine_temp']} °C")
    print(f"  Average Brake Temp     : {stats['avg_brake_temp']} °C")
    print(f"  Maximum Brake Temp     : {stats['max_brake_temp']} °C")
    print(f"  Average Fuel Rate      : {stats['avg_fuel_rate']} L/h")
    print("=" * 45)

    return stats


# =============================================================================
# STEP 4 – Detect critical events
# =============================================================================

def detect_critical_events(df):
    """Count rows where readings exceed defined safety thresholds."""

    engine_overheat_count  = int((df["engine_temp"] > ENGINE_TEMP_LIMIT).sum())
    brake_overheat_count   = int((df["brake_temp"]  > BRAKE_TEMP_LIMIT).sum())
    high_fuel_count        = int((df["fuel_rate"]   > FUEL_RATE_LIMIT).sum())

    events = {
        "engine_overheat": engine_overheat_count,
        "brake_overheat":  brake_overheat_count,
        "high_fuel":       high_fuel_count,
    }

    print("\nCRITICAL EVENTS DETECTED")
    print("-" * 45)
    print(f"  Engine Overheating  (>{ENGINE_TEMP_LIMIT} °C)  : {engine_overheat_count} event(s)")
    print(f"  Brake Overheating   (>{BRAKE_TEMP_LIMIT} °C) : {brake_overheat_count} event(s)")
    print(f"  High Fuel Rate      (>{FUEL_RATE_LIMIT} L/h)   : {high_fuel_count} event(s)")
    print("-" * 45)

    return events


# =============================================================================
# STEP 5 – Generate plots
# =============================================================================

def save_speed_plot(df, output_path):
    """Plot vehicle speed over time."""
    fig, ax = plt.subplots(figsize=(10, 4))

    ax.plot(df.index, df["speed_kmh"], color="steelblue", linewidth=1)
    ax.set_title("Vehicle Speed Over Time")
    ax.set_xlabel("Sample Index")
    ax.set_ylabel("Speed (km/h)")
    ax.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"  Saved plot: {output_path}")


def save_engine_temp_plot(df, output_path):
    """Plot engine temperature over time with overheating threshold line."""
    fig, ax = plt.subplots(figsize=(10, 4))

    ax.plot(df.index, df["engine_temp"], color="firebrick", linewidth=1)
    ax.axhline(y=ENGINE_TEMP_LIMIT, color="orange", linestyle="--", linewidth=1.2,
               label=f"Overheat Limit ({ENGINE_TEMP_LIMIT} °C)")
    ax.set_title("Engine Temperature Over Time")
    ax.set_xlabel("Sample Index")
    ax.set_ylabel("Engine Temperature (°C)")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"  Saved plot: {output_path}")


def save_brake_temp_plot(df, output_path):
    """Plot brake temperature over time with overheating threshold line."""
    fig, ax = plt.subplots(figsize=(10, 4))

    ax.plot(df.index, df["brake_temp"], color="darkorange", linewidth=1)
    ax.axhline(y=BRAKE_TEMP_LIMIT, color="red", linestyle="--", linewidth=1.2,
               label=f"Overheat Limit ({BRAKE_TEMP_LIMIT} °C)")
    ax.set_title("Brake Temperature Over Time")
    ax.set_xlabel("Sample Index")
    ax.set_ylabel("Brake Temperature (°C)")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"  Saved plot: {output_path}")


def generate_all_plots(df):
    """Create output folder and save all plots."""
    os.makedirs(IMAGES_FOLDER, exist_ok=True)

    print("\nGenerating plots...")
    save_speed_plot(df,       os.path.join(IMAGES_FOLDER, "vehicle_speed.png"))
    save_engine_temp_plot(df, os.path.join(IMAGES_FOLDER, "engine_temperature.png"))
    save_brake_temp_plot(df,  os.path.join(IMAGES_FOLDER, "brake_temperature.png"))


# =============================================================================
# STEP 6 – Generate report
# =============================================================================

def write_report(stats, events):
    """Write a plain-text engineering summary to reports/test_summary.txt."""
    os.makedirs(REPORTS_FOLDER, exist_ok=True)
    report_path = os.path.join(REPORTS_FOLDER, "test_summary.txt")

    lines = [
        "VEHICLE TEST SUMMARY",
        "=" * 45,
        "",
        f"Average Speed              : {stats['avg_speed']} km/h",
        f"Maximum Speed              : {stats['max_speed']} km/h",
        "",
        f"Average Engine Temperature : {stats['avg_engine_temp']} °C",
        f"Maximum Engine Temperature : {stats['max_engine_temp']} °C",
        "",
        f"Average Brake Temperature  : {stats['avg_brake_temp']} °C",
        f"Maximum Brake Temperature  : {stats['max_brake_temp']} °C",
        "",
        f"Average Fuel Consumption   : {stats['avg_fuel_rate']} L/h",
        "",
        "=" * 45,
        "CRITICAL EVENTS",
        "=" * 45,
        "",
        f"Critical Engine Temperature Events : {events['engine_overheat']}",
        f"Critical Brake Temperature Events  : {events['brake_overheat']}",
        f"High Fuel Consumption Events       : {events['high_fuel']}",
        "",
        "=" * 45,
        "CONCLUSION",
        "=" * 45,
        "",
        "The vehicle operated within normal conditions for most of the test period.",
        "",
        "A small number of overheating and high fuel consumption events were detected.",
        "",
        "Further investigation is recommended to determine the root causes of these events.",
        "",
    ]

    with open(report_path, "w") as f:
        f.write("\n".join(lines))

    print(f"\n  Report saved: {report_path}")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":

    print("\n── Loading data ──────────────────────────────────\n")
    dataframes = load_all_csv_files(DATA_FOLDER)
    df         = merge_dataframes(dataframes)

    print("\n── Calculating statistics ────────────────────────\n")
    stats = calculate_statistics(df)

    print("\n── Detecting critical events ─────────────────────\n")
    events = detect_critical_events(df)

    print("\n── Generating visualizations ─────────────────────")
    generate_all_plots(df)

    print("\n── Writing report ────────────────────────────────")
    write_report(stats, events)

    print("\n✓ Analysis complete.\n")
