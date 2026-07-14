# 要件と評価カバレッジ

## スコープと証拠区分
光で書込み・保持・読出しを行い、同種次段へ情報を伝える1ビットセルを対象とする。実証値、条件付き実証、simulation assumption、提案target、NRを混同しない。外部pump/biasからのエネルギー補給はトランジスタ型構成として正当に比較し、それ自体を失敗理由にしない。

## 提案受入目標（文献実績ではない）
- `G_cell*T_link/F >= 2`
- 再生出力ER >=10 dB、post-link ER >=6 dB
- 校正済み等分散Gaussian OOKでQ>=6かつBER<1e-9
- 0–70 deg C、threshold shift ±10%、array threshold CV<=5%
- pump、bias、冷却込み平均1 mW/cell以下

## カバレッジ監査
| 要件 | 状態 | 現行評価 | 不足 |
|---|---|---|---|
| temperature 0–70 °C | partial | Q proxy感度sweep | 実測屈折率・吸収・閾値・保持の温度係数 |
| threshold shift ±10% | not evaluated | 温度をQへ直接減点のみ | 閾値対温度の測定曲線とhysteresis |
| array CV <=5% | partial | scalar `threshold_cv` 感度 | ロット/セル相関、分布形、校正後CV、yield |
| fan-out | partial | 受動power splitのみ | splitter excess loss、同時switch、pump depletion、worst-cell threshold |
| post-link ER >=6 dB | partial | 0.08 dB/stage仮定 | 実測ER分布、ASE/RIN/shot noise、detector bandwidth |
| Q/BER | not evaluated | 無次元Q proxyとMonte Carlo failure | real-noise校正、PRBS BER、信頼区間 |
| total energy / heat | partial | PCMイベント＋理想再生器 | system energy modelのunknown実測 |

機能要件は固定seed byte再現、CSV 192行、指定PNG 8枚、Python 3.11/NumPy/Matplotlib/pytestを維持する。
