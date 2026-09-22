# Audit

Dated log of editorial passes and verification runs. Newest first.

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
