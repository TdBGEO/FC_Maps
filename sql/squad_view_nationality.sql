-- Adds nationality to data.squad_view.
-- squad_view is a PLAIN view, so CREATE OR REPLACE swaps the definition in
-- place: no drop, no gap where the view is missing, and no REFRESH afterwards.
--
-- CREATE OR REPLACE requires the existing columns to keep their exact names,
-- types and order, with new ones appended at the END. That is why the two
-- nationality columns sit after is_active rather than next to birth_country.
-- Django maps columns by name, so the position makes no difference to the app.

CREATE OR REPLACE VIEW data.squad_view AS
SELECT p.player_code,
    p.name,
    p.date_of_birth,
    p.birth_country_iso3,
    bc.name AS birth_country,
    pl.naam AS birthplace_city,
    pl.match_addr,
    pl.geom,
    r."position",
    r.season_id,
    c.name AS club,
    c.competition_name AS club_competition,
    nt.name AS national_team,
    ns.country_iso3,
    COALESCE(comp.name, cc.name) AS competition,
    COALESCE(comp.code, cc.code) AS competition_code,
    nsp.is_active,
    nat.country_iso3 AS nationality_iso3,
    nc.name AS nationality
   FROM data.player p
     LEFT JOIN ref.place pl ON p.birthplace_code = pl.ogc_fid::text
     LEFT JOIN ref.country bc ON p.birth_country_iso3 = bc.iso3
     LEFT JOIN data.player_nationality nat ON p.player_code = nat.player_code
     LEFT JOIN ref.country nc ON nat.country_iso3 = nc.iso3
     LEFT JOIN data.roster r ON p.player_code = r.player_code
     LEFT JOIN ref.club c ON r.club_code = c.club_code
     LEFT JOIN ref.competition cc ON c.competition_id = cc.competition_id
     LEFT JOIN data.national_squad_player nsp ON p.player_code = nsp.player_code
     LEFT JOIN data.national_squad ns ON nsp.squad_id = ns.squad_id
     LEFT JOIN ref.national_team nt ON ns.country_iso3 = nt.country_iso3
     LEFT JOIN ref.competition comp ON ns.competition_id = comp.competition_id;

-- Sanity checks. The counts must be EXACTLY 1292 / 463 — anything higher means
-- a player has more than one nationality row and the join duplicated them.
SELECT competition_code, count(*) FROM data.squad_view GROUP BY 1 ORDER BY 1;

SELECT count(*) AS total,
       count(nationality_iso3) AS with_nationality
FROM data.squad_view WHERE competition_code = 'ERE2627';
