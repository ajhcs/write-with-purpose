# Blind reader validation

## Real public data

Local headless Chromium passed 58 grouped checks, including all 16 comparisons at 1024, 736, and 320 CSS pixels (48 case-width combinations), all four whole-work cases, and a fenced-code case. Checks covered blank initial ratings and comments, readable and responsive columns, context visibility and expansion, eight public license links, safe source HTML handling, mocked state restoration, and a mocked send payload containing the trial identity and exact comment. The public JSON matched the JSON embedded in the tested fragment.

One initial 320-pixel overflow was traced to the comparison selector's intrinsic width; the grid was constrained and all 48 combinations passed on rerun. Host APIs were mocked: real-host persistence and message delivery are not established. No reviews were actually sent.

Tested SHA-256:

- Fragment: `9753c91dd9aa6762991edbf277c9e9c89161e32ed4edf0fa4129c32f46466376`
- Public data: `bb960244a79b061b3a604220a280e9e6628258b5afff61be6da8b82e7fae4272`

## State race regression

An isolated host mock reproduced a stale globals event overwriting a newer comment. Snapshots now carry an interaction revision; older or equal stale snapshots do not replace newer local interactions. The synthetic regression passes, as do newer valid restore and trial and schema guards. The prior tested fragment hash before this repair was `86b991d8af55f087b860e8260208827353ba5236edb5013b528a6e6d175c78a4`. The real-data checks were rerun against the final fragment above.

## Synthetic fixture

Separate local browser checks passed for source HTML safety, Markdown heading and list rendering, optional context, blank choices, exact comment handling, state restore, submission, unavailable-host fallback, oversized comment retention, and optional license-link rendering. The license link also passed against all eight applicable public cases.

Run from the repository root with the existing local browser dependencies:

```sh
TMPDIR=/workspace/tmp/builderbob LD_LIBRARY_PATH=/workspace/cache/builderbob/global-tools/browser-deps/sysroot/usr/lib/x86_64-linux-gnu node experiments/blind-longform-2026-11-16/validation/reader-ui-test.js
TMPDIR=/workspace/tmp/builderbob LD_LIBRARY_PATH=/workspace/cache/builderbob/global-tools/browser-deps/sysroot/usr/lib/x86_64-linux-gnu node experiments/blind-longform-2026-11-16/validation/reader-real-data-test.js
```
