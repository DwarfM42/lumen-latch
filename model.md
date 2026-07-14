# 既存モデル整合性監査

## 性格と出力定義
本モデルは実デバイスへ校正した予測器ではなく、カスケード条件を比較する **simulation only** の感度モデルである。

- `q_factor`（Q proxy、無次元）: `Q = 7 - 0.12*N_span - 0.03*abs(T_C-25) - 20*CV - 0.20*sigma_gain_dB + 0.08*(ER_dB-10)`。係数は全て設計感度仮定で、実測Qへのfitではない。
- `error_rate`（無次元）: 固定seed Monte Carloで、`standard_normal > Q proxy` となるmargin failureと、段ごとのwrite error、read disturb、保持hazardの和事象を数えた試行失敗率。有限試行（標準10,000）なので `0` は「ゼロBER」を意味しない。
- Gaussian BER proxy: 等分散Gaussian OOKが成立し、かつQが測定分布から定義された場合だけ `BER_G=0.5*erfc(Q/sqrt(2))`。現行Q proxyにはこの校正がなく、CSV `error_rate` とも別物である。

## 64段AND受入監査
提案条件は **`Q >= 6 AND error_rate < 1e-9`**。改善だけでは合格にしない。

| 戦略 | Q proxy | Monte Carlo error_rate | Q条件 | error条件 | 総合 |
|---|---:|---:|---|---|---|
| passive | -1.59 | 0.9458 | FAIL | FAIL | **FAIL** |
| each-stage | 5.97 | 0.0003 | FAIL | FAIL | **FAIL** |
| periodic (N=4) | 5.61 | 0.0005 | FAIL | FAIL | **FAIL** |

## 光パワーと13.4 pJ収支
1段透過率は `T=10^(-(L_cell+L_link)/10)`。受動枝は `P[n+1]=P[n]*T/F`、各段再生は `min(P_nominal,P[n]*T*G/F)`、周期再生はN段ごとに理想復元する。

PCM吸収地点の必要エネルギーを `E_abs` とすると、

`E_abs = P_out * tau * eta_c * eta_a`

であり、`E_abs=13.4 pJ`, `P_out=1 mW` の理想下限は `tau=13.4 ns`。一般には `tau=13.4 ns/(eta_c*eta_a)`。13.4 pJは測定値、1 mW・効率・パルス形状はモデル仮定であり分離する。従来の `13.4+1.5*N_regen` はイベント比較用で、wall-plug総エネルギーではない。総監査は `system_energy_audit.md` を参照。

## 再生器の現行扱い
| 項目 | 現行扱い | 証拠区分 |
|---|---|---|
| output clamp / level restoration | nominalへのhard clamp | simulation assumption |
| saturation | nominal上限のみ | partial |
| output ER | 12 dB開始、spanごと0.08 dB低下、6 dB clamp | assumption |
| gain / gain noise | gain=4、noise=0.35 dBをQ式へ線形投入 | assumption |
| pump energy | 明示せず、1.5 pJ/regeneratorで代用 | parameter不足 |
| standby / bias | 0扱いではなくモデル外 | not evaluated |
| input dependence | clamp前は入力比例、再生時は閾値なしで復元 | 非現実的理想化 |

ASE、RIN、shot noise、timing jitter、pump depletion、thermal drift/cross-talk、波長detuning、偏光、back-reflection、位相、飽和雑音、endurance劣化は未モデルである。
