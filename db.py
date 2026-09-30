"""Supabase storage layer for the TCN Grid Outage Manager.

The app uses Supabase when credentials are configured, and falls back to the
local Excel/CSV/JSON files otherwise. Credentials are read, in order, from:

  1. db.configure(url, key)                      (scripts, e.g. the migration)
  2. .streamlit/secrets.toml  SUPABASE_URL / SUPABASE_KEY
  3. environment variables    SUPABASE_URL / SUPABASE_KEY

SUPABASE_KEY must be the project's *secret* (service_role) key. The tables have
Row Level Security enabled with no policies, so the public (anon/publishable)
key cannot read or write anything. Keep the secret key out of git.
"""

import os
import re
from datetime import date, datetime
from functools import lru_cache

import numpy as np
import pandas as pd

PAGE_SIZE = 1000   # PostgREST returns at most 1000 rows per request
CHUNK_SIZE = 500   # rows per insert request

# App column name → database column name
OUTAGE_COLUMNS = {
    "Region": "region",
    "SubRegion_ACC": "subregion_acc",
    "Substation": "substation",
    "Equipment": "equipment",
    "Date_Off": "date_off",
    "Hour_Off": "hour_off",
    "Minute_Off": "minute_off",
    "Date_On": "date_on",
    "Hour_On": "hour_on",
    "Minute_On": "minute_on",
    "Duration": "duration",
    "Class": "outage_class",
    "Last_Load_MW": "last_load_mw",
    "Event_Indication": "event_indication",
    "Officer_Interruption": "officer_interruption",
    "Officer_Restoration": "officer_restoration",
    "Party_Responsible": "party_responsible",
    "Weather_Condition": "weather_condition",
    "Remarks": "remarks",
}
_DATE_COLS = {"date_off", "date_on"}
_INT_COLS = {"hour_off", "minute_off", "hour_on", "minute_on"}
_FLOAT_COLS = {"last_load_mw"}

STATION_MAP_COLUMNS = {
    "Region": "region",
    "Sub-Region": "sub_region",
    "Transmission Station": "transmission_station",
    "Sub-Station": "sub_station",
}
HIERARCHY_COLUMNS = {**STATION_MAP_COLUMNS, "Remarks": "remarks"}
CATALOG_COLUMNS = {
    "Region": "region",
    "SubRegion": "subregion",
    "Substation": "substation",
    "Equipment_Type": "equipment_type",
    "Voltage_Level": "voltage_level",
    "Equipment": "equipment",
}


# ──────────────────────────────────────────────────────────────
# Connection
# ──────────────────────────────────────────────────────────────
_override = {}


def configure(url, key):
    """Set credentials explicitly (used by scripts running outside Streamlit)."""
    _override.update(url=url, key=key)
    _client.cache_clear()


def _credentials():
    if _override:
        return _override.get("url"), _override.get("key")
    url = key = None
    try:
        import streamlit as st
        url = st.secrets.get("SUPABASE_URL")
        key = st.secrets.get("SUPABASE_KEY")
    except Exception:
        pass  # no secrets.toml
    return url or os.environ.get("SUPABASE_URL"), key or os.environ.get("SUPABASE_KEY")


def enabled():
    url, key = _credentials()
    if not (url and key):
        return False
    # Template placeholders from secrets.toml.example count as "not configured"
    return "your-project" not in url and not key.startswith("paste-")


@lru_cache(maxsize=1)
def _client():
    from supabase import create_client
    url, key = _credentials()
    if not (url and key):
        raise RuntimeError("Supabase is not configured (SUPABASE_URL / SUPABASE_KEY missing).")
    return create_client(url, key)


# ──────────────────────────────────────────────────────────────
# Generic helpers
# ──────────────────────────────────────────────────────────────
def _select_all(table):
    """Every row of a table, in insertion order, paging past the 1000-row cap."""
    rows, start = [], 0
    while True:
        res = (_client().table(table).select("*").order("id")
               .range(start, start + PAGE_SIZE - 1).execute())
        rows.extend(res.data)
        if len(res.data) < PAGE_SIZE:
            return rows
        start += PAGE_SIZE


def _insert(table, records):
    for i in range(0, len(records), CHUNK_SIZE):
        _client().table(table).insert(records[i:i + CHUNK_SIZE]).execute()


def _delete_all(table):
    # PostgREST refuses an unfiltered DELETE; every id is > 0.
    _client().table(table).delete().gt("id", 0).execute()


def count(table):
    res = _client().table(table).select("id", count="exact").limit(1).execute()
    return res.count or 0


def _clean(value):
    """NaN/NaT/numpy scalars → JSON-safe Python values."""
    if value is None:
        return None
    if isinstance(value, float) and np.isnan(value):
        return None
    if value is pd.NaT:
        return None
    if isinstance(value, np.generic):
        value = value.item()
        if isinstance(value, float) and np.isnan(value):
            return None
    if isinstance(value, str):
        value = value.strip()
        return value or None
    return value


def _frame(rows, mapping, extra=()):
    """DB rows → DataFrame with the app's column names (None → NaN)."""
    inverse = {db: app for app, db in mapping.items()}
    cols = list(mapping.values()) + list(extra)
    df = pd.DataFrame(rows, columns=cols) if rows else pd.DataFrame(columns=cols)
    df = df[cols].rename(columns=inverse)
    return df.replace({None: np.nan})


def _records(df, mapping):
    out = []
    for row in df.to_dict("records"):
        out.append({db: _clean(row.get(app)) for app, db in mapping.items()})
    return out


# ──────────────────────────────────────────────────────────────
# Outages
# ──────────────────────────────────────────────────────────────
_ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}")


def _to_iso_date(value):
    value = _clean(value)
    if value is None:
        return None
    if isinstance(value, (datetime, pd.Timestamp)):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    s = str(value).strip()
    parsed = pd.to_datetime(s, format="ISO8601", errors="coerce") if _ISO_DATE.match(s) \
        else pd.to_datetime(s, dayfirst=True, errors="coerce")
    return None if pd.isna(parsed) else parsed.date().isoformat()


def _to_int(value):
    value = _clean(value)
    if value is None:
        return None
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return None


def _to_float(value):
    value = _clean(value)
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _outage_record(row):
    rec = {}
    for app, col in OUTAGE_COLUMNS.items():
        v = row.get(app)
        if col in _DATE_COLS:
            rec[col] = _to_iso_date(v)
        elif col in _INT_COLS:
            rec[col] = _to_int(v)
        elif col in _FLOAT_COLS:
            rec[col] = _to_float(v)
        else:
            v = _clean(v)
            rec[col] = None if v is None else str(v)  # e.g. datetime.time durations
    return rec


def read_outages():
    """All outage rows with the app's raw column names, dates as dd/mm/YYYY."""
    df = _frame(_select_all("outages"), OUTAGE_COLUMNS)
    for app in ("Date_Off", "Date_On"):
        d = pd.to_datetime(df[app], format="%Y-%m-%d", errors="coerce")
        df[app] = d.dt.strftime("%d/%m/%Y").where(d.notna(), np.nan)
    return df


def append_outages(df):
    _insert("outages", [_outage_record(r) for r in df.to_dict("records")])


def replace_outages(df):
    _delete_all("outages")
    append_outages(df)


# ──────────────────────────────────────────────────────────────
# Users
# ──────────────────────────────────────────────────────────────
def read_users():
    rows = _client().table("app_users").select("*").execute().data
    return {
        r["username"]: {
            "password": r["password_hash"], "role": r["role"],
            "name": r.get("name") or r["username"], "region": r.get("region"),
        }
        for r in rows
    }


def upsert_user(username, record):
    _client().table("app_users").upsert({
        "username": username,
        "password_hash": record["password"],
        "role": record["role"],
        "name": record.get("name"),
        "region": record.get("region"),
    }).execute()


def delete_user(username):
    _client().table("app_users").delete().eq("username", username).execute()


# ──────────────────────────────────────────────────────────────
# Reference data
# ──────────────────────────────────────────────────────────────
def read_station_map():
    return _frame(_select_all("station_map"), STATION_MAP_COLUMNS)


def read_hierarchy():
    return _frame(_select_all("substation_hierarchy"), HIERARCHY_COLUMNS)


def read_catalog():
    return _frame(_select_all("equipment_catalog"), CATALOG_COLUMNS)


def replace_reference(table, df):
    mapping = {
        "station_map": STATION_MAP_COLUMNS,
        "substation_hierarchy": HIERARCHY_COLUMNS,
        "equipment_catalog": CATALOG_COLUMNS,
    }[table]
    _delete_all(table)
    _insert(table, _records(df, mapping))
