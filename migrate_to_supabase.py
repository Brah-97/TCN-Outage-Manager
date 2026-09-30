"""One-time import of the local data files into Supabase.

    python migrate_to_supabase.py            # refuses if outages already has rows
    python migrate_to_supabase.py --replace  # wipes the Supabase tables and re-imports

Reads SUPABASE_URL / SUPABASE_KEY from .streamlit/secrets.toml (or the
environment). Run supabase_schema.sql in the Supabase SQL Editor first.
The local files are only read, never modified, and stay as a backup.
"""

import importlib.util
import json
import os
import sys
import tomllib
import warnings
from pathlib import Path

import pandas as pd

warnings.filterwarnings("ignore")
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))

import db  # noqa: E402


def load_credentials():
    secrets = BASE_DIR / ".streamlit" / "secrets.toml"
    url = key = None
    if secrets.exists():
        with open(secrets, "rb") as f:
            conf = tomllib.load(f)
        url, key = conf.get("SUPABASE_URL"), conf.get("SUPABASE_KEY")
    url = url or os.environ.get("SUPABASE_URL")
    key = key or os.environ.get("SUPABASE_KEY")
    if not (url and key) or "your-project" in url or key.startswith("paste-"):
        sys.exit("SUPABASE_URL / SUPABASE_KEY are not set. Fill in .streamlit/secrets.toml first.")
    return url, key


def load_app_module():
    """Import app.py without running the Streamlit UI (reuses its parsers)."""
    spec = importlib.util.spec_from_file_location("tcn_app", BASE_DIR / "app.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def step(label, fn):
    print(f"  {label:<34}", end="", flush=True)
    result = fn()
    print(f"{result:>6,} rows")
    return result


def main():
    replace = "--replace" in sys.argv
    url, key = load_credentials()
    db.configure(url, key)

    print(f"Supabase: {url}")
    try:
        existing = db.count("outages")
    except Exception as exc:
        sys.exit(f"Could not reach the 'outages' table ({exc}).\n"
                 "Did you run supabase_schema.sql in the SQL Editor?")
    if existing and not replace:
        sys.exit(f"'outages' already has {existing:,} rows. Nothing imported.\n"
                 "Re-run with --replace to wipe the Supabase tables and import again.")

    # Read everything from the local files first, before touching Supabase
    app = load_app_module()
    outages = pd.read_excel(app.DATA_FILE, sheet_name=0)
    outages.columns = [c.strip() for c in outages.columns]
    users = json.loads(app.USERS_FILE.read_text()) if app.USERS_FILE.exists() else {}
    station_map = pd.read_csv(app.STATION_MAP_FILE).dropna(how="all")
    hierarchy = pd.read_excel(app.HIERARCHY_FILE, sheet_name="Sheet1")
    hierarchy.columns = [c.strip() for c in hierarchy.columns]
    catalog = app.parse_catalog_files()

    print("Importing…")
    step("Outage records", lambda: (db.replace_outages(outages), len(outages))[1])
    step("Station map", lambda: (db.replace_reference("station_map", station_map), len(station_map))[1])
    step("Substation hierarchy", lambda: (db.replace_reference("substation_hierarchy", hierarchy), len(hierarchy))[1])
    step("Equipment catalog", lambda: (db.replace_reference("equipment_catalog", catalog), len(catalog))[1])

    def _users():
        for username, rec in users.items():
            db.upsert_user(username, rec)
        return len(users)
    step("User accounts", _users)

    print("Verifying…")
    checks = {
        "outages": len(outages),
        "station_map": len(station_map),
        "substation_hierarchy": len(hierarchy),
        "equipment_catalog": len(catalog),
    }
    ok = True
    for table, expected in checks.items():
        got = db.count(table)
        flag = "OK" if got == expected else "MISMATCH"
        ok &= got == expected
        print(f"  {table:<34}{got:>6,} / {expected:,}  {flag}")
    got_users = len(db.read_users())
    print(f"  {'app_users':<34}{got_users:>6,} (at least {len(users):,})")
    ok &= got_users >= len(users)

    print("Done." if ok else "Finished with mismatches. Check the counts above.")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
