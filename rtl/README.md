# RTL source

- `polynomial_cfg.vhd`: configuration package extracted from the submitted report.
- `polynomial_top.vhd`: top-level wrapper extracted from the submitted report.

The report's `Polynomial.vhd` section is a duplicate of the top-level wrapper, not the missing `polynomial` core. Recover the original core source before treating this RTL set as compilable or complete.
