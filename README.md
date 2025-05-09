# ZekeShot 🚀

## Executive Summary
ZekeShot is a pixel Pygame shooter where the user blast upward through waves of enemies to collect even **more** chickens. 

## Demo KPI 📈
![ZekeShot gameplay gif](data/images/demo.gif)



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
