# LumenLatch: Request for One Representative PCM Input/Output Trace

## 1. Research question

Can the information-bearing output of one optical memory cell reliably control or write the next stage—allowing the minimum necessary optical pump or electrical bias—while preserving logic level, extinction ratio, fan-out, error margin, total energy, and thermal feasibility across multiple stages?

LumenLatch is an early-stage, non-commercial personal research project on cascadable optical 1-bit cells. It is not presented as a completed device or as a replacement for existing photonic-computing architectures.

## 2. What prior work already establishes

Published integrated-photonic PCM work has demonstrated optical writing, optical reading, multilevel nonvolatile storage, and retention at the single-cell level. Other optical devices have demonstrated gain, nonlinear switching, and level restoration under different material and pumping conditions.

The project treats the reported 13.4 pJ PCM write value as energy absorbed at the PCM—not as laser wall-plug or system energy. Its current `Q proxy` and Monte Carlo `error_rate` are sensitivity-model outputs, not measured BER.

## 3. The unresolved point

I have not found a demonstration in which the measured output of one PCM cell, at a clearly defined reference plane, drives the nonvolatile write or control operation of a same-type next PCM cell.

The immediate question is therefore narrower than fabricating a new multi-stage chip:

> Is there measurable margin between a real cell's read-output waveform and the input threshold of a next-stage write or externally powered regenerator?

## 4. Minimum data requested

One representative operating condition from an existing experiment would already be useful. A complete raw dataset is not required.

Preferred minimum trace:

- input pulse waveform;
- output pulse waveform;
- time axis and units;
- optical power, energy, or normalized intensity;
- reference plane before and after the device;
- device state or transition represented;
- optical pump and/or electrical-bias condition;
- measurement bandwidth or detector/oscilloscope bandwidth;
- if readily available, extinction ratio and noise floor.

A simple CSV with columns such as `time`, `input`, and `output` is ideal. A MAT/HDF5 file, downsampled trace, or digitizable representative figure is also sufficient. Optional but valuable metadata include waveguide/coupler loss, pulse width, temperature, trial count, and the write-threshold distribution.

## 5. Intended use

The trace would be used to:

1. reconstruct the input/output reference planes and link-loss budget;
2. estimate the gain, bandwidth, extinction ratio, and noise margin needed for a next stage;
3. compare passive propagation, all-optical regeneration, and O/E/O regeneration using the same measured input;
4. separate dynamic event energy from pump, bias, standby, and thermal-control power; and
5. decide whether a two-cell experiment is justified before proposing new fabrication.

A replay study would be labelled as trace-driven analysis, not as a physical two-cell demonstration. Results would not be used to claim measured BER or system-energy superiority unless the supplied measurement supports those claims.

## 6. Citation, publication, and confidentiality

For public data, the original paper, authors, DOI, laboratory, and any repository record will be cited. For unpublished data, I will not redistribute the trace, identify unpublished device details, or publish derived results without the provider's written permission. Aggregate or redacted analysis can be used instead if agreed in advance. I am also willing to work under reasonable attribution, embargo, or confidentiality terms specified by the provider.

No commercial use, model training for resale, or transfer to a third party is intended.

## 7. Project context

LumenLatch is a public, non-commercial personal research project. Its assumptions, limitations, negative results, code, and current evidence map are available here:

- [Research overview](https://github.com/DwarfM42/lumen-latch#readme)
- [Global research landscape and collaboration routes](https://github.com/DwarfM42/lumen-latch/blob/main/research_landscape.md)
- [Model definitions and limitations](https://github.com/DwarfM42/lumen-latch/blob/main/model.md)
- [System-energy boundary audit](https://github.com/DwarfM42/lumen-latch/blob/main/system_energy_audit.md)
- [Primary-source claim map](https://github.com/DwarfM42/lumen-latch/blob/main/sources.csv)

Even a single representative trace—or confirmation that this measurement is unavailable or unsuitable—would materially improve the next research decision.
