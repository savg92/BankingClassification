from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]


def test_phase0_scaffold_is_present() -> None:
    expected_paths = [
        ROOT / "pyproject.toml",
        ROOT / "README.md",
        ROOT / ".env",
        ROOT / ".env.example",
        ROOT / "apps" / "backend" / "pyproject.toml",
        ROOT / "apps" / "backend" / "main.py",
        ROOT / "apps" / "frontend" / "package.json",
        ROOT / "training" / "pyproject.toml",
        ROOT / "training" / "notebooks",
        ROOT / "training" / "cache",
    ]

    for path in expected_paths:
        assert path.exists(), f"Missing required scaffold item: {path}"


def test_backend_scaffold_uses_fastapi() -> None:
    main_py = (ROOT / "apps" / "backend" / "app" / "main.py").read_text(encoding="utf-8")
    assert "FastAPI" in main_py
    assert "@app.post(\"/analyze\"" in main_py


def test_frontend_scaffold_uses_vite_react_ts() -> None:
    package_json = json.loads(
        (ROOT / "apps" / "frontend" / "package.json").read_text(encoding="utf-8")
    )
    assert package_json["scripts"]["dev"] == "vite"
    assert package_json["dependencies"]["react"].startswith("^")
    assert package_json["dependencies"]["react-dom"].startswith("^")