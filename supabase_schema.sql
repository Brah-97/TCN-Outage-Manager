-- TCN Grid Outage Manager: Supabase schema
-- Run once in the Supabase dashboard: SQL Editor → New query → paste → Run.
--
-- Row Level Security is enabled on every table with NO policies, so the public
-- (anon / publishable) key can neither read nor write. The Streamlit app runs
-- server-side with the secret (service_role) key, which bypasses RLS.

-- ── Outage records ────────────────────────────────────────────
create table if not exists public.outages (
    id                   bigint generated always as identity primary key,
    created_at           timestamptz not null default now(),
    region               text,
    subregion_acc        text,
    substation           text,
    equipment            text,
    date_off             date,
    hour_off             smallint,
    minute_off           smallint,
    date_on              date,
    hour_on              smallint,
    minute_on            smallint,
    duration             text,          -- "h:mm", e.g. "401:16"
    outage_class         text,          -- Forced / Emergency / Planned
    last_load_mw         double precision,
    event_indication     text,
    officer_interruption text,
    officer_restoration  text,
    party_responsible    text,
    weather_condition    text,
    remarks              text
);
create index if not exists outages_region_idx   on public.outages (region);
create index if not exists outages_date_off_idx on public.outages (date_off);

-- ── App users ─────────────────────────────────────────────────
create table if not exists public.app_users (
    username      text primary key,
    password_hash text not null,
    role          text not null check (role in ('admin', 'operator')),
    name          text,
    region        text,             -- null = all regions
    created_at    timestamptz not null default now()
);

-- ── Reference data ────────────────────────────────────────────
-- Canonical station / sub-region names (was station_region_map.csv).
-- Row order matters for name matching, so reads are ordered by id.
create table if not exists public.station_map (
    id                   bigint generated always as identity primary key,
    region               text,
    sub_region           text,
    transmission_station text,
    sub_station          text
);

-- Network Hierarchy tab (was Complete List of Substation.xlsx).
create table if not exists public.substation_hierarchy (
    id                   bigint generated always as identity primary key,
    region               text,
    sub_region           text,
    transmission_station text,
    sub_station          text,
    remarks              text
);

-- 330kV lines/transformers and 132kV transformers
-- (was the two equipment reference workbooks; 33kV feeders excluded).
create table if not exists public.equipment_catalog (
    id             bigint generated always as identity primary key,
    region         text,
    subregion      text,
    substation     text,
    equipment_type text,
    voltage_level  text,
    equipment      text
);

-- ── Lock everything down ──────────────────────────────────────
alter table public.outages              enable row level security;
alter table public.app_users            enable row level security;
alter table public.station_map          enable row level security;
alter table public.substation_hierarchy enable row level security;
alter table public.equipment_catalog    enable row level security;
