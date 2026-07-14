# 13.4 pJ システム総エネルギー監査

## 結論
**13.4 ± 0.6 pJはシステム総エネルギーではない。** Ríos et al. 2015 Supplementary S5/Table S2の1 µm GSTセル（減衰 -0.97 dB、10 ns pulse）について、既知の吸収と測定pump pulse energyから算出した **GST/PCMが吸収した光エネルギー** である。waveguide launch、chip incident、laser output、laser wall-plugのいずれでもない。

Supplementary S1の経路は `CW diode laser → EOM → EDFA → fiber/focusing grating coupler → waveguide → GST`。13.4 pJにはこれら上流のlaser E/O損失、EOM、EDFA、fiber/coupler、制御、冷却は含まれない。S3は `E_GST/E_tot` と `E_tot=(1-A)E_pulse` を分離する。したがって吸収エネルギーをlaser electrical energyへ足し直すと二重計上になる。報告read pulse `0.48 ± 0.03 pJ` は本文で比較に使えるが、取得資料だけでは13.4 pJと同じ境界が完全には確定できず、本監査では「測定値・境界不十分」とした。

## 境界式とcomponent分離

`E_laser_elec = E_PCM_abs/(eta_abs*eta_waveguide*eta_split*eta_coupling*eta_laser_EO)`

ここで `E_PCM_abs` は末端の吸収地点。分母に同じ損失を一度だけ置く。dynamicはPCM write/read、laser E/O、coupling/waveguide/split、amplifier/regeneration、detector/controlをイベントごとに集計する。staticはCW pump/electrical bias、thermal control、standbyをshared/cellへ分ける。

| component | dynamic/static | 現在のタグ | 注意 |
|---|---|---|---|
| PCM write absorption 13.4±0.6 pJ | dynamic | measured | GST吸収面 |
| PCM read 0.48±0.03 pJ | dynamic | measured, boundary incomplete | totalへ無批判に流用しない |
| laser E/O | dynamic | scenario assumption / unknown | 分母で変換、PCMを再加算しない |
| coupling/waveguide/split | dynamic loss | scenario assumption / unknown | efficiency積 |
| amp/regeneration | dynamic + static候補 | scenario assumption / unknown | EDFA/SOA/CW pumpを明示 |
| CW pump/electric bias | static | unknown | 0はunknownの代用ではない |
| thermal control | static | unknown | cryogenic/coolingも含む |
| detector/control | dynamic/static | scenario assumption / unknown | clock/EOM/AWGを含み得る |
| standby | static | unknown | activityと分離 |

値のタグは **measured / literature range / scenario assumption / unknown**。unknownを0に置いた結果を「system total」と呼ばない。

## 3 scenario
- `pcm_absorbed_floor`: 13.4 pJのみ。物理下限であり **lower_bound_not_system_total**。
- `optimistic_integrated`: `eta_abs=.80, eta_waveguide=.95, eta_split=.95, eta_coupling=.85, eta_laser_EO=.30`、read 0.48 pJ、再生2 pJ、control 1 pJ、shared 50 mW、cell standby 1 µW。全て将来集積のscenario assumption。
- `conservative_current_lab`: `.50,.80,.90,.25,.15`、再生50 pJ、control 20 pJ、shared 5 W、cell 5 mW。現行labの厳密測定ではなく保守scenario。

各scenarioは `f={1 kHz,1 MHz,100 MHz,1 GHz}`、`N={1,10^3,10^6,10^9}`、`activity={0.0001,0.001,0.01,0.1,1}` の80組、計240行。

`P_dynamic=N*A*f*E_dynamic_active`、`P_total=P_dynamic+P_static_shared+N*P_static_cell`。

非現実的な大規模・高周波点も算数監査のため表示するが、CSV `feasibility=arithmetic_only_not_feasibility_claim` とし成立主張には使わない。

## 電子方式の一次資料比較
比較単位は対象ごとに固定する。CPU TDP/clockは使用しない。以下の値は同じ機能を測っていないため、異なるboundaryを一つの代表rangeへ合成せず、LumenLatchの **13.4 ± 0.6 pJ/absorbed PCM write** と直接順位付けしない。

| source / year / node | measured value | normalized functional unit | boundary / included | exclusions / caveat |
|---|---:|---|---|---|
| Yahya et al. / 2016 / commercial 130 nm CMOS | 6.24 pJ/access | 0.195 pJ/bit/access（32-bit wordで単純除算） | 1 KB 8T SRAM macro active access。decoder、WL driver、bank、read/write peripheralを含む | read/write混合の最小総access。**read単独 NR**。I/O pad・外部controllerの含有は確認できない |
| Yoshimoto et al. / 2012 / 40 nm bulk CMOS | 12.9 pJ/access (50% R/50% W); 1.52 pJ/write cycle | 0.80625 pJ/bit/mixed access; 0.095 pJ/bit-write（16-bit word） | 512 Kb 8T SRAM macroのactive energy、array/peripheryを含む | leakageとmacro外I/O padsを除外。**read単独 NR** |
| Mensink et al. / 2010 / 90 nm CMOS | 0.28 pJ/bit at 2 Gb/s | 0.028 pJ/bit/mm（10 mm） | differential TX + capacitively driven 10 mm wire + RX | on-chip PRBS、clock divider、output bufferおよび外部clock sourceを除外 |
| Schinkel et al. / 2006 / 0.13 µm CMOS | 2 pJ/bit at 3 Gb/s | 0.2 pJ/bit/mm（10 mm） | TX + uninterrupted 10 mm RC-limited wire + RX | clock generation、test-pattern generator、output buffersを除外。正しいJSSC DOIは `10.1109/JSSC.2005.859880` |
| Lee et al. / 2020 / 65 nm CMOS | 0.83 pJ/bit/pin at 6.4 Gb/s | 0.83 pJ/delivered interface bit | fabricated HBM base-die receiver/deserializer + phase interpolation/skew compensation | HBM stack、DRAM array core、ACT/PRE、controller、packageを除外。**array/ACT-PRE energy NR** |
| Park et al. / 2022 / node NR in directly checked title/abstract | 0.385 pJ/bit at 10 Gb/s | 0.385 pJ/delivered interface bit | HBM I/O TIA-terminated di-code transceiver + equalization、ECC、calibration | DRAM array、ACT/PRE、HBM stack全体を除外。**array/ACT-PRE energy NR**。本文paywallのためnode/voltage詳細NR |

### 45 nm算術演算（Horowitz, ISSCC 2014）
Horowitzの一次資料表は **45 nm、0.9 Vの推定energy** を pJ/operation で示す（fabricated acceleratorの実測ではない）。表で直接示される値だけを転記する。

| source / year / node | measured value | normalized functional unit | boundary / included | exclusions / caveat |
|---|---:|---|---|---|
| Horowitz / 2014 / 45 nm, 0.9 V | INT8 add 0.03; INT16 add 0.05; INT32 add 0.10 pJ | pJ/arithmetic add | arithmetic unit estimate | registers/interconnect/memory/controlを除外。実測silicon値ではない |
| Horowitz / 2014 / 45 nm, 0.9 V | INT8 multiply 0.20; INT16 multiply 1.00; INT32 multiply 3.10 pJ | pJ/arithmetic multiply | arithmetic unit estimate | 同上 |
| Horowitz / 2014 / 45 nm, 0.9 V | FP16 add 0.40; FP32 add 0.90 pJ | pJ/arithmetic add | arithmetic unit estimate | FP8は表に直接値なし（**NR**） |
| Horowitz / 2014 / 45 nm, 0.9 V | FP16 multiply 1.10; FP32 multiply 3.70 pJ | pJ/arithmetic multiply | arithmetic unit estimate | FP8は表に直接値なし（**NR**） |
| derived from Horowitz add + multiply | INT8 0.23; INT16 1.05; INT32 3.20 pJ | pJ/one multiply + one add | arithmetic-only serial sum | **derived, not author-reported MAC; memory excluded**。fusing/data reuse/controlはモデル化しない |
| derived from Horowitz add + multiply | FP16 1.50; FP32 4.60 pJ | pJ/one multiply + one add | arithmetic-only serial sum | **derived, not author-reported MAC; memory excluded**。FP8 MACは**NR** |

同一boundary内の代表rangeだけを述べると、SRAM macroは **0.095 pJ/bit-write**（write）および **0.195–0.80625 pJ/bit/access**（定義の異なるtotal/mixed access）、10 mm on-chip TX+wire+RXは **0.28–2 pJ/bit**、確認済みHBM I/O回路は **0.385–0.83 pJ/bit**、Horowitz arithmetic-only derived MACは **0.23–4.60 pJ/op** である。これらのrange同士、および13.4 pJ absorbed writeとの大小比較は機能・boundary不一致のため行わない。

一次資料anchorとしてRíos 2015、Nozaki 2019 O–E–O、Islam 1990 tandem NOR、Ballarini 2013 polaritonも保持する。未報告欄は **NR/parameter不足** とし、二次的な一般値で埋めない。

## 用途判定
| 用途 | 判定 | 理由 |
|---|---|---|
| high-frequency logic | **不利** | write 13.4 pJ吸収だけでも高activityで発熱、endurance/BER未確定 |
| nonvolatile memory | **条件付き** | 保持は実証、system write/read energy・endurance・array yield不足 |
| AI weights | **有望** | 低頻度program・不揮発多値は適合。ただしread/ADC/laser総電力が必要 |
| reconfigurable routing | **有望** | 低activityなら不揮発保持が利点。ER/loss/thermal drift要評価 |
| chip-to-chip | **不利** | PCM writeはbit transferと同機能でなく、I/O source/receiverが未計上 |
| matrix compute | **条件付き** | weight保持には有望、MAC全体のlaser/detector/ADC境界がunknown |
| low-frequency state | **有望** | write頻度が低ければstatic-free PCM保持を活かせる可能性 |

13.4 pJ単体から競合技術への優位は結論しない。

## 一次資料対応
- Ríos et al., *Integrated all-photonic non-volatile multi-level memory*, DOI `10.1038/nphoton.2015.182`: 13.4 pJ、3か月、S1/S3/S5/Table S2境界。
- Feldmann et al., DOI `10.1038/s41467-017-01506-3`: 90:10外部分岐とamplifier。前段出力駆動ではない。
- Islam (Islamを含む著者群), DOI `10.1364/OL.15.000417`: tandem同型NOR、gain 4.5、約30 pJ。
- Ballarini et al., DOI `10.1038/ncomms2734`: 2段、各段Address、最大gain 19、10 K。取得一次資料で下限4を直接再確認できないため「4–19」ではなく最大値を中心に記載する。
