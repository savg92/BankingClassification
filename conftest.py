from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PATHS = [ROOT, ROOT / "apps" / "backend", ROOT / "training"]

for path in PATHS:
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)