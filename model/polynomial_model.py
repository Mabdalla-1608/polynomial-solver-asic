"""Reference (golden) model for the polynomial solver ASIC.

The chip computes

    y = a + b*x + c*x^2 + d*x^3

with the coefficients assigned in rtl/polynomial_cfg.vhd:
a = 10, b = 4, c = 9, d = 2  ->  y = 2x^3 + 9x^2 + 4x + 10

x is a 6-bit unsigned input (0..63) and y is a 24-bit unsigned output.

Run this script to:
  * check the model against every output value visible in the ModelSim and
    Virtuoso simulation screenshots in assets/screenshots/, and
  * print the expected output for every input (useful when writing a testbench).

Usage:
    python model/polynomial_model.py           # check + short table
    python model/polynomial_model.py --all     # check + full 0..63 table
"""

import sys

# Values from rtl/polynomial_cfg.vhd
A, B, C, D = 10, 4, 9, 2
IN_BITS, OUT_BITS = 6, 24


def polynomial(x: int) -> int:
    """Expected chip output for input x."""
    if not 0 <= x < 2**IN_BITS:
        raise ValueError(f"x must fit in {IN_BITS} bits (0..{2**IN_BITS - 1})")
    return A + B * x + C * x**2 + D * x**3


# Input -> output pairs read off the simulation screenshots.
OBSERVED = {
    # assets/screenshots/modelsim-functional-simulation.png (RTL simulation)
    1: 25, 2: 70, 3: 157, 4: 298, 5: 505,
    6: 790, 7: 1165, 8: 1642, 9: 2233, 10: 2950,
    # assets/screenshots/functional-simulation-2.png (Virtuoso transient, x = 2, 3, 1, 0)
    0: 10,
}


def main() -> int:
    bad = {x: (y, polynomial(x)) for x, y in OBSERVED.items() if polynomial(x) != y}
    if bad:
        for x, (seen, want) in sorted(bad.items()):
            print(f"MISMATCH x={x}: simulation shows {seen}, model gives {want}")
        return 1
    print(f"Model matches all {len(OBSERVED)} simulated values.")

    y_max = polynomial(2**IN_BITS - 1)
    print(f"Largest output: y(63) = {y_max} ({y_max.bit_length()} of {OUT_BITS} output bits used)")

    xs = range(2**IN_BITS) if "--all" in sys.argv else range(11)
    print("\n  x |        y")
    print("----+----------")
    for x in xs:
        print(f"{x:3d} | {polynomial(x):8d}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
