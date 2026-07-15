# LumenLatch研究ランドスケープ：研究者の方向と最小検証ルート

調査日: 2026-07-15

## 目的

この文書は論文の性能値を並べるものではなく、研究者・研究室・企業が**次に何を作ろうとしているか**を公開情報から追い、LumenLatchを構成する「記憶」「再生」「増幅」「共振器」「集積」「システム設計」の担当候補を地図化する。

公開プロフィール、研究室ページ、プロジェクト、講演、求人、研究センターを一次情報として優先した。研究方向がページに明記されている場合を**確認**、複数の公開活動からLumenLatchとの接点を導いた場合を**推定**、公式ページで裏付けられなかった場合を**未確認**とする。研究室の将来計画や協力意思を断定しない。

## 最初に得られた結論

1. LumenLatchと同じ「不揮発PCM記憶＋同種次段駆動＋多段restoration」を正面から掲げる公開研究ラインは、今回確認した範囲では見つからない。
2. PCMフォトニクスの主流はAI weight、行列演算、相関検出、neuromorphic computing、reconfigurable photonicsへ向いている。
3. 光トランジスタ／polariton系はgainとnonlinearityを追うが、長時間保持と一体化するよりneuromorphic／quantum／ultrafast processingへ向いている。
4. 光AIは完全光学への純化ではなく、光の線形・並列処理と電子の非線形・制御を組み合わせる方向が強い。
5. 企業の公開製品は演算置換よりinterconnectを先に選んでいる。Lightmatterの現行トップページはPassage/Guideを「AI supercomputerをscaleするphotonic interconnect platform」として前面に出している。
6. LumenLatchの独自な位置は、PCM側の**保持**とtransistor/regenerator側の**gain・restoration**を、外部pump/biasを含む同一system boundaryで橋渡しする点にある。

## 重要な名称訂正

東京大学のheterogeneous Si photonics／programmable photonic circuit研究室は**竹中充（Mitsuru Takenaka）研究室**である。竹中博（Hiroshi Takenaka）ではない。東京大学電気系の[公式教員ページ](https://www.eeis.t.u-tokyo.ac.jp/en/staff/takenaka-mitsuru/)で確認した。

## 世界の5系統

### 1. PCMで記憶と演算を一体化する系統

| 研究者・組織 | 公開情報で確認できる方向 | 試作・人材シグナル | LumenLatchとの接点 | 証拠状態 |
|---|---|---|---|---|
| Oxford ANE / Harish Bhaskaran | Optoelectronic materialsによるbrain-inspired computing、display、interconnectとnanomanufacturing。Bhaskaranは2025年1月からOxfordをleaveしApple Directorを務め、問い合わせはANE group leadsへ誘導 | Oxford ANEという材料・nanomanufacturing系。個別sample提供条件は未確認 | PCM memory、nanostructure、plasmonic enhancement、製造 | **確認**: [Oxford profile](https://www.materials.ox.ac.uk/peoplepages/bhaskaran.html), [ANE](https://nanoeng.materials.ox.ac.uk/) |
| Wolfram Pernice Lab, Heidelberg | PCM不揮発switch／算術／all-optical neural networkから、NEQIOS、HYBRAIN、quantum photonicsを含むhybrid systemへ展開 | PCM in neuromorphic photonicsを含むBachelor/Master/PhDテーマ、chip fabrication/characterization、fiber coupling、wire bonding、電子制御を公開 | PCM photonic memory、cascade、restoration、packaging | **確認**: [Research tracks](https://www.kip.uni-heidelberg.de/photon/research/research_tracks), [Active projects](https://www.kip.uni-heidelberg.de/photon/research/active_projects), [Open positions](https://www.kip.uni-heidelberg.de/photon/openpositions) |
| Bowei Dong, A*STAR IME | Photonic neuromorphic computingから、RF×波長×空間多重とelectronics-photonics integrationを含むhigher-dimensional architectureへ展開 | IMEは200/300 mm設備、SiN/AlN/heterogeneous photonicsを公開。Dong個人emailは非公開で、技術連携はIME窓口 | 大規模PCM photonic architecture、edge/IoT用途、wafer-scale試作 | **確認**: [A*STAR profile](https://research.a-star.edu.sg/researcher/bowei-dong/), [2024 A*STAR highlight](https://research.a-star.edu.sg/articles/highlights/light-speed-data-highway/), [IME fab services](https://www.a-star.edu.sg/ime/rndfoundry) |
| Ghazi Sarwat Syed, IBM Zürich | Deep-learning accelerator向けprocessing-in-memoryを電子・光の両domainで進め、device、material、algorithm、softwareを一体化。ERC INFUSEDはultra-scaled PCMでfast/slow weight dynamicsを扱う | MemVerse group、学生project、internship、PhD、NEQIOS/Hybrain PI/Co-PI、公開emailを研究者ページに掲載 | PCM、electro-photonic IMC、assisted regeneration、system integration | **確認**: [IBM profile](https://research.ibm.com/people/ghazi-sarwat-syed), [IBM INFUSED news](https://research.ibm.com/blog/ibm-researchers-win-prestigious-european-grants) |

**読み取り:** この系統はLumenLatchに最も近いが、現在の公開用途は汎用1-bit latchよりAI／neuromorphic／reconfigurable computeが中心である。接触時は「新しい汎用CPU」ではなく、**PCM read outputを次段write/controlへ接続するreference-plane problem**として質問する方が既存研究と接続しやすい。

### 2. 光論理・光トランジスタを作る系統

| 主体 | 公開情報で確認できる方向 | LumenLatchとの接点 | 証拠状態 |
|---|---|---|---|
| IBM / Thilo Stöferle | 強結合光–物質系、exciton-polariton condensation、室温・超高速all-optical transistor、結合HCG microcavity array、nanophotonic source | Seeded condensationのthreshold、gain、signal suppressionを使うregenerator候補 | **確認**: [IBM profile](https://research.ibm.com/people/thilo-stoferle), [IBM Photonic Computing](https://research.ibm.com/projects/exploratory-photonics), [2026 transistor publication](https://research.ibm.com/publications/integrated-ultrafast-all-optical-polariton-transistors-with-sub-wavelength-grating-microcavities) |

**読み取り:** この系統はPCMの保持層ではなく再生器層に近い。現行素子は光励起polariton condensationであり、通信波長、CW動作、電気駆動、fiber coupling、寿命、熱、歩留まりは別途検証が必要である。IBM公式ではPoLLoCは2023年終了で、現行project listにはCHIP-QD等が掲載されている。外部検索で現れた“PolArt”をStöferleのprojectとして帰属させない。

### 3. 光AIアクセラレータ系統

| 研究者・組織 | 公開情報で確認できる方向 | 外部energy／hybridの扱い | LumenLatchとの接点 | 証拠状態 |
|---|---|---|---|---|
| Dirk Englund / MIT QPAI | Physical AI、photonic neural network、RF-photonic processor、optical tensor core、foundry-compatible programmable photonics。2024年にはsingle-chip DNNでon-chip nonlinearityとforward-only trainingへ進展 | 完全受動への純化ではなく、光の線形処理、chip内nonlinearity、electronic controlをsystemとして統合 | WDM、hybrid photonic-electronic architecture、学習可能な判定・等化、system benchmark | **確認**: [MIT QPAI](https://qp.mit.edu/), [2024 single-chip DNN](https://www.nature.com/articles/s41566-024-01567-z) |

**読み取り:** LumenLatchにとって重要なのは、光だけを残すことではなく、光の伝送・parallelismと電子のdecision／controlを機能分担し、全体で測る姿勢である。

### 4. 実用化をまず光interconnectから進める企業系統

| 組織 | 現在の公式focus | 試作・製品化シグナル | LumenLatchとの接点 | 証拠状態 |
|---|---|---|---|---|
| Lightmatter | “Photonic interconnects that scale AI supercomputers”。PassageをNPO/OBOから2D/3D CPO、3D interposerまでのroadmap、Guideをlarge-scale light sourceとして提示 | EVK、M1000 reference platform、wafer-to-rack manufacturing、AI infrastructure partner ecosystemを公開 | Dense optical routing、source distribution、packaging、system energy。現在の勝ち筋がcompute置換よりI/Oであるという実例 | **確認**: [Lightmatter](https://lightmatter.co/) |

**読み取り:** 企業の現在の公開focusは「光CPUで電子を全置換」ではなく、AI clusterのelectrical I/O制約をphotonic interconnectで解くことにある。LumenLatchの短期用途も、chip-to-chip bit transferそのものではなく、低頻度設定を保持するrouting／switch stateから検証する方が現実的である。ただし、現在のLumenLatch監査ではchip-to-chip通信用途自体は不利判定であり、機能境界を混同しない。

### 5. 材料・製造・集積基盤を作る系統

| 組織 | 公開情報で確認できる方向 | Access | LumenLatchとの接点 | 証拠状態 |
|---|---|---|---|---|
| imec | Next-generation silicon photonics、Si PIC prototyping/volume production、SiN photonics、heterogeneous integration | Contact窓口とplatform serviceを公開。**標準公開platform上のPCM integration条件は今回未確認** | Low-loss routing、heterogeneous integration、process control、volume path | **確認**: [imec integrated photonics](https://www.imec-int.com/en/integrated-photonics)。PCM-on-platform availabilityは**NR** |
| E/PCOS | Phase-change material/memory、OTS、selector-only memory、phase-change photonics、plasmonics、neuromorphic/in-memory computingの国際community。2026年はLeuvenで開催 | Conference email、speaker、committee、program routeを公開。Imecはsponsorで現地委員にimec所属者 | PCM材料研究者への横断的接触、PCM追加工程partner探索 | **確認**: [Call for abstracts](https://epcos2026.be/call-for-abstracts/), [Committees](https://epcos2026.be/committees/), [Sponsors](https://epcos2026.be/sponsors/) |

**読み取り:** imecを「PCM光セルをすぐMPWで作れる場所」とはまだ扱えない。公開platformでできるSi/SiN部分と、bilateral/customになる可能性が高いPCM integrationを分離して問い合わせる必要がある。

## 日本の接点

| 研究者・組織 | 本当に狙っている用途 | 装置・基盤 | LumenLatchとの接点 | 接触／再現性 | 証拠状態 |
|---|---|---|---|---|---|
| 京都大学 野田進 / PCSEL Research Center | High-power・high-beam-quality source、beam/polarization/direction control、industrial transfer | Photonic crystal、PCSEL。2024年12月に大学と産業を橋渡しするcenterを設立 | Efficient local source、cavity、beam delivery。PCM memoryそのものではない | 共同研究、device fabrication、PCSEL素子の有償提供、装置利用支援を公式に案内 | **確認**: [About](https://ku-pcsel-center.or.jp/gaiyou), [事業内容](https://ku-pcsel-center.or.jp/ja/jigyo) |
| 東京大学 竹中充研究室 | AI向けprogrammable PIC、LSI optical I/O、heterogeneous Si photonics | SiにIII-V、Ge、2D materialsを統合。Device/circuit/systemを横断 | Hybrid regenerator、photodetector/modulator、programmable routing、将来のPCM integration | Lab website経由。専用加工またはfoundry/shared facilityが必要 | **確認**: [UTokyo faculty page](https://www.eeis.t.u-tokyo.ac.jp/en/staff/takenaka-mitsuru/) |
| 東京大学 種村拓夫研究室 | Beam steering/imaging、photonic unitary processor、machine-learning optical circuits | Large-scale phase shifter array、integrated photonics、metasurface | Low-loss routing、unitary network、readout/beam control。Memory/repeaterは直接targetではない | Lab website経由。Integrated sampleは共同設備が必要 | **確認**: [UTokyo faculty page](https://www.eeis.t.u-tokyo.ac.jp/en/staff/tanemura-takuo/) |
| André Röhm / UTokyo Information Photonics Lab | Physical deep learning、delay/reservoir/laser network、digital twin、remote training | Laser dynamics、physical neural network、training/error model | Q proxy校正、noise tolerance、network-level experiment design | 特任准教授、公開emailあり。Fabではなくmodel/digital-twin側で接続 | **確認**: [Members](https://www.infotonics.ipc.i.u-tokyo.ac.jp/Member.html?lang=en), [Research](https://www.infotonics.ipc.i.u-tokyo.ac.jp/Research.html?lang=en), [Conferences](https://www.infotonics.ipc.i.u-tokyo.ac.jp/Conference.html?lang=en) |

## 接触優先順位

| 優先 | 相手 | 最初に聞く内容 | 理由 |
|---:|---|---|---|
| 1 | Pernice Lab | Existing PCM sample/trace、read-to-write compatibility、cascade/restoration、共同測定または学生project化 | PCM neuromorphic photonicsの具体的学生テーマと、chip-to-packageの試作能力が公開されている |
| 2 | Ghazi Sarwat Syed / IBM | PCM read outputのreference plane、raw waveform、fast/slow state、electro-photonic assisted cascade | 電子・光PCMとdevice-to-systemを同じgroupで扱い、公式emailがある |
| 3 | Bowei Dong / A*STAR IME | Two-node PCM experiment、electronics-photonics integration、existing test chip／raw trace、fab route | Deviceからarchitectureと200/300 mm試作へ接続できる |
| 4 | Oxford ANE group leads | Bhaskaran不在中のPCM/plasmonic activity、sample/data route、field-programmable couplerとの接点 | PCM cellの発祥系譜だが、公式ページが問い合わせをgroup leadsへ誘導している |
| 5 | 竹中充研究室 | O/E/Oまたはelectrically assisted optical regeneratorの最小test structure、heterogeneous integration | 日本国内でhybrid integrationとAI PICをdevice/circuit/system横断で扱う |
| 6 | André Röhm | Measured noise traceからQ proxyをreal-noise model／digital twinへ置き換える共同設計 | Fabなしで着手でき、BER校正とremote trainingへ直結する |
| 7 | Thilo Stöferle / IBM | Seeded polariton transistorのinput/output plane、fan-out、pump/thermal ledger | Regenerator物理への最短接点だが、PCMとの接続には波長・駆動・寿命のgapがある |
| 8 | 野田PCSEL Center / 種村研究室 | Source/cavity/routingの個別課題 | LumenLatch成立後のsource・routing層には重要だが、最初のcascade proofからは一段遠い |

## 最安で検証価値が高い次の一手

### 推奨: 「実測trace取得＋replay assisted-cascade」

新しい2-cell maskを最初から作らず、**既存PCM cellの実測read waveformを取得し、その情報を保持したまま外部energyで次段write/controlへ接続できるか**を検証する。

#### Phase A — Data request（最低cost）

上位4研究室へ[共通1-page request](collaboration_request.md)を送り、可能なら匿名化・downsample済みでもよいので次を求める。

1. PCM stateごとのread output waveformまたはtrial-level power trace
2. 出力reference plane（PCM直後、waveguide、coupler、detector等）
3. 次cell write thresholdの分布とpulse-width dependence
4. Coupler、waveguide、splitter、detectorのloss ledger
5. Temperature、read disturb、write error、retention条件
6. Local pump/biasを使った場合のstatic/dynamic energy boundary

これだけで現行モデルの最大の空欄である`前段read output -> 次段write threshold`のmarginを、架空のbest deviceを作らず評価できる。

#### Phase B — Trace replay（低cost、no new fab）

実測traceをAWG/EOMまたはdigital hardware-in-the-loopで再生し、次の3枝を同じ入力で比較する。

- Passive propagation
- All-optical gain／limitingを仮定した枝
- Photodetector + comparator/driver + EOMによるO/E/O枝

測るものはthreshold crossing率、noise margin、latency、必要gain、event failure、static/dynamic energy ledgerである。この段階は**実PCM二段実証ではない**が、どのregenerator classだけが次cell driveを成立させ得るかを安価にfalsifyできる。

#### Phase C — Existing chip上のconditional two-node test（中cost）

既存chip上に独立PCM regionが2つある場合、stage 1の情報-bearing read outputでlocal pump/biasをgateし、stage 2を書き換える。完全受動を要求せず、外部energyと情報経路を分離して記録する。

### Cost/value順位

| 順位 | 検証 | 新規fab | 検証できること | 検証できないこと | 相対cost |
|---:|---|---|---|---|---|
| 1 | Raw-data request + reference-plane audit | 不要 | 受動cascadeのenergy margin、必要gainの下限 | Hardwareのrestoration | 最低 |
| 2 | Trace replay assisted-cascade | 不要 | Regenerator class、noise margin、latency、energy accounting | PCM二段の物理動作 | 低 |
| 3 | Existing chipのtwo-node conditional test | 原則不要 | 情報保持＋外部energyによる実stage-2 write | Wafer-scale variation | 中 |
| 4 | Custom integrated two-cell test vehicle | 必要 | Link loss、thermal cross-talk、同種二段 | Large-array yield | 高 |
| 5 | Multi-stage/array tapeout | 必要 | BER、fan-out、yield、calibration | — | 最高 |

ここでの相対costは、laser、detector、AWG/EOM、oscilloscopeを共同利用できる前提である。利用設備がない場合は、Phase Bをdigitized traceのsoftware replayから始め、部品購入前に必要bandwidth、dynamic range、gain、latencyを確定する。

**結論:** 最初に買うべきものはmask setではなく、正しいreference planeのraw traceである。最初の物理実験は「完全受動2-cell」ではなく、既存cellと市販regeneratorを使ったconditional two-node testが最もcost/value比がよい。

## Go / No-Go条件

次のどれかが成立したらcustom two-cellへ進む。

- 実測read traceと次cell thresholdの間に、現実的なlink lossを入れても再生可能なmarginがある
- O/E/Oまたはall-optical regeneratorを含むtotal energy/latency ledgerが対象用途のdutyで成立する
- Trial-level traceから校正したerror modelが、二段測定へ進む価値のあるfailure probabilityを示す

次の場合はpassive PCM latch pathを止め、routing/weight-holding用途へ限定する。

- Read output reference planeからwrite thresholdまでの不足が、fan-out 1でも現実的gain/heat budgetを超える
- Threshold variation／thermal driftがregenerator後もmarginを消す
- Required write dutyがenduranceまたはstatic heatを用途上許容できない

## 公式情報ソース

- [Oxford: Harish Bhaskaran profile](https://www.materials.ox.ac.uk/peoplepages/bhaskaran.html)
- [Oxford Advanced Nanoscale Engineering](https://nanoeng.materials.ox.ac.uk/)
- [Heidelberg: Pernice Lab](https://www.kip.uni-heidelberg.de/photon/)
- [A*STAR: Bowei Dong](https://research.a-star.edu.sg/researcher/bowei-dong/)
- [A*STAR 2024: To build a light-speed data highway](https://research.a-star.edu.sg/articles/highlights/light-speed-data-highway/)
- [A*STAR IME: Fab services](https://www.a-star.edu.sg/ime/rndfoundry)
- [A*STAR interview: Computing at the speed of light](https://research.a-star.edu.sg/articles/features/computing-at-the-speed-of-light/)
- [IBM Research: Ghazi Sarwat Syed](https://research.ibm.com/people/ghazi-sarwat-syed)
- [IBM Research: INFUSED ERC grant](https://research.ibm.com/blog/ibm-researchers-win-prestigious-european-grants)
- [IBM Research: Thilo Stöferle](https://research.ibm.com/people/thilo-stoferle)
- [IBM Research: Photonic Computing](https://research.ibm.com/projects/exploratory-photonics)
- [MIT QPAI](https://qp.mit.edu/)
- [MIT/Nature Photonics: Single-chip photonic DNN](https://www.nature.com/articles/s41566-024-01567-z)
- [Lightmatter](https://lightmatter.co/)
- [imec Integrated Photonics](https://www.imec-int.com/en/integrated-photonics)
- [E/PCOS 2026 Call for Abstracts](https://epcos2026.be/call-for-abstracts/)
- [Kyoto University PCSEL Research Center: 事業内容](https://ku-pcsel-center.or.jp/ja/jigyo)
- [UTokyo: Mitsuru Takenaka](https://www.eeis.t.u-tokyo.ac.jp/en/staff/takenaka-mitsuru/)
- [UTokyo: Takuo Tanemura](https://www.eeis.t.u-tokyo.ac.jp/en/staff/tanemura-takuo/)
- [UTokyo Information Photonics Lab: André Röhm](https://www.infotonics.ipc.i.u-tokyo.ac.jp/Member.html?lang=en)

## 調査上の未解決

- Bowei Dongの2025年講演内容は、今回取得できたA*STAR公式ページだけでは詳細を直接確認できていない。
- Imecの公開Si/SiN platformでPCM deposition/integrationが標準提供されるとは確認できていない。
- 求人テーマは更新が速い。Contact前に各official positions pageを再確認する。
