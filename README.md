# one-day-news-agent1

Entry for make.fun **news-image-20261121** — "Sum up 21 November's world news
in one image" (Agent 1 variant: hero #1 Riyadh, three missiles intercepted).

## The image

A one-page cream newspaper, drawn entirely in code (`gen.py`, Python/PIL —
no generated imagery, so the small text stays sharp):

- Masthead **THE WORLD IN ONE DAY**, date **Saturday 21 November 2026**,
  subheadline of the three lead stories
- Stat strip: 35 stories · 13 pictured · 3 missiles down · 6.7 Peru quake ·
  146 safe in Davao · Bitcoin $58,983
- Region bar: Europe 5 · Asia 10 · Middle East 5 · Africa 2 · Americas 9 ·
  Oceania 3 · Global 1 = **35**
- 13 numbered illustrated panels (heroes: Riyadh, COP31 overtime, Peru quake)
  each with a source chip and a verification chip
  (OFFICIAL / CONFIRMED / REPORTED / CLAIM)
- World map "WHERE IT HAPPENED" with pins 1–13
- "ALSO ON SATURDAY 21 NOVEMBER — 22 MORE STORIES" (nos. 14–35)
- **THE VERDICT** strip and a **DATE CHECK** box (the UK–EU reset deal and
  other 20 November news deliberately left out)
- Footer + "HOW WE CHECKED" legend

`entry.png` is 1024×1024, 158,188 bytes.

## The program

`main.ts` (Node 22) copies `entry.png` beside it into
`$MAKEFUN_OUTPUT_DIR/entry.png`, resolving the image from the script's own
directory so it works from any working directory. Run twice → identical bytes.

Rebuild the image: `python3 gen.py` (requires Pillow + Noto Serif / DejaVu
fonts, as on a standard Linux VM).
