# ZekeShot 🚀

## Executive Summary
ZekeShot is a pixel Pygame shooter where the user blast upward through waves of enemies to collect even **more** chickens. 

## Demo KPI 📈
![ZekeShot gameplay gif](data/images/demo.gif)

## Value Proposition
* **Optimized rendering pipeline** leveraging `pygame.time.Clock` for consistent 60 FPS.
* **Modular domain model** (Player → Bullet → Enemy) for rapid feature iterations.
* **Plug-and-play asset pack** under `data/`—no extra asset licenses required.

## Prerequisites
| Asset | Minimum Spec |
|-------|--------------|
| **Python** | 3.10 + (tested on 3.11) |
| **Pip** | ≥ 22.x |
| **OS** | macOS, Linux, or Windows 10/11 |

> **Heads‑up:** On macOS you may need to allow the app to receive keyboard focus under **System Settings → Privacy & Security → Input Monitoring**.

## Quick‑Start Playbook
```bash
# 1️⃣ Clone the repo
git clone https://github.com/Zekepeke/Zekeshot.git
cd Zekeshot

# 2️⃣ (Optional but recommended) Create & activate a virtual env
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3️⃣ Install dependencies at scale
pip install -r requirements.txt   # pygame == 2.* and pillow

# 4️⃣ Launch the game and get those chickens 🚀
python src/zekeShot.py
```

### One‑liner (for the impatient)
```bash
python -m pip install --quiet --upgrade pip &&   git clone https://github.com/Zekepeke/Zekeshot.git &&   python Zekeshot/src/zekeShot.py
```

## Runtime Controls
| Key | Action |
|-----|--------|
| **← / →** | Move horizontally |
| **Space** | Shoot upward |
| **Esc** | Pause / return to main menu |

## Folder Structure (TL;DR)
```
Zekeshot/
│
├── data/              # Sprite sheets & sound effects
│   ├── images/
│   └── fonts/
│
├── scores/            # High‑score CSVs (auto‑generated)
├── src/
│   ├── zekeShot.py    # Bootstrapper / game loop
│   └── ...            # Helpers, entities, utils
└── requirements.txt   # Locked dependency versions
```

## Continuous Improvement Roadmap
- [ ] Multiplayer over WebSockets
- [ ] Power‑ups & dynamic level generator
- [ ] CI workflow (GitHub Actions) + automated test coverage badge

## Contributing
We’re always looking for synergy. Fork the repo, create a feature branch, commit with Conventional Commits, and open a PR. We’ll circle back ASAP.

## License
**MIT**—because open‑source innovation thrives when friction is minimal.

---

_A zero‑friction, high‑impact mini‑game dropping straight into your local stack._
