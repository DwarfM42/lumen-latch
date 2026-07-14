# LumenLatch

LumenLatchは、光で状態を書き換え、保持し、その出力を再生して次段セルへ伝える「カスケード可能な光学式1ビットセル」の成立可能性を調査する個人研究プロジェクトです。

本リポジトリは完成した光コンピュータの設計ではありません。
現在は、既存研究の整理、成立条件の数値化、簡易シミュレーション、未解決課題の特定を行う初期スコーピング段階です。

現時点では、光書込み・光読出し・不揮発保持を行うPCMセルは既存研究で実証されています。一方、前段の同種セルから得られた実出力だけで次段の同種PCMセルを書き換え、多段接続する実証は確認できていません。

初期モデルでは、完全受動接続は多段化に失敗し、光増幅・信号再生を介する方式に可能性が見られました。ただし、現在のQ値とエラー率は実デバイスのBERとして校正されたものではなく、PCM書込みエネルギー、光源効率、増幅器雑音、待機電力、熱密度なども未確定です。

このリポジトリでは、成功結果だけでなく、仮定、限界、否定的結果、モデル上の問題点も公開します。

## 現在の到達点と監査結果
- PCM単セルの光書込・読出し・多値不揮発、13.4 pJ吸収書込、3か月保持は一次資料で確認。
- 厳密なPCM出力→同種次段PCM書換えは未確認。Feldmannのcarryは外部pulseの90:10分岐。
- 64段の `Q>=6 AND error_rate<1e-9` はpassive、each-stage、periodicの全てがFAIL。
- `q_factor`は無次元engineering proxy、`error_rate`はMonte Carlo event failureであり、Gaussian BERでも実測BERでもない。

## 4方式判定（現在の仮定）
| 方式 | energy/bit・write | standby/heat/area | latency/fanout/multistage | E/O変換 | 判定 |
|---|---|---|---|---|---|
| passive | 追加pumpなし、PCM write境界は不足 | 低static候補、損失累積 | gainなし、64段数値FAIL | 0 | **数値上不成立** |
| external CW-pumped all-optical signal | pump/再生energy unknown | CW heat/area unknown | transistor型に可能性、実PCM多段不足 | 0 | **parameter不足** |
| electrically biased optical regeneration | bias/amp energy unknown | bias standby・ASE・heat | gain/restoration候補 | 0（電力biasあり） | **条件付き** |
| optoelectronic hybrid | detector/modulator/control込み要測定 | electronic standby/area | 3R・fanoutを最も作りやすい | O/E+E/O/段 | **条件付き** |

外部energy補給は失敗条件ではなく、総energy、heat、latency、areaを含めて比較する。

## Energy boundary
13.4±0.6 pJはRíos 2015 Supplementary S5/Table S2の **PCM吸収地点**。waveguide launch、chip incident、laser output、wall-plugではない。`E_laser_elec=E_PCM_abs/(eta_abs*eta_waveguide*eta_split*eta_coupling*eta_laser_EO)` で上流へ展開する。unknown=0のfloorをsystem totalとは呼ばない。詳細は `system_energy_audit.md`。

## 成果物
- `research_summary.md`, `sources.csv`: 一次資料と証拠区分
- `requirements.md`, `model.md`, `simulation_plan.md`: 要件、モデル整合性、不足評価
- `simulate_optical_cell.py`, `simulation_results.csv`, `figures/`: 既存cascade感度モデル
- `system_energy_audit.md`, `system_energy_model.py`, `system_energy_budget.csv`: system energy監査
- `tests/`: cascade 8 test＋system energy 7 test

## 再現（Windows Git Bash）
```bash
uv venv .venv --python 3.11
uv pip install --python .venv/Scripts/python.exe -r requirements.txt
./.venv/Scripts/python.exe simulate_optical_cell.py --output-dir . --seed 20260715 --trials 10000
./.venv/Scripts/python.exe system_energy_model.py --output system_energy_budget.csv
./.venv/Scripts/python.exe -m pytest tests -q
sha256sum simulation_results.csv
```
CSV基準SHA-256は `2de08f6d7744aea0a6c2db67e7bb25a48691b85ae115b3a80e59d9d2bd0b2dbf`。旧hash `04dd5214...` からの更新理由は、各行の記録値と計算値を一致させるため、保持時間を24 hから記録済みの2160 hへ、Q/error計算のERを固定12 dBから記録済みの劣化後ERへ変更し、実際の行固有seedをCSVへ記録したためである。192 data rowsと8 PNGは維持し、64段の全方式FAILという結論は変わらない。system CSVは3 scenario×80 operating points=240 data rows。

## error-rate図の条件
`figures/stages_vs_error_rate.png` はCSVの各行を描画した図ではなく、別の感度条件によるstage sweepである。stage 0–64、ER=10 dB、保持時間24 h、温度25 °C、threshold CV=0.05、gain noise=0.35 dB、write error=1e-5、read disturb=1e-6、周期再生間隔4を用いる。seedはCSVと同じ `base seed + strategy offset + stage` 規則である。`temperature_vs_error_rate.png` と `variation_vs_error_rate.png` もER=10 dB・保持時間24 hを基準とし、それぞれ温度またはthreshold CVだけを掃引する。したがって、これら3図のerror rateを、劣化後ERと2160 h保持を使う `simulation_results.csv` の値として読んではならない。

## 限界と次Phase
未モデルはASE、RIN、shot noise、jitter、pump depletion、thermal drift/cross-talk、wavelength/polarization/detuning、back-reflection、実array CV、endurance、wall-plug standby。次Phaseは (1) pJ級PCM write energyを吸収面からwall-plugまで測定、(2) Q proxyをASE/RIN/shot/timing込みPRBS BERへ校正、の2件を優先する。
