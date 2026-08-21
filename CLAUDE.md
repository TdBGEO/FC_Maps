# FC Maps — Project Guide for Claude Code

## What this project is
FC Maps is a geospatial web app that plots football players' birthplaces on an
interactive Leaflet map. It is live at https://fcmaps.nl (custom domain) and
https://fcmaps-production.up.railway.app.

Currently it shows one map: the FIFA World Cup 2026 national squads. We are now
adding a second map for the Dutch Eredivisie 2026/27 club rosters. **Both maps
must keep working — the World Cup map stays exactly as it is.**

## Current goal
Build the infrastructure for a second map (Eredivisie 2026/27) so that, once the
data is scraped after 1 September, it appears automatically. Specifically:
1. A landing page that links to both maps (World Cup and Eredivisie).
2. An Eredivisie map page that works like the WC one but requests
   `competition_code=ERE2627` instead of `WC2026`.
3. Navigation so a visitor can move between landing page and either map.

The data is NOT in the database yet — do not assume Eredivisie rows exist.
The pages must render gracefully (empty map, no crash) until data arrives.

## Tech stack
- Backend: Django + GeoDjango + Django REST Framework + PostGIS
- Frontend: vanilla HTML + Leaflet, served by a Django template (no framework)
- DB: PostgreSQL + PostGIS locally (source of truth), mirrored on Railway (prod)
- Deploy: Railway (Docker build), custom domain via Cloudflare

## Repository layout
```
FC_Maps/
├── backend/
│   ├── config/            # Django project: settings.py, urls.py, wsgi.py
│   ├── squad/             # PRIMARY app — reads data.squad_view, serves /api/squad/
│   ├── players/           # DEPRECATED, do not use
│   ├── templates/
│   │   └── index.html     # The live WC2026 map page (Leaflet + filters)
│   ├── manage.py
│   └── requirements.txt
├── frontend/index.html    # dev mirror of the template (not served in prod)
├── Dockerfile
├── Procfile
└── requirements.txt       # root, used by Railway
```

## The API
The frontend reads from a single endpoint:
`/api/squad/?competition_code=WC2026&page_size=2000`
It returns GeoJSON features (one per player) from the materialized view
`data.squad_view`. The Eredivisie map will use the same endpoint with
`competition_code=ERE2627`.

Key view/serializer files live in `backend/squad/`. The viewset is a
ReadOnlyModelViewSet with DjangoFilterBackend; `competition_code` is already a
filterable field, so the API likely needs no changes for Eredivisie — verify
before changing anything.

## Database (do not modify schema without asking)
- One player = one row in `data.player`, keyed on Transfermarkt ID.
  A player can belong to BOTH a national squad AND a club roster with no
  duplication. This normalization is intentional — never denormalize it.
- `data.squad_view` is a MATERIALIZED VIEW joining player, place, club,
  roster, national_squad, competition, etc.
- Competitions live in `ref.competition` (WC2026 = id 1, ERE2627 = new).
- After any data write you must run: `REFRESH MATERIALIZED VIEW data.squad_view;`

## Design rules (IMPORTANT — the owner cares about this)
- NO typical "AI-generated" styling. Absolutely no purple gradients, no
  glassmorphism, no generic SaaS look.
- The existing look is editorial: Anton + Inter fonts, orange #E8650A,
  paper #f7f4ef, ink #1a1a1a. Match this exactly on any new page.
- Keep the existing filter sidebar, stats panel, flag markers, and popup
  card styling consistent between the two maps.
- Minimal, clean, purposeful. When in doubt, copy the pattern already in
  `backend/templates/index.html`.

## Deploy flow (never deploy without the owner saying so)
- Local Postgres is the source of truth; Railway is prod.
- Frontend/template changes deploy via git push (Railway auto-builds).
- DB changes sync via a PGAdmin plain backup → DBeaver restore on Railway
  (manual, owner-driven). Do not attempt DB deploys.

## Working style the owner wants
- ALWAYS plan first, then execute. Explain what you will change and why,
  in plain language, before editing.
- Make small, reviewable changes. One page/feature at a time.
- The owner is learning Django/Linux/deployment — explain the *why*, not
  just the *what*.
- The owner is Dutch; match their language (Dutch/English) in chat.
- Never touch `.env`, secrets, or the `players/` deprecated app.
- Never run destructive git commands (force push, hard reset) without asking.

## What NOT to do
- Do not break or restyle the World Cup map.
- Do not invent database columns or API fields — check first.
- Do not add heavy frameworks (React, Vue, build tooling). Keep it vanilla.
- Do not deploy or push to git unless explicitly told.
