# Design flow

The lab took the polynomial solver from RTL to a verified layout with the standard digital ASIC flow. The course tutorial walked through the same steps using an 8×8 add-and-shift multiplier. This project applied them to the custom polynomial instead.

## 1. RTL and functional simulation: ModelSim

- RTL written in VHDL: [`polynomial_cfg.vhd`](../rtl/polynomial_cfg.vhd), [`polynomial_top.vhd`](../rtl/polynomial_top.vhd), plus the polynomial core and a testbench (not recovered).
- The testbench stepped `x` through 0–10 and the waveform was checked against the expected values. See [polynomial.md](polynomial.md).

## 2. Synthesis: Synopsys Design Compiler

- The RTL was mapped onto the **gpdk45 GSCLib** standard-cell library with scripted Design Compiler runs (`check_design`, `compile`), producing a gate-level Verilog netlist plus area and power estimates.

## 3. Place and route: Cadence Innovus 21.17

Steps: import the netlist → floorplan → place the I/O ring from the `.io` file → power planning → placement → pre-CTS timing → clock-tree synthesis (`ccopt_design`) → post-CTS timing → routing → post-route optimisation (`optDesign -postRoute -hold`).

### Timing summaries

| Stage | Check | WNS all (ns) | WNS reg2reg (ns) | WNS default (ns) | TNS (ns) | Violating paths | Paths |
|---|---|---:|---:|---:|---:|---:|---:|
| Pre-CTS | Setup | 0.116 | 0.116 | 5.041 | 0.000 | 0 | 29 |
| Post-CTS | Setup | 0.238 | 0.238 | 5.074 | 0.000 | 0 | 29 |
| Post-CTS | Hold | 0.249 | 0.250 | 0.249 | 0.000 | 0 | 29 |
| Post-route | Setup | 0.821 | 0.821 | 5.712 | 0.000 | 0 | 29 |
| Post-route | Hold | 0.256 | 0.896 | 0.256 | 0.000 | 0 | 29 |

- Design-rule violations (max_cap, max_tran, max_fanout, max_length): **0** at every stage.
- Routing overflow: 0.00% horizontal and vertical.
- Core density: about 0.53%. The die size is set by the pad ring, not the logic, so the core is almost empty.

### I/O pad ring

The pad placement file is [`pnr/polynomial_top.io`](../pnr/polynomial_top.io) (clockwise order):

| Side | Pads |
|---|---|
| Top | `x[5:0]`, VDD, `clock`, `valid_in`, VSS |
| Left | `y[23:18]`, VDDIOR, `reset`, `valid_out` |
| Bottom | `y[17:8]` |
| Right | `y[7:0]`, VSSIOR |
| Corners | 4 × `padIORINGCORNER` |

That is 34 signal pads (6 + 24 + 4 control), 4 supply pads and 4 corner cells.

> Note: in the `.io` file the `padReset` entry is labelled `cell="PADDO"`, while the RTL instantiates it as a `PADDI` input pad. Innovus places pads by instance name, so the label probably had no effect, but it is worth fixing if the flow is re-run.

## 4. Layout import and verification: Virtuoso and Assura

- The routed design was streamed into Cadence Virtuoso to get schematic and layout views.
- Assura **DRC: clean** and **LVS: clean**. Screenshots are in [`assets/screenshots/`](../assets/screenshots/).

## 5. Transistor-level simulation: Virtuoso / Spectre

- A testbench schematic drove the chip's pads, with transient runs longer than 30 clock cycles.
- Inputs 2, 3, 1, 0 gave outputs 70, 157, 25, 10, which match the model.
- A parametric sweep of the clock period found the shortest period that still produced a valid output: **0.777 ns, so f<sub>max</sub> ≈ 1.29 GHz**.
- The SPEF-annotated post-layout comparison could not be run, so no schematic-vs-post-layout delay comparison is available.
