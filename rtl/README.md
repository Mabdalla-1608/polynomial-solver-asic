# RTL source

| File | Contents |
|---|---|
| `polynomial_cfg.vhd` | Package with the assigned coefficients (`a = 10`, `b = 4`, `c = 9`, `d = 2`) and bus widths (`in_bits = 6`, `out_bits = 24`). |
| `polynomial_top.vhd` | Top-level entity `polynomial_top`. It wraps each input in a `PADDI` pad and each output in a `PADDO` pad, and instantiates the `polynomial` core with the config constants as generics. |

The core evaluates `y = a + b·x + c·x² + d·x³` (here `2x³ + 9x² + 4x + 10`). See [../docs/polynomial.md](../docs/polynomial.md).

## Missing files

- **`polynomial.vhd` (the core):** the report section with this name repeats the top-level wrapper, so the core architecture was not recovered.
- **`polynomial_top_tb.vhd` (the testbench):** the report section repeats the wrapper too.

These are needed before the RTL can compile on its own. `PADDI` and `PADDO` are I/O cells from the gpdk45 pad library and are not described in VHDL here. Until the core is recovered, [`../model/polynomial_model.py`](../model/polynomial_model.py) gives the expected output for every input.
