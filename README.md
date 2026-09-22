# Privatized Sovereignty

A Stratigraphy of Control Without Exposure.

In June 2026 the largest aerospace firm in the world sold shares to the public while its founder retained 82.4 percent of the vote through a class of stock that also elects a majority of the board (Space Exploration Technologies, 2026). We treat the founder-controlled public corporation as a well-documented case of lost self-correction, measured by the wedge between voting control and economic exposure. In a simple model the wedge finances its own persistence: a controller whose economic stake is below 0.42 rationally keeps control that destroys firm value, because the private benefits of control exceed the controller's share of the loss, and the Ford family's stake of 0.018 lies a factor of 24 inside that threshold. A lifecycle model calibrated to the documented 6-to-9-year fade of the dual-class premium places the crossover at 7.1 years; over 25 years a perpetual wedge loses 0.53 units of value against a single-class baseline while a renewable sunset gains 0.67. A model of competition among listing venues reproduces 61 years of holdout under low demand and a ratchet ending at 20-to-1 share classes without sunset, where London and Hong Kong arrived in 2024 and 2026. A correction model comparing 5 control architectures under identical controller failure finds the sealed wedge best in normal times and worst in failure, reaching irrecoverable damage in 39 percent of episodes against at most 0.45 percent where controllers can be removed; transparency alone recovers 12 percent of the damage and removability 46 percent. Comparison with Singapore, China, Japan, Korea and India locates the pathology in hierarchy protected from correction.

## Simulation

```bash
cd simulation
uv run run_all.py        # -> output/results.json + output/figures/*.png
```

Mechanisms 1 and 2 are expected-value arithmetic; mechanism 3 runs on a recorded seed, bit-for-bit reproducible. Thirty-four invariant checks fail the run loudly if broken, among them: the crossover landing inside the documented window, the renewable sunset's rank over hard sunset and perpetuity, the entrenchment threshold with the measured Ford and SpaceX stakes on either side, the holdout surviving flat demand and the floor binding until removed, the ratchet's monotonicity, the sealed wedge's twin extremes, and the transparency-versus-removability decomposition. The verified filing figures enter results.json as cited records with sources.

## Build

```bash
uv run build.py          # -> paper/PAPER.pdf  (vendored canonical recipe)
```

Requires `pandoc` and `xelatex` on PATH. From the workspace you can also run `papers build privatized-sovereignty`.

Part of [piatra-papers](https://github.com/piatra-institute). See the workspace docs for the research and writing pipelines.
