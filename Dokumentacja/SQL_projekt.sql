create table if not exists public."Stanowisko"
(
    "Nazwa" varchar not null
        constraint unique_column_nazwa_stanowisko
            unique,
    "Opis"  text,
    id      integer generated always as identity
        constraint "Stanowisko_pk"
            primary key
);

alter table public."Stanowisko"
    owner to hwhivgyo;

create table if not exists public."Rola"
(
    id      integer generated always as identity
        constraint "Rola_pk"
            primary key,
    "Nazwa" varchar not null
        constraint unique_column_nazwa_rola
            unique,
    "Opis"  text
);

alter table public."Rola"
    owner to hwhivgyo;

create table if not exists public."Projekt"
(
    id            integer generated always as identity
        constraint "Projekt_pk"
            primary key,
    "Nazwa"       varchar not null
        constraint unique_column_nazwa
            unique
        constraint check_name
            check (length(("Nazwa")::text) >= 3),
    "Opis"        text    not null,
    "Start_Data"  date    not null,
    "Koniec_Data" date    not null
);

comment on constraint check_name on public."Projekt" is 'długość minimum 3 znaki';

alter table public."Projekt"
    owner to hwhivgyo;

create table if not exists public."Osoba"
(
    id              integer generated always as identity
        constraint "Member_pk"
            primary key,
    "Imie"          varchar            not null,
    "Nazwisko"      varchar            not null,
    "Email"         varchar            not null
        constraint unique_column_email_osoba
            unique
        constraint check_email
            check ("position"(("Email")::text, '@'::text) > 0),
    "Stanowisko_ID" integer default 13 not null
        constraint "Stanowisko_ID_FK"
            references public."Stanowisko"
            on update set default on delete set default,
    "Haslo"         text,
    "Administrator" boolean,
    "Telefon"       varchar
);

comment on constraint check_email on public."Osoba" is 'check if email has @';

alter table public."Osoba"
    owner to hwhivgyo;

create trigger osoba_valid
    after insert or update or delete
    on public."Osoba"
    for each row
execute procedure public.valid_data_osoba();

create trigger validatetelefonbeforeinsert
    before insert
    on public."Osoba"
    for each row
execute procedure public.validatephonenumberandsetnewtelefon();

create table if not exists public."Tablica"
(
    id           integer generated always as identity
        constraint "Tablica_pk"
            primary key,
    "Nazwa"      varchar not null
        constraint unique_column_nazwa_tablica
            unique
        constraint check_name
            check (length(("Nazwa")::text) >= 3),
    "Opis"       text    not null,
    "Projekt_ID" integer not null
        constraint "Projekt_ID_FK"
            references public."Projekt"
            on update cascade on delete cascade
);

comment on constraint check_name on public."Tablica" is 'długość minimum 3 znaki';

alter table public."Tablica"
    owner to hwhivgyo;

create table if not exists public."Zadanie"
(
    id                integer generated always as identity
        constraint "Zadanie_pk"
            primary key,
    "Tytul"           varchar not null
        constraint unique_column_nazwa_zadanie
            unique,
    "Opis"            text    not null,
    "Utworzenie_Data" date    not null,
    "Koniec_Data"     date    not null,
    "Priorytet"       varchar not null,
    "Tablica_ID"      integer not null
        constraint "Tablica_ID_FK"
            references public."Tablica"
            on update cascade on delete cascade,
    "Punkty"          integer not null
);

alter table public."Zadanie"
    owner to hwhivgyo;

create table if not exists public."Zadania_Relacja_Typ"
(
    id      integer generated always as identity
        constraint "Zadanie_Relacja_Typ_pk"
            primary key,
    "Nazwa" varchar not null
        constraint unique_column_nazwa_zadania_relacja_typ
            unique,
    "Opis"  text    not null
);

alter table public."Zadania_Relacja_Typ"
    owner to hwhivgyo;

create table if not exists public."Zadania_Relacja"
(
    id               integer generated always as identity
        constraint "Zadania_Relacja_pk"
            primary key,
    "Zadanie_1_ID"   integer not null
        constraint "Zadanie_1_ID_FK"
            references public."Zadanie"
            on update cascade on delete cascade,
    "Zadanie_2_ID"   integer not null
        constraint "Zadanie_2_ID_FK"
            references public."Zadanie"
            on update cascade on delete cascade,
    "Relacja_Typ_ID" integer not null
        constraint "Relacja_Typ_ID_FK"
            references public."Zadania_Relacja_Typ"
            on update cascade on delete cascade
);

alter table public."Zadania_Relacja"
    owner to hwhivgyo;

create table if not exists public."Projekt_Osoba_Rola"
(
    id           integer generated always as identity
        constraint "Projekt_Osoba_Rola_pk"
            primary key,
    "Osoba_ID"   integer not null
        constraint "Osoba_ID_FK"
            references public."Osoba"
            on update cascade on delete cascade,
    "Projekt_ID" integer not null
        constraint "Projekt_ID_FK"
            references public."Projekt"
            on update cascade on delete cascade,
    "Rola_ID"    integer not null
        constraint "Rola_ID_FK"
            references public."Rola"
            on update cascade on delete cascade
);

alter table public."Projekt_Osoba_Rola"
    owner to hwhivgyo;

create or replace view public.pg_stat_statements
            (userid, dbid, queryid, query, calls, total_time, min_time, max_time, mean_time, stddev_time, rows,
             shared_blks_hit, shared_blks_read, shared_blks_dirtied, shared_blks_written, local_blks_hit,
             local_blks_read, local_blks_dirtied, local_blks_written, temp_blks_read, temp_blks_written, blk_read_time,
             blk_write_time)
as
SELECT pg_stat_statements.userid,
       pg_stat_statements.dbid,
       pg_stat_statements.queryid,
       pg_stat_statements.query,
       pg_stat_statements.calls,
       pg_stat_statements.total_time,
       pg_stat_statements.min_time,
       pg_stat_statements.max_time,
       pg_stat_statements.mean_time,
       pg_stat_statements.stddev_time,
       pg_stat_statements.rows,
       pg_stat_statements.shared_blks_hit,
       pg_stat_statements.shared_blks_read,
       pg_stat_statements.shared_blks_dirtied,
       pg_stat_statements.shared_blks_written,
       pg_stat_statements.local_blks_hit,
       pg_stat_statements.local_blks_read,
       pg_stat_statements.local_blks_dirtied,
       pg_stat_statements.local_blks_written,
       pg_stat_statements.temp_blks_read,
       pg_stat_statements.temp_blks_written,
       pg_stat_statements.blk_read_time,
       pg_stat_statements.blk_write_time
FROM pg_stat_statements(true) pg_stat_statements(userid, dbid, queryid, query, calls, total_time, min_time, max_time,
                                                 mean_time, stddev_time, rows, shared_blks_hit, shared_blks_read,
                                                 shared_blks_dirtied, shared_blks_written, local_blks_hit,
                                                 local_blks_read, local_blks_dirtied, local_blks_written,
                                                 temp_blks_read, temp_blks_written, blk_read_time, blk_write_time);

alter table public.pg_stat_statements
    owner to postgres;

grant select on public.pg_stat_statements to public;

create or replace view public."Projekty_Zakonczone"(id, "Nazwa", "Opis", "Start_Data", "Koniec_Data") as
SELECT "Projekt".id,
       "Projekt"."Nazwa",
       "Projekt"."Opis",
       "Projekt"."Start_Data",
       "Projekt"."Koniec_Data"
FROM "Projekt"
WHERE "Projekt"."Koniec_Data" < CURRENT_DATE;

alter table public."Projekty_Zakonczone"
    owner to hwhivgyo;

create or replace view public.projekt_z_liczbami
            (id, "Nazwa", "Opis", "Start_Data", "Koniec_Data", liczba_tablic, liczba_zadan) as
SELECT p.id,
       p."Nazwa",
       p."Opis",
       p."Start_Data",
       p."Koniec_Data",
       (SELECT count(*) AS count
        FROM "Tablica" t_1
        WHERE t_1."Projekt_ID" = p.id)  AS liczba_tablic,
       COALESCE(count(z.id), 0::bigint) AS liczba_zadan
FROM "Projekt" p
         LEFT JOIN "Tablica" t ON p.id = t."Projekt_ID"
         LEFT JOIN "Zadanie" z ON t.id = z."Tablica_ID"
GROUP BY p.id, t.id;

alter table public.projekt_z_liczbami
    owner to hwhivgyo;

create or replace view public.tablice_z_0_zadaniami(id, "Nazwa", "Liczba zadan") as
SELECT t.id,
       t."Nazwa",
       COALESCE(count(z.id), 0::bigint) AS "Liczba zadan"
FROM "Tablica" t
         LEFT JOIN "Zadanie" z ON t.id = z."Tablica_ID"
GROUP BY t.id
HAVING count(z.id) = 0;

alter table public.tablice_z_0_zadaniami
    owner to hwhivgyo;

create or replace view public.tablice_z_min_1_zadaniem(id, "Nazwa", "Liczba zadan") as
SELECT t.id,
       t."Nazwa",
       COALESCE(count(z.id), 0::bigint) AS "Liczba zadan"
FROM "Tablica" t
         LEFT JOIN "Zadanie" z ON t.id = z."Tablica_ID"
GROUP BY t.id
HAVING count(z.id) > 0;

alter table public.tablice_z_min_1_zadaniem
    owner to hwhivgyo;

create or replace view public.tablice_z_suma_punktow_mniejsza_niz_100(id, "Nazwa", "Punkty") as
SELECT t.id,
       t."Nazwa",
       COALESCE(sum(
                        CASE
                            WHEN z.id IS NOT NULL THEN z.id
                            ELSE 0
                            END), 0::bigint) AS "Punkty"
FROM "Tablica" t
         LEFT JOIN "Zadanie" z ON t.id = z."Tablica_ID"
GROUP BY t.id
HAVING COALESCE(sum(
                        CASE
                            WHEN z.id IS NOT NULL THEN 1
                            ELSE 0
                            END), 0::bigint) < 100;

alter table public.tablice_z_suma_punktow_mniejsza_niz_100
    owner to hwhivgyo;

create or replace view public.tablice_z_liczba_punktow_minimum_100(id, "Nazwa", "Punkty") as
SELECT t.id,
       t."Nazwa",
       COALESCE(sum(z.id), 0::bigint) AS "Punkty"
FROM "Tablica" t
         LEFT JOIN "Zadanie" z ON t.id = z."Tablica_ID"
GROUP BY t.id
HAVING sum(z.id) >= 100;

alter table public.tablice_z_liczba_punktow_minimum_100
    owner to hwhivgyo;

create or replace view public.moje_projekty_widok
            ("Projekt_ID", "Osoba_ID", "Rola_ID", "Projekt_Nazwa", "Projekt_Opis", "Start_Data", "Koniec_Data", "Imie",
             "Nazwisko", "Email", "Rola_Nazwa", "Rola_Opis")
as
SELECT p.id      AS "Projekt_ID",
       o.id      AS "Osoba_ID",
       r.id      AS "Rola_ID",
       p."Nazwa" AS "Projekt_Nazwa",
       p."Opis"  AS "Projekt_Opis",
       p."Start_Data",
       p."Koniec_Data",
       o."Imie",
       o."Nazwisko",
       o."Email",
       r."Nazwa" AS "Rola_Nazwa",
       r."Opis"  AS "Rola_Opis"
FROM projekt_z_liczbami p
         JOIN "Projekt_Osoba_Rola" pos ON p.id = pos."Projekt_ID"
         JOIN "Osoba" o ON o.id = pos."Osoba_ID"
         JOIN "Rola" r ON pos."Rola_ID" = r.id;

alter table public.moje_projekty_widok
    owner to hwhivgyo;

