# Cascadable all-optical one-bit-cell simulation; all coefficients are assumptions.
import argparse
import csv
import math
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

STRATEGIES=("passive","each-stage","periodic")
FIGURES=("stages_vs_power.png","stages_vs_error_rate.png","insertion_loss_vs_max_stages.png","extinction_ratio_vs_max_stages.png","fanout_vs_max_stages.png","temperature_vs_error_rate.png","variation_vs_error_rate.png","regenerator_interval_vs_total_energy.png")

def propagate_power(initial_power_mw,stages,strategy,insertion_loss_db,link_loss_db,fanout=1,gain=1.0,regeneration_interval=1):
    if strategy not in STRATEGIES: raise ValueError(f"unknown strategy: {strategy}")
    if fanout<1 or stages<0 or regeneration_interval<1: raise ValueError("invalid cascade parameters")
    transmission=10**(-(insertion_loss_db+link_loss_db)/10)
    nominal=float(initial_power_mw); powers=[nominal]
    for stage in range(1,stages+1):
        value=powers[-1]*transmission/fanout
        if strategy=="each-stage": value=min(nominal,value*gain)
        elif strategy=="periodic" and stage%regeneration_interval==0: value=nominal
        powers.append(value)
    return powers

def calculate_q_margin(stages,strategy,temperature_c,threshold_cv,regeneration_interval,gain_noise_db,extinction_ratio_db):
    if strategy=="passive": span=stages
    elif strategy=="each-stage": span=1 if stages else 0
    elif strategy=="periodic": span=min(stages,regeneration_interval)
    else: raise ValueError(f"unknown strategy: {strategy}")
    return 7.0-0.12*span-0.03*abs(temperature_c-25.0)-20.0*threshold_cv-0.20*gain_noise_db+0.08*(extinction_ratio_db-10.0)

def estimate_error_rate(stages,strategy,seed,trials=10000,temperature_c=25.0,threshold_cv=0.05,regeneration_interval=4,gain_noise_db=0.35,extinction_ratio_db=10.0,write_error_rate=1e-5,read_disturb_rate=1e-6,retention_hours=24.0):
    if trials<1 or threshold_cv<0: raise ValueError("invalid Monte Carlo parameters")
    q=calculate_q_margin(stages,strategy,temperature_c,threshold_cv,regeneration_interval,gain_noise_db,extinction_ratio_db)
    rng=np.random.default_rng(seed)
    margin_fail=rng.standard_normal(trials)>q
    event=1-(1-write_error_rate)**max(stages,1)
    event+=1-(1-read_disturb_rate)**max(stages,1)
    event+=min(0.25,retention_hours*1e-10*max(stages,1))
    return float(np.mean(margin_fail | (rng.random(trials)<min(1.0,event))))

def save_plot(path,x,series,xlabel,ylabel,yscale=None):
    fig,ax=plt.subplots(figsize=(7.2,4.8))
    for label,y in series.items(): ax.plot(x,y,marker="o" if len(x)<25 else None,markersize=3,label=label)
    if yscale: ax.set_yscale(yscale)
    ax.set_xlabel(xlabel); ax.set_ylabel(ylabel); ax.grid(True,alpha=0.3)
    if len(series)>1: ax.legend()
    fig.tight_layout(); fig.savefig(path,dpi=150,metadata={"Software":"lumen-latch"}); plt.close(fig)

def generate_figures(folder,seed,trials):
    folder.mkdir(parents=True,exist_ok=True); stages=np.arange(65)
    powers={s:np.array(propagate_power(1.0,64,s,0.5,0.5,gain=4.0,regeneration_interval=4)) for s in STRATEGIES}
    errors={s:np.array([estimate_error_rate(i,s,seed+j*10000+i,trials=trials) for i in stages]) for j,s in enumerate(STRATEGIES)}
    save_plot(folder/FIGURES[0],stages,powers,"Cascade stage","Optical power (mW)","log")
    save_plot(folder/FIGURES[1],stages,{k:np.clip(v,1e-6,1) for k,v in errors.items()},"Cascade stage","Monte Carlo error rate","log")
    losses=np.linspace(0.1,3,30); maximum=np.floor(np.log(0.2)/np.log(10**(-losses/10)))
    save_plot(folder/FIGURES[2],losses,{"passive":maximum},"Insertion + link loss (dB/stage)","Max stages before 0.2 mW")
    ers=np.linspace(6,20,29); save_plot(folder/FIGURES[3],ers,{"0.08 dB/stage degradation":np.floor((ers-6)/0.08)},"Regenerator output ER (dB)","Max stages before 6 dB")
    fanouts=np.arange(1,9); trans=10**(-0.1); fanstages=np.maximum(0,np.floor(np.log(0.2)/np.log(trans/fanouts)))
    save_plot(folder/FIGURES[4],fanouts,{"passive, 1 dB/stage":fanstages},"Fan-out","Max stages before 0.2 mW")
    temps=np.linspace(0,70,29); terr=np.array([estimate_error_rate(32,"periodic",seed+i,trials=trials,temperature_c=float(t)) for i,t in enumerate(temps)])
    save_plot(folder/FIGURES[5],temps,{"periodic N=4":np.clip(terr,1e-6,1)},"Temperature (deg C)","Monte Carlo error rate","log")
    cvs=np.linspace(0,0.2,21); verr=np.array([estimate_error_rate(32,"periodic",seed+500+i,trials=trials,threshold_cv=float(v)) for i,v in enumerate(cvs)])
    save_plot(folder/FIGURES[6],cvs*100,{"periodic N=4":np.clip(verr,1e-6,1)},"Threshold CV (%)","Monte Carlo error rate","log")
    intervals=np.arange(1,17); energy=13.4+np.ceil(64/intervals)*1.5
    save_plot(folder/FIGURES[7],intervals,{"64-stage cascade":energy},"Regenerator interval (stages)","Total event energy (pJ)")

def run_simulation(output_dir,seed,trials):
    output_dir.mkdir(parents=True,exist_ok=True); figure_dir=output_dir/"figures"; figure_dir.mkdir(exist_ok=True)
    for old in figure_dir.glob("*.png"): old.unlink()
    path=output_dir/"simulation_results.csv"
    fields=["strategy","stages","optical_power_mw","total_loss_db","extinction_ratio_db","fanout","gain","gain_noise_db","temperature_c","threshold_cv","retention_hours","read_disturb_rate","write_error_rate","regeneration_interval","error_rate","q_factor","total_energy_pj","seed"]
    with path.open("w",newline="",encoding="utf-8") as handle:
        writer=csv.DictWriter(handle,fieldnames=fields,lineterminator=chr(10)); writer.writeheader()
        for si,strategy in enumerate(STRATEGIES):
            for stages in range(1,65):
                power=propagate_power(1,stages,strategy,0.5,0.5,gain=4,regeneration_interval=4)[-1]
                span=stages if strategy=="passive" else (1 if strategy=="each-stage" else min(stages,4))
                er=max(6,12-0.08*span); regen=0 if strategy=="passive" else (stages if strategy=="each-stage" else stages//4)
                rowseed=seed+si*10000+stages
                retention_hours=2160.0
                error=estimate_error_rate(stages,strategy,rowseed,trials=trials,extinction_ratio_db=er,retention_hours=retention_hours)
                q=calculate_q_margin(stages,strategy,25,0.05,4,0.35,er)
                writer.writerow({"strategy":strategy,"stages":stages,"optical_power_mw":f"{power:.12g}","total_loss_db":f"{-10*math.log10(max(power,1e-300)):.6f}","extinction_ratio_db":f"{er:.6f}","fanout":1,"gain":"4.000000","gain_noise_db":"0.350000","temperature_c":"25.000000","threshold_cv":"0.050000","retention_hours":f"{retention_hours:.6f}","read_disturb_rate":"1e-06","write_error_rate":"1e-05","regeneration_interval":4,"error_rate":f"{error:.12g}","q_factor":f"{q:.6f}","total_energy_pj":f"{13.4+1.5*regen:.6f}","seed":rowseed})
    generate_figures(figure_dir,seed,trials); return path

def main(argv=None):
    parser=argparse.ArgumentParser(); parser.add_argument("--output-dir",type=Path,default=Path(".")); parser.add_argument("--seed",type=int,default=20260715); parser.add_argument("--trials",type=int,default=10000)
    args=parser.parse_args(argv)
    if args.trials<1: parser.error("--trials must be positive")
    path=run_simulation(args.output_dir,args.seed,args.trials); print(f"Wrote {path} and {len(FIGURES)} figures (seed={args.seed})."); return 0

if __name__=="__main__": raise SystemExit(main())
