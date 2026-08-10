-- Combined Database Setup Script for Spoting
-- PostgreSQL 18 Compatible

-- Drop and Create Database
SELECT 'DROP DATABASE spoting'
WHERE EXISTS (SELECT FROM pg_database WHERE datname = 'spoting')\gexec

SELECT 'CREATE DATABASE spoting'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'spoting')\gexec

\c spoting;

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';
SET default_table_access_method = heap;

-- SET pelanggan_json = '{"id": 1, "kod":"KKP01", "nama": "Kementerian Dalam Negeri", "keterangan": "Kementerian" }';

-- Set the variable in psql
\set pelanggan_json '{"id": 1, "kod":"KKP01", "nama": "Kementerian Dalam Negeri", "keterangan": "Kementerian" }'

-- ============================================================
-- CREATE TABLES
-- ============================================================

-- Alembic Version
CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);

ALTER TABLE public.alembic_version OWNER TO postgres;

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);
    
    
-- Pelanggan
CREATE TABLE public.pelanggan (
    id integer NOT NULL,
    kod character varying(50) NOT NULL,
    nama character varying(255) NOT NULL,
    keterangan text,
    aktif boolean,
    cipta_pada timestamp without time zone DEFAULT now(),
    kemaskini_pada timestamp without time zone DEFAULT now()
);
ALTER TABLE public.pelanggan OWNER TO postgres;

CREATE SEQUENCE public.pelanggan_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER SEQUENCE public.pelanggan_id_seq OWNER TO postgres;
ALTER SEQUENCE public.pelanggan_id_seq OWNED BY public.pelanggan.id;

-- Users
CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(50) NOT NULL,
    password character varying(255) NOT NULL,
    role character varying(20) DEFAULT 'user'::character varying NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    pelanggan_id integer,
    nama character varying,
    aktif boolean DEFAULT true,
    force_password_change boolean DEFAULT true,
    email character varying,
    phone character varying
);
ALTER TABLE public.users OWNER TO postgres;

CREATE SEQUENCE public.users_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER SEQUENCE public.users_id_seq OWNER TO postgres;
ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;

-- Organisasi
CREATE TABLE public.organisasi (
    id integer NOT NULL,
    pelanggan_id integer NOT NULL,
    kod character varying(50) NOT NULL,
    nama character varying(255) NOT NULL,
    keterangan text,
    aktif boolean,
    cipta_pada timestamp without time zone DEFAULT now(),
    kemaskini_pada timestamp without time zone DEFAULT now(),
    pegawai_tadbir character varying(64),
    jawatan character varying(64)
);
ALTER TABLE public.organisasi OWNER TO postgres;

CREATE SEQUENCE public.organisasi_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER SEQUENCE public.organisasi_id_seq OWNER TO postgres;
ALTER SEQUENCE public.organisasi_id_seq OWNED BY public.organisasi.id;

-- Sub Organisasi
CREATE TABLE public.sub_organisasi (
    id integer NOT NULL,
    organisasi_id integer NOT NULL,
    kod character varying(50) NOT NULL,
    nama character varying(255) NOT NULL,
    keterangan text,
    aktif boolean,
    cipta_pada timestamp without time zone DEFAULT now(),
    kemaskini_pada timestamp without time zone DEFAULT now(),
    pegawai_tadbir character varying(64),
    jawatan character varying(64)
);
ALTER TABLE public.sub_organisasi OWNER TO postgres;

CREATE SEQUENCE public.sub_organisasi_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER SEQUENCE public.sub_organisasi_id_seq OWNER TO postgres;
ALTER SEQUENCE public.sub_organisasi_id_seq OWNED BY public.sub_organisasi.id;

-- Tapak
CREATE TABLE public.tapak (
    id integer NOT NULL,
    sub_organisasi_id integer NOT NULL,
    kod character varying(50) NOT NULL,
    nama character varying(255) NOT NULL,
    keterangan text,
    aktif boolean DEFAULT true,
    cipta_pada timestamp without time zone DEFAULT now(),
    kemaskini_pada timestamp without time zone DEFAULT now(),
    nombor character varying(255),
    aras character varying(255),
    alamat_baris_1 character varying(128),
    alamat_baris_2 character varying(128),
    bandar character varying(64),
    negeri character varying(64),
    negara character varying(64) DEFAULT 'MALAYSIA'::character varying,
    pegawai_tadbir character varying(64),
    jawatan character varying(64)
);
ALTER TABLE public.tapak OWNER TO postgres;

CREATE SEQUENCE public.tapak_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER SEQUENCE public.tapak_id_seq OWNER TO postgres;
ALTER SEQUENCE public.tapak_id_seq OWNED BY public.tapak.id;

-- Jenis Tugasan
CREATE TABLE public.jenis_tugasan (
    id integer NOT NULL,
    nama character varying(100) NOT NULL
);
ALTER TABLE public.jenis_tugasan OWNER TO postgres;

CREATE SEQUENCE public.jenis_tugasan_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER SEQUENCE public.jenis_tugasan_id_seq OWNER TO postgres;
ALTER SEQUENCE public.jenis_tugasan_id_seq OWNED BY public.jenis_tugasan.id;

-- Tugasan
CREATE TABLE public.tugasan (
    id integer NOT NULL,
    nama character varying(255),
    protocol character varying(10),
    ip_start inet,
    ip_end inet,
    cipta_pada timestamp without time zone DEFAULT now(),
    kod character varying(50),
    keterangan text,
    aktif boolean DEFAULT true,
    kemaskini_pada timestamp without time zone DEFAULT now(),
    jenis_id integer NOT NULL
);
ALTER TABLE public.tugasan OWNER TO postgres;

CREATE SEQUENCE public.tugasan_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER SEQUENCE public.tugasan_id_seq OWNER TO postgres;
ALTER SEQUENCE public.tugasan_id_seq OWNED BY public.tugasan.id;

-- Profil
CREATE TABLE public.profil (
    id integer NOT NULL,
    tapak_id integer NOT NULL,
    kod character varying(50) NOT NULL,
    nama character varying(255) NOT NULL,
    keterangan text,
    aktif boolean,
    cipta_pada timestamp without time zone DEFAULT now(),
    kemaskini_pada timestamp without time zone DEFAULT now(),
    execution_type character varying(20) DEFAULT 'IMMEDIATE'::character varying,
    is_scheduled boolean DEFAULT false,
    report_template character varying(100) DEFAULT 'DEFAULT'::character varying,
    report_format character varying(20) DEFAULT 'EXCEL'::character varying,
    scheduled_at timestamp without time zone,
    execution_status character varying(50) DEFAULT 'belum'::character varying,
    cron_enabled boolean DEFAULT false,
    frequency character varying(20),
    cron_expression character varying(255)
);
ALTER TABLE public.profil OWNER TO postgres;

CREATE SEQUENCE public.profil_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER SEQUENCE public.profil_id_seq OWNER TO postgres;
ALTER SEQUENCE public.profil_id_seq OWNED BY public.profil.id;

-- Status
CREATE TABLE public.status (
    id integer NOT NULL,
    kod_status character varying(20) NOT NULL
);
ALTER TABLE public.status OWNER TO postgres;

CREATE SEQUENCE public.status_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER SEQUENCE public.status_id_seq OWNER TO postgres;
ALTER SEQUENCE public.status_id_seq OWNED BY public.status.id;

-- X Profil Tugasan
CREATE TABLE public.x_profil_tugasan (
    profil_id integer NOT NULL,
    tugasan_id integer NOT NULL,
    jadualkan_pada timestamp without time zone,
    selesai_pada timestamp without time zone,
    id integer NOT NULL,
    status_id integer
);
ALTER TABLE public.x_profil_tugasan OWNER TO postgres;

CREATE SEQUENCE public.x_profil_tugasan_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER SEQUENCE public.x_profil_tugasan_id_seq OWNER TO postgres;
ALTER SEQUENCE public.x_profil_tugasan_id_seq OWNED BY public.x_profil_tugasan.id;

-- X Profil Ejen
CREATE TABLE public.x_profil_ejen (
    id bigint NOT NULL,
    profil_id bigint NOT NULL,
    ejen_id bigint NOT NULL,
    status character varying(20) DEFAULT 'Pending'::character varying NOT NULL,
    started_at timestamp without time zone,
    completed_at timestamp without time zone,
    created_at timestamp without time zone DEFAULT now() NOT NULL
);

ALTER TABLE public.x_profil_ejen OWNER TO postgres;

CREATE SEQUENCE public.x_profil_ejen_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.x_profil_ejen_id_seq OWNER TO postgres;

ALTER SEQUENCE public.x_profil_ejen_id_seq
OWNED BY public.x_profil_ejen.id;


-- Ejen
CREATE TABLE public.ejen (
    id bigint NOT NULL,
    ip_address inet NOT NULL,
    machine_id uuid NOT NULL,
    hostname character varying(255) NOT NULL,
    tapak_id bigint NOT NULL,
    profile_id bigint NOT NULL,
    status character varying(20) NOT NULL DEFAULT 'Running',
    last_seen timestamp without time zone NOT NULL DEFAULT now(),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);
ALTER TABLE public.ejen OWNER TO postgres;

CREATE SEQUENCE public.ejen_id_seq AS bigint START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER SEQUENCE public.ejen_id_seq OWNER TO postgres;
ALTER TABLE public.ejen ALTER COLUMN id SET DEFAULT nextval('public.ejen_id_seq'::regclass);

-- Hasil Imbasan (with blockchain columns)
CREATE TABLE public.hasil_imbasan (
    id bigint NOT NULL,
    profil_tugasan_id bigint NOT NULL,
    ejen_id bigint NOT NULL,
    machine_id uuid NOT NULL,
    hasil json NOT NULL,
    created_at timestamp without time zone DEFAULT now(),
    prev_hash TEXT,
    row_hash TEXT
);
ALTER TABLE public.hasil_imbasan OWNER TO postgres;

CREATE SEQUENCE public.hasil_imbasan_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER SEQUENCE public.hasil_imbasan_id_seq OWNER TO postgres;
ALTER SEQUENCE public.hasil_imbasan_id_seq OWNED BY public.hasil_imbasan.id;

-- X Profil Tugasan Ejen
CREATE TABLE public.x_profil_tugasan_ejen (
    id bigint NOT NULL,
    profil_tugasan_id bigint NOT NULL,
    ejen_id bigint NOT NULL,
    status character varying(20) DEFAULT 'Pending'::character varying NOT NULL,
    started_at timestamp without time zone,
    completed_at timestamp without time zone,
    created_at timestamp without time zone DEFAULT now() NOT NULL
);

ALTER TABLE public.x_profil_tugasan_ejen OWNER TO postgres;

CREATE SEQUENCE public.x_profil_tugasan_ejen_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.x_profil_tugasan_ejen_id_seq OWNER TO postgres;

ALTER SEQUENCE public.x_profil_tugasan_ejen_id_seq
OWNED BY public.x_profil_tugasan_ejen.id;
-- ============================================================
-- SET DEFAULTS FOR IDENTITY COLUMNS
-- ============================================================
ALTER TABLE ONLY public.hasil_imbasan ALTER COLUMN id SET DEFAULT nextval('public.hasil_imbasan_id_seq'::regclass);
ALTER TABLE ONLY public.jenis_tugasan ALTER COLUMN id SET DEFAULT nextval('public.jenis_tugasan_id_seq'::regclass);
ALTER TABLE ONLY public.organisasi ALTER COLUMN id SET DEFAULT nextval('public.organisasi_id_seq'::regclass);
ALTER TABLE ONLY public.pelanggan ALTER COLUMN id SET DEFAULT nextval('public.pelanggan_id_seq'::regclass);
ALTER TABLE ONLY public.profil ALTER COLUMN id SET DEFAULT nextval('public.profil_id_seq'::regclass);
ALTER TABLE ONLY public.status ALTER COLUMN id SET DEFAULT nextval('public.status_id_seq'::regclass);
ALTER TABLE ONLY public.sub_organisasi ALTER COLUMN id SET DEFAULT nextval('public.sub_organisasi_id_seq'::regclass);
ALTER TABLE ONLY public.tapak ALTER COLUMN id SET DEFAULT nextval('public.tapak_id_seq'::regclass);
ALTER TABLE ONLY public.tugasan ALTER COLUMN id SET DEFAULT nextval('public.tugasan_id_seq'::regclass);
ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);
ALTER TABLE ONLY public.x_profil_tugasan ALTER COLUMN id SET DEFAULT nextval('public.x_profil_tugasan_id_seq'::regclass);
ALTER TABLE ONLY public.x_profil_ejen
ALTER COLUMN id SET DEFAULT nextval('public.x_profil_ejen_id_seq'::regclass);

ALTER TABLE ONLY public.x_profil_tugasan_ejen
ALTER COLUMN id SET DEFAULT nextval('public.x_profil_tugasan_ejen_id_seq'::regclass);
-- ============================================================
-- PRIMARY KEY CONSTRAINTS
-- ============================================================
ALTER TABLE ONLY public.ejen ADD CONSTRAINT ejen_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.ejen ADD CONSTRAINT ejen_unique UNIQUE (ip_address);
ALTER TABLE ONLY public.ejen ADD CONSTRAINT ejen_machine_id_key UNIQUE (machine_id);
ALTER TABLE ONLY public.hasil_imbasan ADD CONSTRAINT hasil_imbasan_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.jenis_tugasan ADD CONSTRAINT jenis_tugasan_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.organisasi ADD CONSTRAINT organisasi_kod_key UNIQUE (kod);
ALTER TABLE ONLY public.organisasi ADD CONSTRAINT organisasi_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.pelanggan ADD CONSTRAINT pelanggan_kod_key UNIQUE (kod);
ALTER TABLE ONLY public.pelanggan ADD CONSTRAINT pelanggan_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.profil ADD CONSTRAINT profil_kod_key UNIQUE (kod);
ALTER TABLE ONLY public.profil ADD CONSTRAINT profil_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.status ADD CONSTRAINT status_kod_status_key UNIQUE (kod_status);
ALTER TABLE ONLY public.status ADD CONSTRAINT status_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.sub_organisasi ADD CONSTRAINT sub_organisasi_kod_key UNIQUE (kod);
ALTER TABLE ONLY public.sub_organisasi ADD CONSTRAINT sub_organisasi_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.tapak ADD CONSTRAINT tapak_kod_key UNIQUE (kod);
ALTER TABLE ONLY public.tapak ADD CONSTRAINT tapak_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.tugasan ADD CONSTRAINT tugasan_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.x_profil_tugasan ADD CONSTRAINT unique_profil_tugasan UNIQUE (profil_id, tugasan_id);
ALTER TABLE ONLY public.users ADD CONSTRAINT users_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.users ADD CONSTRAINT users_username_key UNIQUE (username);
ALTER TABLE ONLY public.x_profil_tugasan ADD CONSTRAINT x_profil_tugasan_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.x_profil_ejen
ADD CONSTRAINT x_profil_ejen_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.x_profil_ejen
ADD CONSTRAINT uq_x_profil_ejen UNIQUE (profil_id, ejen_id);

ALTER TABLE ONLY public.x_profil_tugasan_ejen
ADD CONSTRAINT x_profil_tugasan_ejen_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.x_profil_tugasan_ejen
ADD CONSTRAINT uq_task_agent UNIQUE (profil_tugasan_id, ejen_id);
-- ============================================================
-- FOREIGN KEY CONSTRAINTS
-- ============================================================
ALTER TABLE ONLY public.ejen
ADD CONSTRAINT ejen_tapak_fk
FOREIGN KEY (tapak_id)
REFERENCES public.tapak(id);

ALTER TABLE ONLY public.ejen
ADD CONSTRAINT ejen_profile_fk
FOREIGN KEY (profile_id)
REFERENCES public.profil(id);

ALTER TABLE ONLY public.hasil_imbasan ADD CONSTRAINT fk_hasil_ejen FOREIGN KEY (ejen_id) REFERENCES public.ejen(id) ON DELETE CASCADE;
ALTER TABLE ONLY public.hasil_imbasan
ADD CONSTRAINT fk_hasil_profil_tugasan
FOREIGN KEY (profil_tugasan_id)
REFERENCES public.x_profil_tugasan(id)
ON DELETE CASCADE;

ALTER TABLE ONLY public.tugasan ADD CONSTRAINT fk_jenis FOREIGN KEY (jenis_id) REFERENCES public.jenis_tugasan(id);
ALTER TABLE ONLY public.x_profil_tugasan ADD CONSTRAINT fk_xprofil_status FOREIGN KEY (status_id) REFERENCES public.status(id);
ALTER TABLE ONLY public.x_profil_tugasan
ADD CONSTRAINT x_profil_tugasan_profil_id_fkey
FOREIGN KEY (profil_id)
REFERENCES public.profil(id)
ON DELETE CASCADE;

ALTER TABLE ONLY public.x_profil_tugasan
ADD CONSTRAINT x_profil_tugasan_tugasan_id_fkey
FOREIGN KEY (tugasan_id)
REFERENCES public.tugasan(id)
ON DELETE CASCADE;
ALTER TABLE ONLY public.organisasi ADD CONSTRAINT organisasi_pelanggan_id_fkey FOREIGN KEY (pelanggan_id) REFERENCES public.pelanggan(id) ON DELETE CASCADE;
ALTER TABLE ONLY public.profil ADD CONSTRAINT profil_tapak_id_fkey FOREIGN KEY (tapak_id) REFERENCES public.tapak(id) ON DELETE CASCADE;
ALTER TABLE ONLY public.sub_organisasi ADD CONSTRAINT sub_organisasi_organisasi_id_fkey FOREIGN KEY (organisasi_id) REFERENCES public.organisasi(id) ON DELETE CASCADE;
ALTER TABLE ONLY public.tapak ADD CONSTRAINT tapak_sub_organisasi_id_fkey FOREIGN KEY (sub_organisasi_id) REFERENCES public.sub_organisasi(id) ON DELETE CASCADE;
ALTER TABLE ONLY public.users
ADD CONSTRAINT users_pelanggan_id_fkey
FOREIGN KEY (pelanggan_id)
REFERENCES public.pelanggan(id);
-- Profile-Agent relationship
ALTER TABLE ONLY public.x_profil_ejen
ADD CONSTRAINT x_profil_ejen_ejen_id_fkey
FOREIGN KEY (ejen_id)
REFERENCES public.ejen(id)
ON DELETE CASCADE;

ALTER TABLE ONLY public.x_profil_ejen
ADD CONSTRAINT x_profil_ejen_profil_id_fkey
FOREIGN KEY (profil_id)
REFERENCES public.profil(id)
ON DELETE CASCADE;

-- Profile-Task-Agent relationship
ALTER TABLE ONLY public.x_profil_tugasan_ejen
ADD CONSTRAINT x_profil_tugasan_ejen_ejen_id_fkey
FOREIGN KEY (ejen_id)
REFERENCES public.ejen(id)
ON DELETE CASCADE;

ALTER TABLE ONLY public.x_profil_tugasan_ejen
ADD CONSTRAINT x_profil_tugasan_ejen_profil_tugasan_id_fkey
FOREIGN KEY (profil_tugasan_id)
REFERENCES public.x_profil_tugasan(id)
ON DELETE CASCADE;
-- ============================================================
-- INSERT SEED DATA
-- ============================================================

-- -- Pelanggan
-- INSERT INTO public.pelanggan (id, kod, nama, keterangan, aktif)
-- VALUES (
--     :'pelanggan_json'::jsonb ->> 'id'
--     :'pelanggan_json'::jsonb ->> 'kod',
--     :'pelanggan_json'::jsonb ->> 'nama',
--     :'pelanggan_json'::jsonb ->> 'keterangan',
--     true
-- );


-- Pelanggan INSERT
INSERT INTO public.pelanggan (id, kod, nama, keterangan, aktif)
VALUES (
    (:'pelanggan_json'::jsonb ->> 'id')::INTEGER,
    :'pelanggan_json'::jsonb ->> 'kod',
    :'pelanggan_json'::jsonb ->> 'nama',
    :'pelanggan_json'::jsonb ->> 'keterangan',
    true
);

-- Users
INSERT INTO public.users (id, pelanggan_id, username, nama, role, force_password_change, email, password) VALUES
 (1, 1, 'HangTuah', 'Super Admin 1', 'super admin', false, 'superadmin1@agct.com.my', 'PDawrM6ihWtC'),
 (2, 1, 'HangJebat', 'Super Admin 2', 'super admin', false, 'superadmin2@agct.com.my', 'bjFFsRXibI2N'),
 (3, 1, 'HangLekiu', 'Super Admin 3', 'super admin', false, 'superadmin3@agct.com.my', 'bIvPmGdRVGUM');
 


-- COPY public.users (id, username, password, role, created_at, pelanggan_id, nama, aktif, force_password_change, email, phone) FROM stdin;
-- 4   superadmin  pbkdf2_sha256$600000$Dzqc9LWxdElFmncYx6tW9A==$YEhBxFEcCgWA9WGYtUEAxFTJz/zHm71cvzM3h6Jx/2o=  super admin 2026-05-10 10:43:34.926637  1   Super Admin t   f   \N  \N
-- \.

INSERT INTO public.jenis_tugasan (id, nama)
VALUES
(1,'BIN_USED'),
(2,'BIN_DISK'),
(3,'LIBRARIES'),
(4,'CERT_KEYS'),
(5,'EXEC_SCRIPT'),
(6,'KERNEL_MODULES'),
(7,'NETWORK_PROTOCOL'),
(8,'NETWORK_APP'),
(9,'WEB_APP');

INSERT INTO public.tugasan
(
    id,
    nama,
    kod,
    protocol,
    ip_start,
    ip_end,
    keterangan,
    aktif,
    jenis_id
)
VALUES
(1,'Binaries Used','BIN_USED',NULL,NULL,NULL,'Detect binaries used',true,1),
(2,'Binaries on Disk','BIN_DISK',NULL,NULL,NULL,'Detect binaries on disk',true,2),
(3,'Libraries','LIBRARIES',NULL,NULL,NULL,'Detect libraries',true,3),
(4,'Certificates','CERT_KEYS',NULL,NULL,NULL,'Detect certificates',true,4),
(5,'Executable Scripts','EXEC_SCRIPT',NULL,NULL,NULL,'Detect executable scripts',true,5),
(6,'Kernel Modules','KERNEL_MODULES',NULL,NULL,NULL,'Detect kernel modules',true,6),
(7,'Network Protocols','NETWORK_PROTOCOL',NULL,NULL,NULL,'Detect network protocols',true,7),
(8,'Network Applications','NETWORK_APP',NULL,NULL,NULL,'Detect network applications',true,8),
(9,'Web Applications','WEB_APP',NULL,NULL,NULL,'Detect web applications',true,9); 

INSERT INTO public.status (id, kod_status)
VALUES
(1,'in process'),
(2,'telah dijadualkan'),
(3,'selesai'),
(4,'gagal');

-- ============================================================
-- INITIALIZE SEQUENCES AFTER SEED DATA
-- ============================================================

SELECT pg_catalog.setval('public.pelanggan_id_seq', 1, true);
SELECT pg_catalog.setval('public.users_id_seq', 3, true);
SELECT pg_catalog.setval('public.jenis_tugasan_id_seq', 9, true);
SELECT pg_catalog.setval('public.tugasan_id_seq', 9, true);
SELECT pg_catalog.setval('public.status_id_seq', 4, true);

-- ============================================================
-- BLOCKCHAIN HASH FUNCTION FOR hasil_imbasan
-- ============================================================

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE OR REPLACE FUNCTION public.set_hasil_imbasan_hash()
RETURNS TRIGGER AS $$
DECLARE
    prev_hash_val TEXT;
    row_data JSONB;
    computed_hash TEXT;
BEGIN
    -- 1. Get the hash of the previous row
    SELECT row_hash
    INTO prev_hash_val
    FROM public.hasil_imbasan
    ORDER BY id DESC
    LIMIT 1;

    -- 2. Build a JSONB representation of the new row
    --    excluding row_hash
    row_data := to_jsonb(NEW) - 'row_hash';

    -- 3. Add the previous hash to the chain
    row_data := row_data || jsonb_build_object(
        'prev_hash',
        prev_hash_val
    );

    -- 4. Compute SHA-256 hash
    computed_hash := encode(
        public.digest(row_data::text, 'sha256'),
        'hex'
    );

    -- 5. Assign the computed values
    NEW.prev_hash := prev_hash_val;
    NEW.row_hash := computed_hash;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_hasil_imbasan_hash
BEFORE INSERT ON public.hasil_imbasan
FOR EACH ROW
EXECUTE FUNCTION public.set_hasil_imbasan_hash();
-- ============================================================
-- BLOCKCHAIN INITIAL STATE
-- ============================================================
-- No genesis record is inserted.
-- The first hasil_imbasan record starts the hash chain
-- with prev_hash = NULL.


-- ============================================================
-- VERIFICATION QUERY (optional - comment out if not needed)
-- ============================================================
-- SELECT id, profil_tugasan_id, ejen_id, hasil, prev_hash, row_hash, created_at 
-- FROM public.hasil_imbasan 
-- ORDER BY id;

-- ============================================================
-- END OF SCRIPT
-- ============================================================
