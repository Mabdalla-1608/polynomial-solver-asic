# Polynomial Solver ASIC

A VHDL polynomial-solver design taken from an ECE 403 digital-design / ASIC implementation project. The submitted project report documents functional simulation, an Innovus physical-design flow, Assura DRC/LVS checks, timing summaries, and a post-layout parametric simulation.

> **Repository status:** This is a portfolio scaffold reconstructed from the submitted lab report, not yet a complete, independently reproducible source release. The report contains the configuration package and top-level pad-wrapper source, but the section labelled `Polynomial.vhd` repeats the top-level wrapper instead of containing the polynomial-core implementation. The section labelled `Polynomial_top_tb.vhd` also repeats the wrapper rather than providing a testbench. Those missing source files have deliberately not been fabricated.

## Design configuration

The configuration package in [`rtl/polynomial_cfg.vhd`](rtl/polynomial_cfg.vhd) sets:

| Parameter | Value |
|---|---:|
| `a` | 10 |
| `b` | 4 |
| `c` | 9 |
| `d` | 2 |
| Input width | 6 bits |
| Output width | 24 bits |

The top-level entity in [`rtl/polynomial_top.vhd`](rtl/polynomial_top.vhd) exposes clock, reset, valid-in/valid-out, a 6-bit input bus, and a 24-bit output bus. It instantiates a `polynomial` core and maps signals through `PADDI` and `PADDO` I/O pad components.

**The report does not include the polynomial-core implementation**, so the exact mathematical expression and its internal architecture are not documented here. They should be added only after recovering the original source.

## Implementation and verification flow documented in the report

- VHDL design and ModelSim functional simulation.
- Cadence Innovus placement, clock-tree synthesis, routing, and timing analysis.
- I/O pad integration and pad-ring layout.
- Cadence Virtuoso schematic/layout views.
- Cadence Assura DRC and LVS verification.
- Post-layout parametric simulation.

## Reported results

The report's Innovus timing summaries show **zero violating paths** in the listed pre-CTS setup, post-CTS setup/hold, and post-route setup/hold summaries. The post-route summaries also report 0.00% horizontal and vertical routing overflow.

The report describes a first valid output at approximately **0.777 ns**, corresponding to an estimated frequency of approximately **1.285 GHz**. It also explicitly notes that simulation using SPEF files was not completed, so this figure should be presented as the reported parametric-simulation estimate—not as a fully validated post-layout maximum-frequency signoff result.

## Repository layout

```text
polynomial-solver-asic/
├── README.md
├── rtl/
│   ├── polynomial_cfg.vhd
│   ├── polynomial_top.vhd
│   └── README.md
├── testbench/
│   └── README.md
├── assets/
│   └── screenshots/
│       └── README.md
└── reports/
    └── README.md
```

## Screenshots to add

Replace the suggested image filenames below with your own high-resolution, redacted screenshots:

1. `assets/screenshots/modelsim-functional-simulation.png`
2. `assets/screenshots/innovus-placement.png`
3. `assets/screenshots/innovus-routed-layout.png`
4. `assets/screenshots/assura-drc-clean.png`
5. `assets/screenshots/assura-lvs-clean.png`
6. `assets/screenshots/innovus-timing-summary.png`
7. `assets/screenshots/virtuoso-layout.png`

Use screenshots that show your own work and remove personal identifiers, account names, machine paths, and any restricted course/PDK information before publishing.

## Reproducing the design

A complete reproduction is **not currently possible from the files in this repository**. Before adding simulation instructions or claiming the repository is runnable, recover and review:

- The actual `polynomial` core VHDL source.
- The actual VHDL testbench.
- Any permitted simulation scripts or setup notes needed to compile the design.

Do not upload university-provided PDKs, standard-cell libraries, proprietary technology files, or the lab manual. Check the course/university rules before publishing assignment source code publicly.
