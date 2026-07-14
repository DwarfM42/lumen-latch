# シミュレーション計画

## 現行比較
passive、each-stage ideal restoration、periodic N-stage restorationを1–64段で比較する。現行CSV/8 PNGは監査基準として不変に保つ。

## 不足parameterと評価設計
| 不足parameter | 取得方法 | sweep / 受入評価 |
|---|---|---|
| PCM write energy分布 | 同一geometryで1000+ pulse、入力面と吸収面を同時校正 | 温度×状態×pulse width、pJ budgetを信頼区間化 |
| real Q/BER noise | ASE/RIN/shot/receiver/timingを個別測定 | PRBS、10^9 bit以上、Q proxyから実BERへの校正（Phase 2） |
| gain saturation/ASE | 入出力power・OSNR sweep | gain 1–20、fan-out 1–8、段数1/2/4/16/64 |
| threshold temperature shift | 0–70 °C chamber | worst-case ±10%判定、thermal hysteresis |
| array CV / correlation | wafer/lot sampling | raw/校正後CV、yield、spatial correlation |
| post-link ER | 実splitter・waveguide・coupler使用 | ER>=6 dBかつQ/BER AND条件 |
| standby/pump/bias | wall-plug instrumentation | dynamic/static分離、activity 1e-4–1 |
| wavelength/polarization/detuning/reflection | tunable laser・polarization・reflectometry | linewidth corner、back-reflection安定性 |

## Phase 2優先項目
1. **pJ級PCM write energy budget**: absorption planeからlaser wall-plugまで同時測定し二重計上を排除。
2. **BER/Q real-noise calibration**: Q proxy、Gaussian analytical BER、event failureを分離し、多段PRBS実測へ接続。

既存テストはpassive減衰、各段/周期復元、seed再現、温度/CV劣化、CLI生成を維持する。system modelは240行、有限値、単調性、単位、再現性を別テストする。
