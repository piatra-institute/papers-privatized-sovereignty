# Privatized Sovereignty

A Stratigraphy of Control Without Exposure. The paper treats the founder-controlled public corporation as a fossil of an order losing its capacity for correction. The diagnostic quantity is the wedge between voting control and economic exposure, verified from the 2026 primary filings: a founder at 82.4 percent of the vote on roughly 46 percent of the shares at the June 2026 SpaceX listing, a public class with no vote at Snap, a charter constant of 49.999999 percent at Palantir, a family class holding 40 percent of the vote on 1.8 percent of the shares at Ford. The formal result is self-financing entrenchment: below a threshold stake, 0.42 in the model, a controller rationally keeps control that destroys firm value, and the smaller the stake, the cheaper the retention. Three built mechanisms carry the argument. A lifecycle model calibrated to the documented 6-to-9-year fade of the dual-class premium finds the insulation advantage crossing zero at 7.1 years, the perpetual wedge destroying 0.53 units of 25-year value while a renewable sunset gains 0.67. An exchange-competition model reproduces the documented shape of normalization: 61 years of holdout under low founder demand, defection 7 years after the demand shift, a federal floor that binds until removed, and a permissiveness ratchet ending at 20-to-1 classes with no sunset, where London and Hong Kong arrived in 2024 and 2026. A correction model comparing 5 control architectures under an identical controller failure finds the sealed wedge best in normal times and worst in the tail, with 39 percent of failure episodes reaching irrecoverable damage, and finds transparency without removability recovering 12 percent of the damage where removability recovers 46. The comparison with Singapore, China, Japan, Korea, and India shows hierarchy everywhere and pathology only where hierarchy is protected from correction.

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

Requires `pandoc` and `xelatex` on PATH. From the workspace you can also run
`papers build privatized-sovereignty`.

Part of [piatra-papers](https://github.com/piatra-institute). See the workspace
docs for the research and writing pipelines.
