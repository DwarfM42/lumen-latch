"""Behavioral tests for the cascadable optical-cell simulator."""

import csv
import hashlib
import subprocess
import sys
from pathlib import Path

import pytest

from simulate_optical_cell import estimate_error_rate, propagate_power


def test_propagate_power_passive_chain_decays_geometrically():
    powers = propagate_power(
        initial_power_mw=1.0,
        stages=3,
        strategy="passive",
        insertion_loss_db=1.0,
        link_loss_db=2.0,
        fanout=1,
        gain=1.0,
    )

    assert powers == pytest.approx([1.0, 10 ** (-3 / 10), 10 ** (-6 / 10), 10 ** (-9 / 10)])


def test_propagate_power_each_stage_restores_nominal_level():
    powers = propagate_power(1.0, 4, "each-stage", 1.0, 2.0, fanout=1, gain=4.0)
    assert powers[1:] == pytest.approx([1.0] * 4)


def test_propagate_power_periodic_regeneration_restores_every_n_stages():
    powers = propagate_power(1.0, 4, "periodic", 1.0, 0.0, fanout=1, gain=1.0, regeneration_interval=2)
    attenuation = 10 ** (-1 / 10)
    assert powers == pytest.approx([1.0, attenuation, 1.0, attenuation, 1.0])


def test_error_estimate_is_reproducible_for_fixed_seed():
    kwargs = dict(stages=16, strategy="periodic", seed=123, trials=4000, temperature_c=25.0, threshold_cv=0.05)
    assert estimate_error_rate(**kwargs) == estimate_error_rate(**kwargs)


def test_temperature_stress_increases_error_rate():
    base = estimate_error_rate(stages=32, strategy="passive", seed=7, trials=8000, temperature_c=25.0, threshold_cv=0.05)
    hot = estimate_error_rate(stages=32, strategy="passive", seed=7, trials=8000, temperature_c=70.0, threshold_cv=0.05)
    assert hot > base


def test_threshold_variation_increases_error_rate():
    base = estimate_error_rate(stages=32, strategy="passive", seed=11, trials=8000, temperature_c=25.0, threshold_cv=0.01)
    varied = estimate_error_rate(stages=32, strategy="passive", seed=11, trials=8000, temperature_c=25.0, threshold_cv=0.15)
    assert varied > base


EXPECTED_FIGURES = {
    "stages_vs_power.png",
    "stages_vs_error_rate.png",
    "insertion_loss_vs_max_stages.png",
    "extinction_ratio_vs_max_stages.png",
    "fanout_vs_max_stages.png",
    "temperature_vs_error_rate.png",
    "variation_vs_error_rate.png",
    "regenerator_interval_vs_total_energy.png",
}

def test_cli_generates_reproducible_csv_and_exactly_eight_nonempty_pngs(tmp_path):
    script = Path(__file__).parents[1] / "simulate_optical_cell.py"
    command = [sys.executable, str(script), "--output-dir", str(tmp_path), "--seed", "20260715", "--trials", "1200"]
    subprocess.run(command, check=True)
    csv_path = tmp_path / "simulation_results.csv"
    first_hash = hashlib.sha256(csv_path.read_bytes()).hexdigest()
    with csv_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    required = {
        "strategy", "stages", "optical_power_mw", "total_loss_db",
        "extinction_ratio_db", "fanout", "gain", "gain_noise_db",
        "temperature_c", "threshold_cv", "retention_hours",
        "read_disturb_rate", "write_error_rate", "regeneration_interval",
        "error_rate", "q_factor", "total_energy_pj", "seed",
    }
    assert len(rows) >= 100
    assert required <= set(rows[0])
    figures = {item.name for item in (tmp_path / "figures").glob("*.png")}
    assert figures == EXPECTED_FIGURES
    assert all((tmp_path / "figures" / name).stat().st_size > 0 for name in figures)
    subprocess.run(command, check=True)
    assert hashlib.sha256(csv_path.read_bytes()).hexdigest() == first_hash
