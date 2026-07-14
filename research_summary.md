# 完全光学式1ビットセルと同種カスケードの研究要約

## 範囲と判定基準
対象は1ビット保持、光読出し、同種次段駆動である。全光という語がPCM相転移への最終刺激だけを意味する場合と、外部EOM、EDFA、電子trigger、別pumpを含まない自律カスケードを区別する。数値は **experimentally demonstrated**、**conditional**、**simulation only**、**not demonstrated**、**currently difficult** に分類する。NRは未報告で、他素子の値を流用しない。

## 主要結論
1. **PCM単セルは実証済み**: Ríos et al. 2015はGST導波路セルで光書込・光読出・8準位不揮発動作、最小13.4 pJ、少なくとも3か月保持を実測した。ただし前段PCMの実出力だけで同種次段を不揮発書換えする実験は未実証。最小値と430 pJ級の別geometryを合成して架空のbest cellにはしない。
2. **Feldmann 2017 optical abacusは厳密カスケードではない**: carryは外部書込pulseを90:10にsplitし、その一部を第2PCMへ送る。第1PCM透過出力による駆動ではなく、分岐調整にはoptical amplifierも使う。
3. **真正二段に最も近い実証**: Islam 1990のfiber soliton NORは同型二段tandem、gain 4.5、約30 pJ。ただし非集積。Ballarini et al. 2013のpolariton transistorは第1段出力で40 µm離れた第2段Controlをswitchし、最大gain 19、ER約12 dB、約10 ps、activation約1 fJ、level restorationを示した（下限4は今回のローカル一次資料で直接再確認できないためrange主張を弱めた）。ただし各段にAddress pump、無機GaAs系は10 Kで、1 fJはpump・cooling込みwall-plug energyではない。
4. **SOA-MZI、ring、PhC**: 5–10 Gb/s級SOA RAM、20 ps・5.5 fJ ring laser memory、30–74 fJ級PhC memory、128-bit WDM集積など単セル・配列実証は多数。しかし同種多段のBER、fan-out、link gain、logic-level restorationを同時に測った報告はほぼない。128 resonatorのbus直列配置は論理カスケードではない。
5. **一つの万能方式はない**: PCMは不揮発保持が強いが出力利得がない。polaritonはgainとrestorationが強いが保持・温度・pumpが弱い。SOA/laserは局所電力でgainを得るがbias heat、ASE、detuningを負う。受動ring/PhCはgain <= 1でfan-outと損失復元が現状困難。

## 技術別証拠
| 技術 | 単セル | 同種二段 | gain / restoration | 支配的障害 | 判定 |
|---|---|---|---|---|---|
| PCM GST/AIST | 光書込・読出・多値不揮発 | 前段実出力駆動なし | 受動、状態依存吸収 | read出力とwrite thresholdのenergy非対称 | 実証済み単セル、cascade未実証 |
| SOA-MZI / SRAM | 5–10 Gb/s級 | 同一RAMセル二段NR | SOA gain、電流bias、ASE | 多段net gainとheat | 条件付き単セル |
| semiconductor ring laser | 20 ps、5.5 fJ等 | NR | electrical pump由来gain | resonance調整と多段整合 | 単セル実証 |
| passive ring / PhC | 30–74 fJ級例 | NR | gainなし | loss、fan-out、drift | 現状困難 |
| fiber soliton NOR | gate | 同型二段 | gain 4.5 | 非集積、pulse形成 | 二段実証済み |
| inorganic polariton | transistor | 2段 | 最大gain 19、restoration | 10 K、各段Address pump、保持なし | 条件付き二段 |

## 工学条件（本評価の提案target）
`G_cell*T_link/F >= 2` を設計余裕込み条件とする。再生段ERは10 dB以上、最悪リンク後6 dB以上。等分散Gaussian OOKの目安としてBER<1e-9にQ>=6を要求するが、ERだけからBERは保証しない。温度0–70 deg C、threshold shift ±10%、array CV<=5%、平均1 mW/cell以下を評価する。平均電力は `P_static + E_write*f_write + E_read*f_read` とし、pump、SOA bias、laser、clock、thermal tuning、coolingをsystem外へ隠さない。

## 保持・disturb・write reliability
Ríos 2015の3か月保持は実測だが、10年保持や高速logic用途のenduranceではない。100 write/erase cyclesの報告から高頻度書換え寿命は証明できない。read disturb、write error、threshold CV、0–70 deg Cの多段yieldは主要文献でNRが多い。本simulatorの既定rateはsensitivity assumptionであり測定値ではない。

## シミュレーションの読み方
passiveはenergy追加なしだがlossとmarginが累積する。each-stageは理想level restorationを置くためpowerは維持するが、各段energyとnoise sourceを負う。periodicは中間案。本モデルがtargetを満たしても物理実証にはならず、同種二段、次にfan-out、最後に多段PRBS BERとtemperature cornerを測る必要がある。

## 調査制約
一部IEEE/Nature本文は購読制限がある。提供された調査資料はpublisher page、Crossref/OpenAlex、公開accepted manuscriptで照合済みの結果を利用した。詳細claim mapは `sources.csv`。未報告値は推測しない。


## 監査追補：4方式とsystem energy
| 方式 | energy/bit | energy/write | standby | latency | heat | area | fanout | multistage | E/O conversions | 現在判定 |
|---|---|---|---|---|---|---|---|---|---|---|
| passive PCM | delivered-bit値NR | 13.4 pJはPCM吸収面のみ | 低static候補 | write 10 ns例 | 高activity密度は不明 | PCM小型、link込みNR | gainなし | 64段AND条件FAIL | 0 | **数値上不成立** |
| external CW-pumped all-optical signal | pump込みNR | PCM+pump境界NR | CW pump必須 | optical、実値NR | CW heat NR | pump/splitter込みNR | local energyで候補 | PCM同種多段NR | 0 | **parameter不足** |
| electrically biased optical regeneration | bias/amp込みNR | PCM+regen NR | electrical bias必須 | SOA等依存 | bias/ASE heat NR | active device込みNR | gain候補 | restoration候補、BER NR | optical pathは0（電力biasあり） | **条件付き** |
| optoelectronic hybrid | detector+logic+modulator込みNR | PCM+OEO NR | clock/electronics依存 | O/E/O遅延 | electronic/laser heat NR | detector/CMOS/modulator | 最も実装容易 | 3R候補、同一cell多段NR | O/E+E/Oを段ごと | **条件付き** |

外部energyは情報を保ったまま次段駆動energyを供給する正当なtransistor型機構であり、それだけで失敗とはしない。優劣はenergy/write、delivered bit、standby、latency、heat、area、fanout、多段BER、conversion回数で判定する。

13.4±0.6 pJはRíos Supplementary S5/Table S2の1 µm GST、-0.97 dB、10 nsに対するPCM吸収光energyである。S1のCW diode→EOM→EDFA→fiber/grating coupler→waveguide→GSTの上流損失・wall-plugは含まれない。詳細なdynamic/static、3 scenario、240 operating pointsと用途判定は `system_energy_audit.md`。

## 電子比較の境界と用途判定
一次資料で確認したSRAM macro access、10 mm on-chip TX+wire+RX、HBM I/O receiver/transceiver、45 nm arithmetic estimateは、順にmemory access、delivered link bit、interface bit、算術operationという別機能である。HBM array/ACT-PRE、SRAM read単独、FP8演算はNRであり、HorowitzのMAC値は表のmultiply+addからの **derived arithmetic-only sum（memory excluded）** であって実accelerator総energyではない。

したがって13.4 pJ absorbed PCM writeとの直接順位付けはしない。LumenLatchは低頻度のnonvolatile state/weights/routingには候補を残す一方、高頻度logic、chip-to-chip transfer、matrix computeの優位を主張するにはlaser wall-plug、readout、ADC/DAC、control、memory traffic、standbyを同一boundaryで実測する必要がある。
