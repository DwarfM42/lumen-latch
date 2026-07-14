"""13.4 pJ boundary to system-power TDD tests."""
import csv, hashlib, math, subprocess, sys
from pathlib import Path
import pytest
from system_energy_model import ACTIVITIES, CELL_COUNTS, FREQUENCIES_HZ, SCENARIOS, laser_electrical_energy_pj, power_budget_w, write_budget_csv

def test_laser_energy_closes_absorbed_pcm_boundary():
    assert laser_electrical_energy_pj(13.4,.8,.9,.95,.8,.3)==pytest.approx(13.4/(.8*.9*.95*.8*.3))

def test_efficiencies_must_be_finite_fractions():
    for bad in (0,-.1,1.1,math.nan,math.inf):
        with pytest.raises(ValueError): laser_electrical_energy_pj(13.4,bad,1,1,1,1)

def test_dynamic_and_static_power_are_separated():
    r=power_budget_w(100,1e6,1e3,.01,2,1e-6)
    assert r['dynamic_w']==pytest.approx(1e-3)
    assert r['static_w']==pytest.approx(2.001)
    assert r['total_w']==pytest.approx(2.002)

def test_csv_has_all_240_scenario_operating_points_and_finite_numbers(tmp_path):
    rows=list(csv.DictReader(write_budget_csv(tmp_path/'budget.csv').open(encoding='utf-8',newline='')))
    assert len(rows)==len(SCENARIOS)*len(FREQUENCIES_HZ)*len(CELL_COUNTS)*len(ACTIVITIES)==240
    assert {r['scenario'] for r in rows}==set(SCENARIOS)
    for r in rows:
        for c in ('frequency_hz','cells','activity','dynamic_w','static_w','total_w','dynamic_active_pj'):
            assert math.isfinite(float(r[c]))

def test_power_is_monotonic_in_frequency_cells_and_activity(tmp_path):
    rows=list(csv.DictReader(write_budget_csv(tmp_path/'b.csv').open(encoding='utf-8',newline='')))
    def d(f,n,a): return float(next(r for r in rows if r['scenario']=='optimistic_integrated' and float(r['frequency_hz'])==f and float(r['cells'])==n and float(r['activity'])==a)['dynamic_w'])
    assert d(1e9,1,1)>d(1e3,1,1)
    assert d(1e6,1e9,1)>d(1e6,1,1)
    assert d(1e6,1,1)>d(1e6,1,1e-4)

def test_unknown_zero_is_not_labeled_system_total(tmp_path):
    rows=list(csv.DictReader(write_budget_csv(tmp_path/'b.csv').open(encoding='utf-8',newline='')))
    r=next(x for x in rows if x['scenario']=='pcm_absorbed_floor')
    assert r['completeness']=='lower_bound_not_system_total'
    assert 'unknown' in r['unknown_components']

def test_cli_output_is_byte_reproducible(tmp_path):
    script=Path(__file__).parents[1]/'system_energy_model.py'; out=tmp_path/'b.csv'; cmd=[sys.executable,str(script),'--output',str(out)]
    subprocess.run(cmd,check=True); h=hashlib.sha256(out.read_bytes()).hexdigest(); subprocess.run(cmd,check=True)
    assert hashlib.sha256(out.read_bytes()).hexdigest()==h
