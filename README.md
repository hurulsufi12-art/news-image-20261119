# The World in One Day — 19 November 2026

[![make.fun](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![make.fun](https://make.fun/badge/news-image-20261119/hurulsufi12-art/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![make.fun](https://make.fun/badge/news-image-20261119/hurulsufi12-art/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119)

A newspaper front page that sums up the world news of **Thursday, 19 November 2026** in one image (1024×1024 PNG).

- **Lead:** GTA VI launches today — Grand Theft Auto VI begins its global rollout; gamers enter Vice City after a 13-year wait since GTA V.
- Trump, Xi and Putin meet in Shenzhen during APEC — their first trilateral summit.
- Democrats nominate Hakeem Jeffries for Speaker — he would be the first African-American Speaker.
- US–Iran fire continues — Iran widens attacks to Kuwait and Bahrain after the US struck a missile site on Qeshm Island.
- Cyclone Akvan nears India's east coast — landfall expected between Machilipatnam and Puri.
- The EU proposes a €45 billion loan to Ukraine, to be repaid after Russia pays reparations.
- Also: NASA's Voyager 1 passes the one-light-day mark today; Fed minutes — most officials expect further rate hikes; Moldova summons the Russian envoy over drone incursions; Australia sanctions Israeli settlers; Pew — Islam on track to be the world's largest religion by 2035.

Everything in the image is drawn with code (see `draw.py`); no photographs and no AI-generated imagery, so no text is ever garbled.

## Files

- `entry.png` — the image (1024×1024, under 1 MiB)
- `main.py` — Python 3.13, standard library only; copies `entry.png` to `$MAKEFUN_OUTPUT_DIR` (or `/output`)
- `draw.py` — the Pillow script that drew `entry.png` deterministically (build-time provenance only; not run by the grader)
- `LICENSE` — MIT

## Run it

```bash
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Two runs write byte-identical files.
