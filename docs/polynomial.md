# The polynomial

## Result

$$y = 2x^3 + 9x^2 + 4x + 10$$

In the generic form used by the design, `y = a + b·x + c·x² + d·x³`, with the coefficients from [`rtl/polynomial_cfg.vhd`](../rtl/polynomial_cfg.vhd):

| Generic | Value | Role |
|---|---:|---|
| `a` | 10 | constant term |
| `b` | 4 | coefficient of `x` |
| `c` | 9 | coefficient of `x²` |
| `d` | 2 | coefficient of `x³` |
| `in_bits` | 6 | width of `x` (0–63) |
| `out_bits` | 24 | width of `y` |

The coefficients were assigned per student on the course's "Assigned Polynomial Coefficients" page.

## How this was confirmed

The source of the polynomial core is missing (see the main [README](../README.md)), so the config package alone does not say which coefficient goes with which power of `x`. The obvious guess, `a·x³ + b·x² + c·x + d`, is **wrong**: it gives `y(2) = 116`, but the simulation shows 70.

Instead, the formula was recovered from the simulation outputs:

1. The ModelSim waveform shows `x = 1…10 → y = 25, 70, 157, 298, 505, 790, 1165, 1642, 2233, 2950`, and the Virtuoso transient shows `x = 0 → y = 10`.
2. The third differences of these values are constant (12), so `y` is a cubic with leading coefficient 12 / 3! = 2.
3. A least-squares cubic fit gives exactly `[2, 9, 4, 10]`.
4. The resulting formula reproduces all 11 observed values with no error.

That puts `a` on the constant term and `d` on `x³`, so the core evaluates the polynomial in ascending powers of `x`.

To re-run the check:

```bash
python model/polynomial_model.py          # verifies the 11 observed values, prints x = 0..10
python model/polynomial_model.py --all    # full table for x = 0..63
```

## Output range

| x | y |
|---:|---:|
| 0 | 10 |
| 15 | 8,845 |
| 31 | 68,365 |
| 63 | 536,077 |

`y(63) = 536,077` fits in 20 bits, leaving 4 bits of headroom on the 24-bit output.
