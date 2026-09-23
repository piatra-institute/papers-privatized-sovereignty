# Audit

Dated log of editorial passes and verification runs. Newest first.

## 2026-09-23 — structured-evidence migration

Structured-evidence migration (references and claims).
- references.yaml: 45 CSL entries. 12 journal articles and 2 NBER working papers matched in Crossref with DOIs; 5 more completed from DOI records (brodsgaard2012, cremers2024, gompers2010, north2009, oecd2014); the 6 corporate filings re-fetched from SEC EDGAR and given their document URLs; the remaining books, law-review articles, statutes, the court case and institutional documents entered by hand (pew2025 and fca2024 re-fetched). Crossref's automatic matches for berle1932 and light2019 were book reviews and for bebchuk2017 the SSRN preprint; replaced by hand. Organisation ids shortened (brt1990, crs2021, cii2018, fca2024, hkex2026, jpx2026, nse2025, oecd2014, korea2025, singapore2020, spacex2026, npc2023, tse2023, laporta1999, brodsgaard2012).
- Bibliographic corrections: masulis2009 author names from upper case; La Porta et al. co-author spelling Lopez-de-Silanes; filings dated to their EDGAR filing dates (Alphabet and Palantir 24 April, Meta 16 April, Ford 27 March 2026).
- Numerical corrections (prose vs results.json): perpetual wedge 25-year loss "0.53" -> "0.52" (0.524829; abstract, lifecycle section, Figure 1 caption, metadata abstract, README); party vertical detection lag "3.7" -> "3.6" years ( /correction/grid/vertical/mean_detect_lag = 3.649903).
- claims.yaml: 71 claims (45 computation, 15 source, 5 interpretation, 3 assumption, 2 definition, 1 normative). Filing figures verified in the EDGAR documents (SpaceX 82.4%, 91.6%, 51% of directors, economic stake 46.4% from prospectus share counts; Snap over 99%, death-or-disability proxy, 2016 non-voting dividend; Meta 60.8% and 99.8%; Alphabet 27.4 + 25.3; Palantir 49.999999%; Ford 40% and 70,852,076 of 4,011,082,261 shares = 1.8%). Pew 73% (1958) and 17% (2025) from the fact sheet; academic claims from Crossref/OpenAlex abstracts (Dyck and Zingales, Masulis et al., Gompers et al., La Porta et al., Brødsgaard, Bae et al., Bertrand et al., Tabakovic and Wollmann).
- Unverified, not bound: Bebchuk and Hirst 21.9%/24.9% (law-review PDF not retrievable); Broadridge 28% retail participation; NSE 50.1% promoter share; HKEX July 2026 thresholds and 20:1; FCA no-sunset/no-cap rule (only the policy statement and its 29 July 2024 date confirmed); CII 2018 seven-year petitions; Cremers et al. 6-to-9-year window (abstract confirms dissipation but not the years); TSE "over 40 percent"; Seligman NYSE dates; Korea and China statutes; Liscow et al. "more than their salaries" (abstract confirms DOT capacity as a cost driver only); Light (2019) blended workforce.
- Execution receipt: run id models (verification/models.json), `uv run python run_all.py`, 34 invariants, results.json reproduced byte for byte.
- metadata claims_target: claim-ledger.

## 2026-09-23 — prose revision

Prose rewritten against the house standards. Headings made descriptive (Introduction, Legal visibility of structural change, The wedge between voting and economic interest, The managerial corporation and one share, one vote, The contractual view and the end of the voting floor, Founder control and the dual-class premium, A lifecycle model of the wedge, Platforms as governing institutions, Index ownership and consent, Competition among listing venues, A model of listing-standard competition, Dimensions of comparison, Five control systems, Institutional decline through selection, A model of correction capacity, Observable correction events, Proposed charter rules, Objections, Falsification, Conclusion, Reproducibility).

Corrections found during the pass:
  - The abstract said sealed-wedge defeat occurs in 39 percent of episodes "against 0 in 250 under architectures that can remove a controller". results.json gives defeat rates of 0.00375 (custodial, 15 of 4,000), 0.0045 (reciprocal) and 0 (vertical). Now "against at most 0.45 percent".
  - The body gave the custodial defeat rate as "1 in 250"; it is 1 in 267 (0.375 percent). Now stated as 0.375 percent (15 of 4,000), with the reciprocal and vertical rates added.
  - Figure 3 printed defeat rates with two decimals, showing the custodial and reciprocal rates as 0.00; now percentages with one decimal.
Values audited and confirmed: entrenchment threshold 0.4167 = B_PRIV/DRAG (closed form); Ford ratio 23.6 (reported as a factor of 24); crossover 7.13 years by bisection; race years are integer model years. results.json unchanged by the figure edits.

## 2026-08-13 — v1, first full draft to publication

Scope: the entire paper, simulation, and evidence base, from the seed chat to publication.

Changes:
  - Sources: 45 entries verified against Crossref, SEC EDGAR, or the live institutional record. The 6 specimen structures fetched from primary filings this session, including the June 2026 SpaceX prospectus (82.4 percent voting, 91.6 percent of Class B, the Class B board provision) and the Ford record-date counts behind the 1.8 percent computation. Seed corrections logged in research.md: the OECD title fixed, the Pew date fixed, the KOSPI drawdown, the Toyota unwind size, and Tata Sons dropped as unverifiable or secondary, Coinbase/DoorDash/Robinhood/Comcast dropped as redundant with verified specimens. The seed's HKEX claim verified and found understated: thresholds halved and the top-tier ratio doubled to 20:1 in July 2026.
  - Simulation design iterations logged: the renewable-sunset rule initially renewed the slow type on a floating-point zero (fixed with a materiality bar, which is also the truer rendering of a renewal vote); the race's first demand curve put the incumbent's defection in 2016 rather than the late 1980s and never tipped the foreign venues (fixed with era-anchored piecewise demand, venue-scale thresholds, and a parallel ratchet); the network architecture initially self-corrected through personal exposure its managers do not have (fixed at alpha 0.03, the point of cross-shareholding being precisely that exposure is reciprocal and corporate rather than personal).
  - Voice: draft came in at 0 errors, 0 review-candidates; "exactly" thinned 3 to 1, carry-family 8 to 4, one 26-sentence run broken with short sentences.

Verification:
  - voice: 0 errors, 0 review-candidates
  - refs: 45 in-text keys, 45 bib entries, 0 missing, 0 unused
  - claims: 252 sim values, 39 decimal claims in prose, 0 without a match
  - build: 17 pages, no missing-character warnings
  - simulation: 34/34 invariants
  - check => PASS
