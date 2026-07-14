"""LumenLatch system-energy accounting; values beyond the PCM boundary are scenarios, not measurements."""
from __future__ import annotations
import argparse, csv, math
from pathlib import Path

FREQUENCIES_HZ=(1e3,1e6,1e8,1e9)
CELL_COUNTS=(1,1e3,1e6,1e9)
ACTIVITIES=(1e-4,1e-3,1e-2,1e-1,1.0)
PCM_WRITE_ABSORBED_PJ=13.4
PCM_READ_REPORTED_PJ=0.48
SCENARIOS={
 'pcm_absorbed_floor': dict(eta_abs=1.,eta_waveguide=1.,eta_split=1.,eta_coupling=1.,eta_laser_eo=1.,read_pj=0.,amp_pj=0.,control_pj=0.,static_shared_w=0.,static_cell_w=0.,completeness='lower_bound_not_system_total',unknown='laser/coupling/waveguide/split/amplifier/pump/bias/thermal/detector/control unknown'),
 'optimistic_integrated': dict(eta_abs=.80,eta_waveguide=.95,eta_split=.95,eta_coupling=.85,eta_laser_eo=.30,read_pj=PCM_READ_REPORTED_PJ,amp_pj=2.,control_pj=1.,static_shared_w=.05,static_cell_w=1e-6,completeness='scenario_total_known_terms_only',unknown='thermal control and standby architecture unknown'),
 'conservative_current_lab': dict(eta_abs=.50,eta_waveguide=.80,eta_split=.90,eta_coupling=.25,eta_laser_eo=.15,read_pj=PCM_READ_REPORTED_PJ,amp_pj=50.,control_pj=20.,static_shared_w=5.,static_cell_w=5e-3,completeness='scenario_total_known_terms_only',unknown='EDFA/CW pump/cooling/control duty and measured wall-plug boundary unknown'),
}

def _fraction(value):
    if not math.isfinite(value) or value<=0 or value>1: raise ValueError('efficiency must be finite in (0,1]')
    return value

def laser_electrical_energy_pj(pcm_absorbed_pj,eta_abs,eta_waveguide,eta_split,eta_coupling,eta_laser_eo):
    if not math.isfinite(pcm_absorbed_pj) or pcm_absorbed_pj<0: raise ValueError('energy must be finite and nonnegative')
    denominator=math.prod(_fraction(x) for x in (eta_abs,eta_waveguide,eta_split,eta_coupling,eta_laser_eo))
    return pcm_absorbed_pj/denominator

def power_budget_w(energy_active_pj,frequency_hz,cells,activity,static_shared_w,static_cell_w):
    values=(energy_active_pj,frequency_hz,cells,activity,static_shared_w,static_cell_w)
    if any(not math.isfinite(x) or x<0 for x in values) or activity>1: raise ValueError('invalid power parameter')
    dynamic=cells*activity*frequency_hz*energy_active_pj*1e-12
    static=static_shared_w+cells*static_cell_w
    return {'dynamic_w':dynamic,'static_w':static,'total_w':dynamic+static}

def scenario_energy(name):
    s=SCENARIOS[name]
    if name=='pcm_absorbed_floor': write=PCM_WRITE_ABSORBED_PJ; read=0.
    else:
        eff=(s['eta_abs'],s['eta_waveguide'],s['eta_split'],s['eta_coupling'],s['eta_laser_eo'])
        write=laser_electrical_energy_pj(PCM_WRITE_ABSORBED_PJ,*eff)
        read=laser_electrical_energy_pj(s['read_pj'],*eff)
    return write,read,write+read+s['amp_pj']+s['control_pj']

def write_budget_csv(path):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    fields=('scenario','frequency_hz','cells','activity','pcm_write_absorbed_pj','pcm_read_reported_pj','laser_electrical_write_pj','laser_electrical_read_pj','amplifier_regeneration_pj','detector_control_pj','dynamic_active_pj','static_shared_w','static_cell_w','dynamic_w','static_w','total_w','eta_abs','eta_waveguide','eta_split','eta_coupling','eta_laser_eo','completeness','unknown_components','evidence_tags','feasibility')
    with path.open('w',newline='',encoding='utf-8') as h:
        w=csv.DictWriter(h,fieldnames=fields,lineterminator=chr(10)); w.writeheader()
        for name,s in SCENARIOS.items():
            write,read,active=scenario_energy(name)
            for f in FREQUENCIES_HZ:
                for n in CELL_COUNTS:
                    for a in ACTIVITIES:
                        p=power_budget_w(active,f,n,a,s['static_shared_w'],s['static_cell_w'])
                        w.writerow(dict(scenario=name,frequency_hz=f'{f:.12g}',cells=f'{n:.12g}',activity=f'{a:.12g}',pcm_write_absorbed_pj='13.4',pcm_read_reported_pj='0.48',laser_electrical_write_pj=f'{write:.12g}',laser_electrical_read_pj=f'{read:.12g}',amplifier_regeneration_pj=f"{s['amp_pj']:.12g}",detector_control_pj=f"{s['control_pj']:.12g}",dynamic_active_pj=f'{active:.12g}',static_shared_w=f"{s['static_shared_w']:.12g}",static_cell_w=f"{s['static_cell_w']:.12g}",dynamic_w=f"{p['dynamic_w']:.12g}",static_w=f"{p['static_w']:.12g}",total_w=f"{p['total_w']:.12g}",eta_abs=s['eta_abs'],eta_waveguide=s['eta_waveguide'],eta_split=s['eta_split'],eta_coupling=s['eta_coupling'],eta_laser_eo=s['eta_laser_eo'],completeness=s['completeness'],unknown_components=s['unknown'],evidence_tags='PCM write:measured; read:measured boundary incomplete; efficiencies/static:scenario assumption; missing:unknown',feasibility='arithmetic_only_not_feasibility_claim'))
    return path

def main(argv=None):
    p=argparse.ArgumentParser(); p.add_argument('--output',type=Path,default=Path('system_energy_budget.csv')); a=p.parse_args(argv)
    path=write_budget_csv(a.output); print(f'Wrote {path} ({len(SCENARIOS)*len(FREQUENCIES_HZ)*len(CELL_COUNTS)*len(ACTIVITIES)} rows, {len(SCENARIOS)} scenarios).'); return 0
if __name__=='__main__': raise SystemExit(main())
