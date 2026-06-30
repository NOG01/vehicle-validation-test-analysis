"""
generate_data.py
----------------
Generates two simulated vehicle test run CSV files.
Each file contains approximately 300 rows of realistic vehicle data.

A small number of intentional abnormal events are included:
  - Engine overheating   : engine_temp > 105
  - Brake overheating    : brake_temp  > 180
  - High fuel consumption: fuel_rate   > 15
"""

import os
import random
import csv

# ── Output folder ────────────────────────────────────────────────────────────
DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)

# ── Column names ─────────────────────────────────────────────────────────────
COLUMNS = ["time", "speed_kmh", "engine_temp", "fuel_rate", "brake_temp"]


def build_speed_profile(num_rows):
    """Create a smooth speed profile for the entire test run."""
    speeds = []
    speed = 0.0

    for t in range(num_rows):
        if t < 20:
            speed = min(speed + random.uniform(3, 6), 60)
        elif t < 60:
            speed += random.uniform(-4, 4)
            speed = max(20, min(speed, 80))
        elif t < 180:
            speed += random.uniform(-3, 3)
            speed = max(80, min(speed, 130))
        elif t < 240:
            speed += random.uniform(-6, 5)
            speed = max(30, min(speed, 110))
        else:
            speed = max(0, speed - random.uniform(2, 5))
        speeds.append(round(speed, 1))

    return speeds


def generate_test_run(filename, num_rows=300, anomaly_seed=None):
    """Generate one CSV file simulating a vehicle test run."""

    random.seed(anomaly_seed)

    # Decide which rows will contain anomalies (only a small number)
    engine_overheat_rows = set(random.sample(range(80, num_rows - 10), 3))
    brake_overheat_rows  = set(random.sample(range(100, num_rows - 10), 2))
    high_fuel_rows       = set(random.sample(range(50, num_rows - 10), 4))

    speeds = build_speed_profile(num_rows)
    rows   = []

    for t in range(num_rows):
        speed = speeds[t]

        # ── Engine temperature ────────────────────────────────────────────
        # Normal range: 80–95 °C, rising slightly with speed
        engine_temp = 80 + (speed / 130) * 12 + random.uniform(-2, 2)

        # ── Fuel consumption ──────────────────────────────────────────────
        fuel_rate = 2.5 + (speed / 130) * 8 + random.uniform(-1, 1)
        fuel_rate = max(0.5, fuel_rate)

        # ── Brake temperature ─────────────────────────────────────────────
        # Brakes run warmer at high speed; base is near ambient
        brake_temp = 28 + (speed / 130) * 60 + random.uniform(-4, 4)

        # ── Inject anomalies ──────────────────────────────────────────────
        if t in engine_overheat_rows:
            engine_temp = random.uniform(106, 115)

        if t in brake_overheat_rows:
            brake_temp = random.uniform(182, 210)

        if t in high_fuel_rows:
            fuel_rate = random.uniform(15.5, 18.0)

        rows.append({
            "time":        t,
            "speed_kmh":   speed,
            "engine_temp": round(engine_temp, 1),
            "fuel_rate":   round(fuel_rate, 2),
            "brake_temp":  round(brake_temp, 1),
        })

    # ── Write CSV ─────────────────────────────────────────────────────────────
    filepath = os.path.join(DATA_FOLDER, filename)
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"[OK] Generated: {filepath}  ({num_rows} rows)")


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Generating test data files...\n")
    generate_test_run("test_run_01.csv", num_rows=300, anomaly_seed=42)
    generate_test_run("test_run_02.csv", num_rows=300, anomaly_seed=99)
    print("\nDone. CSV files are saved in the 'data/' folder.")
