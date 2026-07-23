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

SET pelanggan_json = '{"id": 1, "kod":"KKP01", "nama": "Kementerian Dalam Negeri", "keterangan": "Kementerian" }';

-- ============================================================
-- CREATE TABLES
-- ============================================================

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

-- Ejen
CREATE TABLE public.ejen (
    id bigint NOT NULL,
    ip_address inet NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    tapak_id bigint NOT NULL,
    tugasan_id bigint
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

-- ============================================================
-- PRIMARY KEY CONSTRAINTS
-- ============================================================
ALTER TABLE ONLY public.ejen ADD CONSTRAINT ejen_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.ejen ADD CONSTRAINT ejen_unique UNIQUE (ip_address);
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

-- ============================================================
-- INDEXES
-- ============================================================
CREATE INDEX ix_organisasi_id ON public.organisasi USING btree (id);
CREATE INDEX ix_pelanggan_id ON public.pelanggan USING btree (id);
CREATE INDEX ix_profil_id ON public.profil USING btree (id);
CREATE INDEX ix_sub_organisasi_id ON public.sub_organisasi USING btree (id);
CREATE INDEX ix_tapak_id ON public.tapak USING btree (id);
CREATE INDEX ix_tugasan_id ON public.tugasan USING btree (id);

-- ============================================================
-- FOREIGN KEY CONSTRAINTS
-- ============================================================
-- ALTER TABLE ONLY public.ejen ADD CONSTRAINT ejen_tapak_fk FOREIGN KEY (tapak_id) REFERENCES public.tapak(id);
-- ALTER TABLE ONLY public.ejen ADD CONSTRAINT ejen_tugasan_id_fkey FOREIGN KEY (tugasan_id) REFERENCES public.tugasan(id);
ALTER TABLE ONLY public.hasil_imbasan ADD CONSTRAINT fk_hasil_ejen FOREIGN KEY (ejen_id) REFERENCES public.ejen(id) ON DELETE CASCADE;

ALTER TABLE ONLY public.tugasan ADD CONSTRAINT fk_jenis FOREIGN KEY (jenis_id) REFERENCES public.jenis_tugasan(id);
ALTER TABLE ONLY public.x_profil_tugasan ADD CONSTRAINT fk_xprofil_status FOREIGN KEY (status_id) REFERENCES public.status(id);
ALTER TABLE ONLY public.organisasi ADD CONSTRAINT organisasi_pelanggan_id_fkey FOREIGN KEY (pelanggan_id) REFERENCES public.pelanggan(id) ON DELETE CASCADE;
ALTER TABLE ONLY public.profil ADD CONSTRAINT profil_tapak_id_fkey FOREIGN KEY (tapak_id) REFERENCES public.tapak(id) ON DELETE CASCADE;
ALTER TABLE ONLY public.sub_organisasi ADD CONSTRAINT sub_organisasi_organisasi_id_fkey FOREIGN KEY (organisasi_id) REFERENCES public.organisasi(id) ON DELETE CASCADE;
ALTER TABLE ONLY public.tapak ADD CONSTRAINT tapak_sub_organisasi_id_fkey FOREIGN KEY (sub_organisasi_id) REFERENCES public.sub_organisasi(id) ON DELETE CASCADE;
ALTER TABLE ONLY public.users ADD CONSTRAINT users_pelanggan_id_fkey FOREIGN KEY (pelanggan_id) REFERENCES public.pelanggan(id);

-- ============================================================
-- INSERT SEED DATA
-- ============================================================

-- Pelanggan
INSERT INTO public.pelanggan (id, kod, nama, keterangan, aktif)
VALUES (
    :'customer_json'::jsonb ->> 'id'
    :'customer_json'::jsonb ->> 'kod',
    :'customer_json'::jsonb ->> 'nama',
    :'customer_json'::jsonb ->> 'keterangan',
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

-- ============================================================
-- BLOCKCHAIN HASH FUNCTION FOR hasil_imbasan
-- ============================================================
\c spoting;
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE OR REPLACE FUNCTION set_hasil_imbasan_hash()
RETURNS TRIGGER AS $$
DECLARE
    prev_hash_val TEXT;
    row_data JSONB;
    computed_hash TEXT;
BEGIN
    -- 1. Get the hash of the last inserted row (ordered by id)
    SELECT row_hash INTO prev_hash_val
    FROM hasil_imbasan
    ORDER BY id DESC
    LIMIT 1;

    -- 2. Build a JSONB representation of the new row, excluding row_hash
    row_data := to_jsonb(NEW) - 'row_hash';

    -- 3. Add the previous hash as an extra field (this creates the chain)
    row_data := row_data || jsonb_build_object('prev_hash', prev_hash_val);

    -- 4. Compute SHA-256 hash of the JSONB text and convert to hex
    computed_hash := encode(digest(row_data::text, 'sha256'), 'hex');

    -- 5. Assign the computed values to the NEW row
    NEW.prev_hash := prev_hash_val;
    NEW.row_hash := computed_hash;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_hasil_imbasan_hash
BEFORE INSERT ON hasil_imbasan
FOR EACH ROW
EXECUTE FUNCTION set_hasil_imbasan_hash();

-- ============================================================
-- INSERT GENESIS RECORD FOR hasil_imbasan
-- ============================================================

-- Temporarily disable the trigger to insert genesis record
-- We need to first insert the parent records (ejen and x_profil_tugasan)
-- since they have foreign key constraints

-- Insert sample ejen (needed for foreign key)
INSERT INTO public.ejen (id, ip_address, tapak_id, tugasan_id) 
VALUES (1, '127.0.0.1', 1, 1);

-- Insert sample x_profil_tugasan (needed for foreign key)
INSERT INTO public.x_profil_tugasan (id, profil_id, tugasan_id) 
VALUES (1, 1, 1);

-- Now insert the genesis record for hasil_imbasan with explicit NULL prev_hash and row_hash
-- The trigger will automatically compute the hash
INSERT INTO public.hasil_imbasan (id, profil_tugasan_id, ejen_id,machine_id, hasil, prev_hash, row_hash) 
VALUES (1, 1, 1, '00000000-0000-0000-0000-000000000000', '{"key": "value", "status": "success"}', NULL, NULL);

-- ============================================================
-- FINALIZE FOREIGN KEY CONSTRAINTS (ensure they are enabled)
-- ============================================================
-- Note: Foreign keys were added earlier, but we need to verify the genesis record inserted properly

ALTER TABLE ONLY public.hasil_imbasan ADD CONSTRAINT fk_hasil_profil_tugasan FOREIGN KEY (profil_tugasan_id) REFERENCES public.x_profil_tugasan(id) ON DELETE CASCADE;
-- ALTER TABLE ONLY public.x_profil_tugasan ADD CONSTRAINT x_profil_tugasan_profil_id_fkey FOREIGN KEY (profil_id) REFERENCES public.profil(id) ON DELETE CASCADE;
-- ALTER TABLE ONLY public.x_profil_tugasan ADD CONSTRAINT x_profil_tugasan_tugasan_id_fkey FOREIGN KEY (tugasan_id) REFERENCES public.tugasan(id) ON DELETE CASCADE;

-- ============================================================
-- VERIFICATION QUERY (optional - comment out if not needed)
-- ============================================================
-- SELECT id, profil_tugasan_id, ejen_id, hasil, prev_hash, row_hash, created_at 
-- FROM public.hasil_imbasan 
-- ORDER BY id;

-- ============================================================
-- END OF SCRIPT
-- ============================================================