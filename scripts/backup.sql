--
-- PostgreSQL database dump
--

\restrict 5chd837JQzaLkk3H1g6lDhWI8fNAGR0WfhTSkltNUemdeDgN4xJUAX5UzoaVATo

-- Dumped from database version 18.3
-- Dumped by pg_dump version 18.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: ejen; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ejen (
    id bigint NOT NULL,
    ip_address inet NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    tapak_id bigint NOT NULL,
    tugasan_id bigint
);


ALTER TABLE public.ejen OWNER TO postgres;

--
-- Name: ejen_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.ejen ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.ejen_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: hasil_imbasan; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.hasil_imbasan (
    id bigint NOT NULL,
    profil_tugasan_id bigint NOT NULL,
    ejen_id bigint NOT NULL,
    hasil json NOT NULL,
    created_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.hasil_imbasan OWNER TO postgres;

--
-- Name: hasil_imbasan_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.hasil_imbasan_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.hasil_imbasan_id_seq OWNER TO postgres;

--
-- Name: hasil_imbasan_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.hasil_imbasan_id_seq OWNED BY public.hasil_imbasan.id;


--
-- Name: jenis_tugasan; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.jenis_tugasan (
    id integer NOT NULL,
    nama character varying(100) NOT NULL
);


ALTER TABLE public.jenis_tugasan OWNER TO postgres;

--
-- Name: jenis_tugasan_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.jenis_tugasan_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.jenis_tugasan_id_seq OWNER TO postgres;

--
-- Name: jenis_tugasan_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.jenis_tugasan_id_seq OWNED BY public.jenis_tugasan.id;


--
-- Name: organisasi; Type: TABLE; Schema: public; Owner: postgres
--

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

--
-- Name: organisasi_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.organisasi_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.organisasi_id_seq OWNER TO postgres;

--
-- Name: organisasi_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.organisasi_id_seq OWNED BY public.organisasi.id;


--
-- Name: pelanggan; Type: TABLE; Schema: public; Owner: postgres
--

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

--
-- Name: pelanggan_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pelanggan_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.pelanggan_id_seq OWNER TO postgres;

--
-- Name: pelanggan_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.pelanggan_id_seq OWNED BY public.pelanggan.id;


--
-- Name: profil; Type: TABLE; Schema: public; Owner: postgres
--

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

--
-- Name: profil_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.profil_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.profil_id_seq OWNER TO postgres;

--
-- Name: profil_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.profil_id_seq OWNED BY public.profil.id;


--
-- Name: status; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.status (
    id integer NOT NULL,
    kod_status character varying(20) NOT NULL
);


ALTER TABLE public.status OWNER TO postgres;

--
-- Name: status_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.status_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.status_id_seq OWNER TO postgres;

--
-- Name: status_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.status_id_seq OWNED BY public.status.id;


--
-- Name: sub_organisasi; Type: TABLE; Schema: public; Owner: postgres
--

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

--
-- Name: sub_organisasi_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sub_organisasi_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sub_organisasi_id_seq OWNER TO postgres;

--
-- Name: sub_organisasi_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sub_organisasi_id_seq OWNED BY public.sub_organisasi.id;


--
-- Name: tapak; Type: TABLE; Schema: public; Owner: postgres
--

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

--
-- Name: tapak_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tapak_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tapak_id_seq OWNER TO postgres;

--
-- Name: tapak_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tapak_id_seq OWNED BY public.tapak.id;


--
-- Name: tugasan; Type: TABLE; Schema: public; Owner: postgres
--

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

--
-- Name: tugasan_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tugasan_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tugasan_id_seq OWNER TO postgres;

--
-- Name: tugasan_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tugasan_id_seq OWNED BY public.tugasan.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

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

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: x_profil_tugasan; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.x_profil_tugasan (
    profil_id integer NOT NULL,
    tugasan_id integer NOT NULL,
    jadualkan_pada timestamp without time zone,
    selesai_pada timestamp without time zone,
    id integer NOT NULL,
    status_id integer
);


ALTER TABLE public.x_profil_tugasan OWNER TO postgres;

--
-- Name: x_profil_tugasan_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.x_profil_tugasan_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.x_profil_tugasan_id_seq OWNER TO postgres;

--
-- Name: x_profil_tugasan_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.x_profil_tugasan_id_seq OWNED BY public.x_profil_tugasan.id;


--
-- Name: hasil_imbasan id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hasil_imbasan ALTER COLUMN id SET DEFAULT nextval('public.hasil_imbasan_id_seq'::regclass);


--
-- Name: jenis_tugasan id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.jenis_tugasan ALTER COLUMN id SET DEFAULT nextval('public.jenis_tugasan_id_seq'::regclass);


--
-- Name: organisasi id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organisasi ALTER COLUMN id SET DEFAULT nextval('public.organisasi_id_seq'::regclass);


--
-- Name: pelanggan id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pelanggan ALTER COLUMN id SET DEFAULT nextval('public.pelanggan_id_seq'::regclass);


--
-- Name: profil id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.profil ALTER COLUMN id SET DEFAULT nextval('public.profil_id_seq'::regclass);


--
-- Name: status id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.status ALTER COLUMN id SET DEFAULT nextval('public.status_id_seq'::regclass);


--
-- Name: sub_organisasi id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sub_organisasi ALTER COLUMN id SET DEFAULT nextval('public.sub_organisasi_id_seq'::regclass);


--
-- Name: tapak id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tapak ALTER COLUMN id SET DEFAULT nextval('public.tapak_id_seq'::regclass);


--
-- Name: tugasan id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tugasan ALTER COLUMN id SET DEFAULT nextval('public.tugasan_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: x_profil_tugasan id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.x_profil_tugasan ALTER COLUMN id SET DEFAULT nextval('public.x_profil_tugasan_id_seq'::regclass);


--
-- Data for Name: ejen; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ejen (id, ip_address, created_at, tapak_id, tugasan_id) FROM stdin;
7	169.254.32.153	2026-07-03 11:20:53.773504	1	\N
\.


--
-- Data for Name: hasil_imbasan; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.hasil_imbasan (id, profil_tugasan_id, ejen_id, hasil, created_at) FROM stdin;
8	111	7	[{"CryptoDetails": "", "ExecutablePath": "C:\\\\Program Files\\\\Microsoft OneDrive\\\\26.106.0603.0003\\\\OneDrive.Sync.Service.exe", "PID": "25300", "Process": "OneDrive.Sync.Service.exe", "Protocol": "TLS", "RemoteIP": "104.208.16.92", "RemotePort": "443", "Role": "CLIENT", "ScanTimeUTC": "2026-07-03T03:35:56.440078", "ScriptPath": ""}, {"CryptoDetails": "", "ExecutablePath": "C:\\\\Program Files (x86)\\\\Microsoft\\\\Edge\\\\Application\\\\msedge.exe", "PID": "14924", "Process": "msedge.exe", "Protocol": "TLS", "RemoteIP": "2606:4700:440b::6812:2715", "RemotePort": "443", "Role": "CLIENT", "ScanTimeUTC": "2026-07-03T03:35:56.440078", "ScriptPath": ""}, {"CryptoDetails": "", "ExecutablePath": "C:\\\\Program Files\\\\Microsoft OneDrive\\\\26.106.0603.0003\\\\OneDrive.Sync.Service.exe", "PID": "25300", "Process": "OneDrive.Sync.Service.exe", "Protocol": "TLS", "RemoteIP": "20.184.175.1", "RemotePort": "443", "Role": "CLIENT", "ScanTimeUTC": "2026-07-03T03:35:56.440078", "ScriptPath": ""}, {"CryptoDetails": "", "ExecutablePath": "C:\\\\Program Files (x86)\\\\AnyDesk\\\\AnyDesk.exe", "PID": "8408", "Process": "AnyDesk.exe", "Protocol": "TLS", "RemoteIP": "15.235.229.125", "RemotePort": "443", "Role": "CLIENT", "ScanTimeUTC": "2026-07-03T03:35:56.440078", "ScriptPath": ""}, {"CryptoDetails": "", "ExecutablePath": "C:\\\\Program Files (x86)\\\\Microsoft\\\\Edge\\\\Application\\\\msedge.exe", "PID": "14924", "Process": "msedge.exe", "Protocol": "TLS", "RemoteIP": "2406:da18:30d:8117:5ae5:bf5d:54b7:1a2a", "RemotePort": "443", "Role": "CLIENT", "ScanTimeUTC": "2026-07-03T03:35:56.440078", "ScriptPath": ""}, {"CryptoDetails": "", "ExecutablePath": "C:\\\\Users\\\\Admin\\\\AppData\\\\Local\\\\GitHubDesktop\\\\app-3.6.2\\\\GitHubDesktop.exe", "PID": "33964", "Process": "GitHubDesktop.exe", "Protocol": "TLS", "RemoteIP": "140.82.114.25", "RemotePort": "443", "Role": "CLIENT", "ScanTimeUTC": "2026-07-03T03:35:56.440078", "ScriptPath": ""}, {"CryptoDetails": "", "ExecutablePath": "C:\\\\Program Files (x86)\\\\Microsoft\\\\Edge\\\\Application\\\\msedge.exe", "PID": "14924", "Process": "msedge.exe", "Protocol": "TLS", "RemoteIP": "2406:da18:30d:8117:f28a:18d2:e50d:a36e", "RemotePort": "443", "Role": "CLIENT", "ScanTimeUTC": "2026-07-03T03:35:56.440078", "ScriptPath": ""}, {"CryptoDetails": "", "ExecutablePath": "C:\\\\Users\\\\Admin\\\\AppData\\\\Local\\\\Programs\\\\Microsoft VS Code\\\\Code.exe", "PID": "14844", "Process": "Code.exe", "Protocol": "TLS", "RemoteIP": "2603:1061:14:160::1", "RemotePort": "443", "Role": "CLIENT", "ScanTimeUTC": "2026-07-03T03:35:56.440078", "ScriptPath": ""}, {"CryptoDetails": "", "ExecutablePath": "", "PID": "8648", "Process": "", "Protocol": "TLS", "RemoteIP": "2603:1040:a06:6::2", "RemotePort": "443", "Role": "CLIENT", "ScanTimeUTC": "2026-07-03T03:35:56.440078", "ScriptPath": ""}, {"CryptoDetails": "", "ExecutablePath": "C:\\\\Program Files (x86)\\\\Microsoft\\\\Edge\\\\Application\\\\msedge.exe", "PID": "14924", "Process": "msedge.exe", "Protocol": "TLS", "RemoteIP": "172.188.155.25", "RemotePort": "443", "Role": "CLIENT", "ScanTimeUTC": "2026-07-03T03:35:56.440078", "ScriptPath": ""}, {"CryptoDetails": "", "ExecutablePath": "C:\\\\Program Files (x86)\\\\Microsoft\\\\Edge\\\\Application\\\\msedge.exe", "PID": "14924", "Process": "msedge.exe", "Protocol": "TLS", "RemoteIP": "2606:4700:4408::ac40:9bd1", "RemotePort": "443", "Role": "CLIENT", "ScanTimeUTC": "2026-07-03T03:35:56.440078", "ScriptPath": ""}, {"CryptoDetails": "", "ExecutablePath": "C:\\\\Program Files (x86)\\\\AnyDesk\\\\AnyDesk.exe", "PID": "8408", "Process": "AnyDesk.exe", "Protocol": "TLS", "RemoteIP": "15.235.229.121", "RemotePort": "443", "Role": "CLIENT", "ScanTimeUTC": "2026-07-03T03:35:56.440078", "ScriptPath": ""}]	2026-07-03 11:35:58.769952
9	112	7	null	2026-07-03 11:37:52.445556
10	114	7	null	2026-07-07 11:15:13.568324
11	115	7	[{"algorithm": "AES", "detection_pattern": "AES-(128|192|256)", "file_path": "C:\\\\xampp\\\\htdocs\\\\test.php", "key_size": "256", "language": "php", "library_or_api": "AES-(128|192|256)", "primitive": "block-cipher"}, {"algorithm": "AES", "detection_pattern": "openssl_encrypt", "file_path": "C:\\\\xampp\\\\htdocs\\\\test.php", "key_size": "unknown", "language": "php", "library_or_api": "openssl_encrypt", "primitive": "block-cipher"}]	2026-07-07 11:20:46.268451
12	116	7	[{"category": "block-cipher", "evidence": "AES-(128|192|256)", "item": "AES", "property": "key_size", "resource": "C:\\\\xampp\\\\htdocs\\\\test.php", "resource_type": "php", "severity": "info", "value": "256"}, {"category": "block-cipher", "evidence": "openssl_encrypt", "item": "AES", "property": "key_size", "resource": "C:\\\\xampp\\\\htdocs\\\\test.php", "resource_type": "php", "severity": "info", "value": "unknown"}]	2026-07-07 11:34:23.181507
13	117	7	null	2026-07-07 12:03:34.21472
14	118	7	null	2026-07-07 12:14:26.400471
15	119	7	[{"category": "block-cipher", "evidence": "string,string,crypto-library", "item": "AES", "property": "key_length", "resource": "C:\\\\Program Files\\\\PostgreSQL\\\\18\\\\bin\\\\postgres.exe", "resource_type": "C", "severity": "info", "value": "128"}, {"category": "block-cipher", "evidence": "string,crypto-library", "item": "3DES", "property": "key_length", "resource": "C:\\\\Program Files\\\\PostgreSQL\\\\18\\\\bin\\\\postgres.exe", "resource_type": "C", "severity": "info", "value": "112"}, {"category": "block-cipher", "evidence": "string,crypto-library", "item": "DES", "property": "key_length", "resource": "C:\\\\Program Files\\\\PostgreSQL\\\\18\\\\bin\\\\postgres.exe", "resource_type": "C", "severity": "info", "value": "56"}, {"category": "block-cipher", "evidence": "crypto-library", "item": "ARIA", "property": "key_length", "resource": "C:\\\\Program Files\\\\PostgreSQL\\\\18\\\\bin\\\\postgres.exe", "resource_type": "C", "severity": "info", "value": "unknown"}, {"category": "mac", "evidence": "string,crypto-library", "item": "HMAC", "property": "key_length", "resource": "C:\\\\Program Files\\\\PostgreSQL\\\\18\\\\bin\\\\postgres.exe", "resource_type": "C", "severity": "info", "value": "unknown"}, {"category": "hash-function", "evidence": "crypto-library", "item": "SHA-2", "property": "key_length", "resource": "C:\\\\Program Files\\\\PostgreSQL\\\\18\\\\bin\\\\postgres.exe", "resource_type": "C", "severity": "info", "value": "unknown"}, {"category": "hash-function", "evidence": "crypto-library", "item": "SHA-256", "property": "key_length", "resource": "C:\\\\Program Files\\\\PostgreSQL\\\\18\\\\bin\\\\postgres.exe", "resource_type": "C", "severity": "info", "value": "unknown"}, {"category": "hash-function", "evidence": "crypto-library", "item": "MD5", "property": "key_length", "resource": "C:\\\\Program Files\\\\PostgreSQL\\\\18\\\\bin\\\\postgres.exe", "resource_type": "C", "severity": "info", "value": "unknown"}, {"category": "hash-function", "evidence": "crypto-library", "item": "bcrypt", "property": "key_length", "resource": "C:\\\\Program Files\\\\PostgreSQL\\\\18\\\\bin\\\\postgres.exe", "resource_type": "C", "severity": "info", "value": "unknown"}, {"category": "digital-signature", "evidence": "crypto-library", "item": "DSA", "property": "key_length", "resource": "C:\\\\Program Files\\\\PostgreSQL\\\\18\\\\bin\\\\postgres.exe", "resource_type": "C", "severity": "info", "value": "unknown"}, {"category": "key-agreement", "evidence": "string,crypto-library", "item": "ECDH", "property": "key_length", "resource": "C:\\\\Program Files\\\\PostgreSQL\\\\18\\\\bin\\\\postgres.exe", "resource_type": "C", "severity": "info", "value": "unknown"}, {"category": "digital-signature", "evidence": "crypto-library", "item": "BLS", "property": "key_length", "resource": "C:\\\\Program Files\\\\PostgreSQL\\\\18\\\\bin\\\\postgres.exe", "resource_type": "C", "severity": "info", "value": "unknown"}, {"category": "tls", "evidence": "string,crypto-library", "item": "TLS", "property": "key_length", "resource": "C:\\\\Program Files\\\\PostgreSQL\\\\18\\\\bin\\\\postgres.exe", "resource_type": "C", "severity": "info", "value": "unknown"}, {"category": "ssl", "evidence": "string,crypto-library", "item": "SSL", "property": "key_length", "resource": "C:\\\\Program Files\\\\PostgreSQL\\\\18\\\\bin\\\\postgres.exe", "resource_type": "C", "severity": "info", "value": "unknown"}, {"category": "ssh", "evidence": "string,crypto-library", "item": "SSH", "property": "key_length", "resource": "C:\\\\Program Files\\\\PostgreSQL\\\\18\\\\bin\\\\postgres.exe", "resource_type": "C", "severity": "info", "value": "unknown"}, {"category": "block-cipher", "evidence": "crypto-library", "item": "SEED", "property": "key_length", "resource": "C:\\\\Program Files\\\\PostgreSQL\\\\18\\\\bin\\\\postgres.exe", "resource_type": "C", "severity": "info", "value": "unknown"}]	2026-07-07 14:36:27.266029
16	120	7	null	2026-07-07 14:37:51.557441
17	121	7	[{"category": "block-cipher", "evidence": "string,string,crypto-library", "item": "AES", "property": "key_length", "resource": "C:\\\\Program Files\\\\PostgreSQL\\\\18\\\\bin\\\\postgres.exe", "resource_type": "C", "severity": "info", "value": "128"}, {"category": "block-cipher", "evidence": "string,crypto-library", "item": "3DES", "property": "key_length", "resource": "C:\\\\Program Files\\\\PostgreSQL\\\\18\\\\bin\\\\postgres.exe", "resource_type": "C", "severity": "info", "value": "112"}, {"category": "block-cipher", "evidence": "string,crypto-library", "item": "DES", "property": "key_length", "resource": "C:\\\\Program Files\\\\PostgreSQL\\\\18\\\\bin\\\\postgres.exe", "resource_type": "C", "severity": "info", "value": "56"}, {"category": "block-cipher", "evidence": "crypto-library", "item": "ARIA", "property": "key_length", "resource": "C:\\\\Program Files\\\\PostgreSQL\\\\18\\\\bin\\\\postgres.exe", "resource_type": "C", "severity": "info", "value": "unknown"}, {"category": "mac", "evidence": "string,crypto-library", "item": "HMAC", "property": "key_length", "resource": "C:\\\\Program Files\\\\PostgreSQL\\\\18\\\\bin\\\\postgres.exe", "resource_type": "C", "severity": "info", "value": "unknown"}, {"category": "hash-function", "evidence": "crypto-library", "item": "SHA-2", "property": "key_length", "resource": "C:\\\\Program Files\\\\PostgreSQL\\\\18\\\\bin\\\\postgres.exe", "resource_type": "C", "severity": "info", "value": "unknown"}, {"category": "hash-function", "evidence": "crypto-library", "item": "SHA-256", "property": "key_length", "resource": "C:\\\\Program Files\\\\PostgreSQL\\\\18\\\\bin\\\\postgres.exe", "resource_type": "C", "severity": "info", "value": "unknown"}, {"category": "hash-function", "evidence": "crypto-library", "item": "MD5", "property": "key_length", "resource": "C:\\\\Program Files\\\\PostgreSQL\\\\18\\\\bin\\\\postgres.exe", "resource_type": "C", "severity": "info", "value": "unknown"}, {"category": "hash-function", "evidence": "crypto-library", "item": "bcrypt", "property": "key_length", "resource": "C:\\\\Program Files\\\\PostgreSQL\\\\18\\\\bin\\\\postgres.exe", "resource_type": "C", "severity": "info", "value": "unknown"}, {"category": "digital-signature", "evidence": "crypto-library", "item": "DSA", "property": "key_length", "resource": "C:\\\\Program Files\\\\PostgreSQL\\\\18\\\\bin\\\\postgres.exe", "resource_type": "C", "severity": "info", "value": "unknown"}, {"category": "key-agreement", "evidence": "string,crypto-library", "item": "ECDH", "property": "key_length", "resource": "C:\\\\Program Files\\\\PostgreSQL\\\\18\\\\bin\\\\postgres.exe", "resource_type": "C", "severity": "info", "value": "unknown"}, {"category": "digital-signature", "evidence": "crypto-library", "item": "BLS", "property": "key_length", "resource": "C:\\\\Program Files\\\\PostgreSQL\\\\18\\\\bin\\\\postgres.exe", "resource_type": "C", "severity": "info", "value": "unknown"}, {"category": "tls", "evidence": "string,crypto-library", "item": "TLS", "property": "key_length", "resource": "C:\\\\Program Files\\\\PostgreSQL\\\\18\\\\bin\\\\postgres.exe", "resource_type": "C", "severity": "info", "value": "unknown"}, {"category": "ssl", "evidence": "string,crypto-library", "item": "SSL", "property": "key_length", "resource": "C:\\\\Program Files\\\\PostgreSQL\\\\18\\\\bin\\\\postgres.exe", "resource_type": "C", "severity": "info", "value": "unknown"}, {"category": "ssh", "evidence": "string,crypto-library", "item": "SSH", "property": "key_length", "resource": "C:\\\\Program Files\\\\PostgreSQL\\\\18\\\\bin\\\\postgres.exe", "resource_type": "C", "severity": "info", "value": "unknown"}, {"category": "block-cipher", "evidence": "crypto-library", "item": "SEED", "property": "key_length", "resource": "C:\\\\Program Files\\\\PostgreSQL\\\\18\\\\bin\\\\postgres.exe", "resource_type": "C", "severity": "info", "value": "unknown"}]	2026-07-07 15:37:08.840176
\.


--
-- Data for Name: jenis_tugasan; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.jenis_tugasan (id, nama) FROM stdin;
1	Network Scanning
2	Security Audit
3	Infrastructure Monitoring
\.


--
-- Data for Name: organisasi; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.organisasi (id, pelanggan_id, kod, nama, keterangan, aktif, cipta_pada, kemaskini_pada, pegawai_tadbir, jawatan) FROM stdin;
3	1	ORG003	Jabatan Sukarelawan Negara (RELA)	Ibu Pejabat D2 Putrajaya	t	2026-05-15 13:57:54.169094	2026-05-15 13:57:54.169094	Masidon Jumaili	Pegawai Tadbir F28
1	1	ORG001	Jabatan Imigresen Malaysia	Pegawai di Ibu Pejabat Putrajaya	t	2026-05-10 10:45:42.444154	2026-05-10 10:45:42.444154	Jamil Bin Borhan	Pegawai Tadbir F28
2	1	ORG002	Jabatan Penjara Malaysia	Pegawai Tadbir	t	2026-05-10 11:23:59.357145	2026-05-10 11:23:59.357145	Pn Suhaila Ibrahim	Pegawai Tadbir F 42
5	1	ORG004	Agensi Antidadah Kebangsaan		t	2026-06-10 00:25:11.56383	2026-06-10 00:25:11.56383		
7	1	ORG006	Jabatan Pendaftaran Pertubuhan Malaysia		t	2026-06-10 00:26:01.5821	2026-06-10 00:26:01.5821		
9	1	ORG007	Jabatan Pendafataran Negara	Tingkat 18	t	2026-06-14 19:55:41.022153	2026-06-14 19:55:41.022153	Hussein Jumali	Timbalan Penolong Pengarah
\.


--
-- Data for Name: pelanggan; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pelanggan (id, kod, nama, keterangan, aktif, cipta_pada, kemaskini_pada) FROM stdin;
1	PLG001	Tenaga Nasional Berhad	Pelanggan utama untuk projek utiliti dan penyelenggaraan infrastruktur.	t	2026-05-10 10:38:43.369956	2026-05-10 10:38:43.369956
2	PLG002	Telekom Malaysia	Pelanggan bagi sistem rangkaian dan komunikasi.	t	2026-05-10 10:38:43.369956	2026-05-10 10:38:43.369956
3	PLG003	Majlis Bandaraya Johor Bahru	Pelanggan sektor kerajaan tempatan untuk pengurusan bandar.	t	2026-05-10 10:38:43.369956	2026-05-10 10:38:43.369956
\.


--
-- Data for Name: profil; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.profil (id, tapak_id, kod, nama, keterangan, aktif, cipta_pada, kemaskini_pada, execution_type, is_scheduled, report_template, report_format, scheduled_at, execution_status, cron_enabled, frequency, cron_expression) FROM stdin;
2	2	PRF002	test	test	t	2026-05-10 11:26:11.719523	2026-05-10 11:26:11.719523	SCHEDULED	t	DEFAULT	EXCEL	2026-05-12 11:00:00	telah dijadualkan	f	\N	\N
14	2	PRF013	test02	test	t	2026-05-19 19:23:44.530812	2026-05-19 19:23:44.530812	IMMEDIATE	f	DEFAULT	EXCEL	\N	execution completed	f	\N	\N
24	2	PRF023	test11	test	t	2026-05-21 03:30:09.192899	2026-05-21 03:30:09.192899	IMMEDIATE	f	DEFAULT	EXCEL	\N	execution completed	f	\N	\N
25	2	PRF024	test12	test	t	2026-05-21 03:49:02.269911	2026-05-21 03:49:02.269911	IMMEDIATE	f	DEFAULT	EXCEL	\N	execution completed	f	\N	\N
15	2	PRF014	test03	test	t	2026-05-19 19:28:01.952351	2026-05-19 19:28:01.952351	IMMEDIATE	f	DEFAULT	EXCEL	\N	execution completed	f	\N	\N
26	2	PRF025	test13	test	t	2026-05-21 03:51:55.263444	2026-05-21 03:51:55.263444	IMMEDIATE	f	DEFAULT	EXCEL	\N	gagal	f	\N	\N
16	2	PRF015	test05	test	t	2026-05-19 19:45:55.014449	2026-05-19 19:45:55.014449	IMMEDIATE	f	DEFAULT	EXCEL	\N	execution completed	f	\N	\N
27	2	PRF026	test20	test	t	2026-05-21 03:55:06.389819	2026-05-21 03:55:06.389819	IMMEDIATE	f	DEFAULT	EXCEL	\N	gagal	f	\N	\N
17	2	PRF016	test06	test	t	2026-05-19 19:51:17.523873	2026-05-19 19:51:17.523873	IMMEDIATE	f	DEFAULT	EXCEL	\N	execution completed	f	\N	\N
28	2	PRF027	test21	test	t	2026-05-21 04:28:33.540631	2026-05-21 04:28:33.540631	IMMEDIATE	f	DEFAULT	EXCEL	\N	gagal	f	\N	\N
7	2	PRF006	testtest	test	t	2026-05-19 07:50:57.15304	2026-05-19 07:50:57.15304	IMMEDIATE	f	DEFAULT	EXCEL	\N	execution completed	f	\N	\N
29	2	PRF028	test25	test	t	2026-05-21 04:36:42.945564	2026-05-21 04:36:42.945564	IMMEDIATE	f	DEFAULT	EXCEL	\N	gagal	f	\N	\N
30	2	PRF029	test30	test	t	2026-05-21 04:43:06.009765	2026-05-21 04:43:06.009765	IMMEDIATE	f	DEFAULT	EXCEL	\N	gagal	f	\N	\N
8	2	PRF007	new prof	test	t	2026-05-19 08:00:46.052901	2026-05-19 08:00:46.052901	IMMEDIATE	f	DEFAULT	EXCEL	\N	execution completed	f	\N	\N
18	2	PRF017	test07	test	t	2026-05-19 19:56:41.098852	2026-05-19 19:56:41.098852	IMMEDIATE	f	DEFAULT	EXCEL	\N	execution completed	f	\N	\N
34	4	PRF033	test2	test	t	2026-05-21 13:43:26.333907	2026-05-21 13:43:26.333907	IMMEDIATE	f	DEFAULT	EXCEL	\N	execution completed	f	\N	\N
21	2	PRF020	test1222	test	t	2026-05-20 13:19:12.660767	2026-05-20 13:19:12.660767	IMMEDIATE	f	DEFAULT	EXCEL	\N	in process	f	\N	\N
31	3	PRF030	test	test	t	2026-05-21 13:00:14.96581	2026-05-21 13:00:14.96581	IMMEDIATE	f	DEFAULT	EXCEL	\N	gagal	f	\N	\N
22	2	PRF021	test09	test	t	2026-05-21 03:13:23.731403	2026-05-21 03:13:23.731403	IMMEDIATE	f	DEFAULT	EXCEL	\N	execution completed	f	\N	\N
13	2	PRF012	test01	test	t	2026-05-19 19:19:44.927975	2026-05-19 19:19:44.927975	IMMEDIATE	f	DEFAULT	EXCEL	\N	execution completed	f	\N	\N
32	4	PRF031	test	test	t	2026-05-21 13:36:03.616063	2026-05-21 13:36:03.616063	IMMEDIATE	f	DEFAULT	EXCEL	\N	execution completed	f	\N	\N
23	2	PRF022	test10	test	t	2026-05-21 03:20:15.223721	2026-05-21 03:20:15.223721	IMMEDIATE	f	DEFAULT	EXCEL	\N	execution completed	f	\N	\N
35	4	PRF034	test3	test	t	2026-05-21 13:53:19.470457	2026-05-21 13:53:19.470457	IMMEDIATE	f	DEFAULT	EXCEL	\N	execution completed	f	\N	\N
33	4	PRF032	test1	test	t	2026-05-21 13:38:37.154134	2026-05-21 13:38:37.154134	IMMEDIATE	f	DEFAULT	EXCEL	\N	execution completed	f	\N	\N
36	4	PRF035	test5	test	t	2026-05-21 13:59:22.611307	2026-05-21 13:59:22.611307	IMMEDIATE	f	DEFAULT	EXCEL	\N	execution completed	f	\N	\N
1	1	PRF001	PC Windows di Kaunter dan Back Office	Imbasan PC Windows	t	2026-05-10 10:50:55.603496	2026-05-10 10:50:55.603496	SCHEDULED	t	DEFAULT	EXCEL	2026-06-18 23:30:00	telah dijadualkan	f		
41	1	PRF036	New Server	test	t	2026-07-03 11:34:54.833572	2026-07-03 11:34:54.833572	IMMEDIATE	f	DEFAULT	EXCEL	\N	execution completed	f		
42	1	PRF037	Test New	test	t	2026-07-07 11:12:20.383823	2026-07-07 11:12:20.383823	IMMEDIATE	f	DEFAULT	EXCEL	\N	execution completed	f		
43	1	PRF038	New Test 2	test	t	2026-07-07 11:19:56.264211	2026-07-07 11:19:56.264211	IMMEDIATE	f	DEFAULT	EXCEL	\N	execution completed	f		
44	1	PRF039	Test Profile	test	t	2026-07-07 11:34:01.6008	2026-07-07 11:34:01.6008	IMMEDIATE	f	DEFAULT	EXCEL	\N	execution completed	f		
45	1	PRF040	Test Profil 01	test	t	2026-07-07 12:14:03.40559	2026-07-07 12:14:03.40559	IMMEDIATE	f	DEFAULT	EXCEL	\N	execution completed	f		
46	1	PRF041	Test Profil 02	test	t	2026-07-07 14:28:21.188889	2026-07-07 14:28:21.188889	IMMEDIATE	f	DEFAULT	EXCEL	\N	execution completed	f		
47	1	PRF042	Test Profil 04	test	t	2026-07-07 14:37:33.962852	2026-07-07 14:37:33.962852	IMMEDIATE	f	DEFAULT	EXCEL	\N	execution completed	f		
48	1	PRF043	test profil 05	test	t	2026-07-07 14:40:10.505483	2026-07-07 14:40:10.505483	IMMEDIATE	f	DEFAULT	EXCEL	\N	execution completed	f		
\.


--
-- Data for Name: status; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.status (id, kod_status) FROM stdin;
1	in process
2	telah dijadualkan
3	selesai
4	gagal
\.


--
-- Data for Name: sub_organisasi; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sub_organisasi (id, organisasi_id, kod, nama, keterangan, aktif, cipta_pada, kemaskini_pada, pegawai_tadbir, jawatan) FROM stdin;
2	2	SUB002	test	test	t	2026-05-10 11:24:11.596496	2026-05-10 11:24:11.596496	test	test
3	2	SUB003	test1	test	t	2026-05-21 12:58:48.432368	2026-05-21 12:58:48.432368	person1	person2
1	1	SUB001	Bahagian Penguatkuasaan	Pusat Operasi Putrajaya	t	2026-05-10 10:50:26.000519	2026-05-10 10:50:26.000519	Henry Anak Zachary	Pegawai IT F42
4	1	SUB004	Bahagian Depoh dan Tahanan	Ibu Pejabat Kuala Lumpur	t	2026-05-25 20:57:01.916676	2026-05-25 20:57:01.916676	Thamalingam A/L Subramaniam	Pegawai F28
7	9	SUB005	Bahagian Pendaftaran	Tingkat 10 Putrajaya	t	2026-06-14 19:55:47.893372	2026-06-14 19:55:47.893372	Mukhriz Ismail	Pegawai Gred 38
\.


--
-- Data for Name: tapak; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tapak (id, sub_organisasi_id, kod, nama, keterangan, aktif, cipta_pada, kemaskini_pada, nombor, aras, alamat_baris_1, alamat_baris_2, bandar, negeri, negara, pegawai_tadbir, jawatan) FROM stdin;
2	2	TPK002	test	test	t	2026-05-10 11:25:34.85363	2026-05-10 11:25:34.85363	\N	\N	\N	\N	\N	\N	\N	test	test
3	3	TPK003	test	test	t	2026-05-21 12:59:22.114949	2026-05-21 12:59:22.114949	\N	\N	\N	\N	\N	\N	\N	test	test
4	3	TPK004	test	test	t	2026-05-21 12:59:22.132122	2026-05-21 12:59:22.132122	\N	\N	\N	\N	\N	\N	\N	test	test
1	1	TPK001	Cawangan Kelana Jaya	Pengurus Cawangan	t	2026-05-10 10:50:44.807121	2026-05-26 15:36:32.813023	\N	\N	\N	\N	\N	\N	\N	Nor Saadah Ibrahim	TPPK
\.


--
-- Data for Name: tugasan; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tugasan (id, nama, protocol, ip_start, ip_end, cipta_pada, kod, keterangan, aktif, kemaskini_pada, jenis_id) FROM stdin;
1	Running Binaries Scan	LOCAL	127.0.0.1	127.0.0.1	2026-07-03 11:19:30.773742	BIN_USED	Scan running binaries	t	2026-07-03 11:19:30.773742	1
2	Disk Binaries Scan	LOCAL	127.0.0.1	127.0.0.1	2026-07-03 11:19:30.773742	BIN_DISK	Scan binaries on disk	t	2026-07-03 11:19:30.773742	1
3	Libraries Scan	LOCAL	127.0.0.1	127.0.0.1	2026-07-03 11:19:30.773742	LIBRARIES	Scan installed libraries	t	2026-07-03 11:19:30.773742	1
4	Kernel Module Scan	LOCAL	127.0.0.1	127.0.0.1	2026-07-03 11:19:30.773742	KERNEL	Scan kernel modules	t	2026-07-03 11:19:30.773742	1
5	Certificate & Key Scan	LOCAL	127.0.0.1	127.0.0.1	2026-07-03 11:19:30.773742	CERT_KEYS	Scan certificates and keys	t	2026-07-03 11:19:30.773742	1
6	Executable Script Scan	LOCAL	127.0.0.1	127.0.0.1	2026-07-03 11:19:30.773742	EXEC_SCRIPT	Scan executable scripts	t	2026-07-03 11:19:30.773742	1
7	Web Application Scan	LOCAL	127.0.0.1	127.0.0.1	2026-07-03 11:19:30.773742	WEB_APP	Scan web applications	t	2026-07-03 11:19:30.773742	1
8	Network Application Scan	NETWORK	0.0.0.0	255.255.255.255	2026-07-03 11:19:30.773742	NETWORK_APP	Scan network applications	t	2026-07-03 11:19:30.773742	2
9	Network Protocol Scan	NETWORK	0.0.0.0	255.255.255.255	2026-07-03 11:19:30.773742	NETWORK_PROTOCOL	Scan network protocols	t	2026-07-03 11:19:30.773742	2
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, password, role, created_at, pelanggan_id, nama, aktif, force_password_change, email, phone) FROM stdin;
8	jam.saidin	0V2f8vOq4*NG	admin	2026-05-14 05:18:06.969107	\N	Jamilus Saidin	t	t	\N	\N
18	micheal.jackson	iYwtgbMg93$!	admin	2026-05-28 15:36:24.824159	\N	Michael Jackson	t	f	\N	\N
2	hassan.bakri	IKD%R4tJct&a	admin	2026-05-10 10:43:34.926637	1	Hassan Bakri	t	t	\N	\N
29	roslihashim5	6do&gWe96bP#	admin	2026-06-17 15:28:54.272966	\N	Rosli Hashim	t	t	\N	\N
1	superadmin	pbkdf2_sha256$600000$Dzqc9LWxdElFmncYx6tW9A==$YEhBxFEcCgWA9WGYtUEAxFTJz/zHm71cvzM3h6Jx/2o=	super admin	2026-05-10 10:43:34.926637	1	Super Admin	t	f	\N	\N
39	zamirulibrah	pbkdf2_sha256$600000$JQrshRWqtVrkAJY0al/aSQ==$JPGhQoDsV6YBeHmOyKRrD9mklru2gQP5SWBmSftEwl8=	user	2026-07-01 22:09:54.381154	\N	Zamirul Ibrahim	t	t	\N	\N
40	zamriibrahim	pbkdf2_sha256$600000$sFBcDfAOaVWZMCB+MOZCjQ==$weVxlkEhe4joxit8loZcuGPzMctslmUHqKfNvgjJ3ik=	user	2026-07-01 22:12:16.904388	\N	Zamirul Ibrahim	t	t	\N	\N
41	resalresal01	pbkdf2_sha256$600000$FxN6OgHAxxRL+mbfu4gXqA==$Ye5U+WmXi+ax5R4AMZUCVZmP2TEaJNRuY4PUdk285/s=	user	2026-07-03 21:11:04.505146	\N	Resal	t	f	mszresal06@gmail.com	
20	abangzakaria	pbkdf2_sha256$600000$GuhVKvttczsEngBJW/marA==$U9LLwLbVImVHPDOJ06xB8opJpjza8VnT3d+uIA8i/sU=	admin	2026-05-30 11:05:22.464335	\N	Abang Zakaria Abang Johari	t	t	\N	\N
42	resal.resal0123	pbkdf2_sha256$600000$cwEc4z9SdWWWAH0lUGGTMQ==$44q2gvMBgrWnUomrQvrYk7x20v2FO4XcW/DBlZvXlBM=	user	2026-07-06 13:38:24.940266	\N	Resal	t	t	\N	\N
\.


--
-- Data for Name: x_profil_tugasan; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.x_profil_tugasan (profil_id, tugasan_id, jadualkan_pada, selesai_pada, id, status_id) FROM stdin;
1	8	\N	\N	109	1
1	7	\N	\N	110	1
41	8	\N	2026-07-03 11:35:58.803986	111	3
41	7	\N	2026-07-03 11:37:52.467535	112	3
1	3	\N	\N	113	1
42	7	\N	2026-07-07 11:15:13.577036	114	3
43	7	\N	2026-07-07 11:20:46.273339	115	3
44	7	\N	2026-07-07 11:34:23.185746	116	3
44	1	\N	2026-07-07 12:03:34.219321	117	3
45	1	\N	2026-07-07 12:14:26.404282	118	3
46	1	\N	2026-07-07 14:36:27.274308	119	3
47	1	\N	2026-07-07 14:37:51.561973	120	3
48	1	\N	2026-07-07 15:37:08.844855	121	3
\.


--
-- Name: ejen_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ejen_id_seq', 7, true);


--
-- Name: hasil_imbasan_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.hasil_imbasan_id_seq', 17, true);


--
-- Name: jenis_tugasan_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.jenis_tugasan_id_seq', 3, true);


--
-- Name: organisasi_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.organisasi_id_seq', 9, true);


--
-- Name: pelanggan_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pelanggan_id_seq', 3, true);


--
-- Name: profil_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.profil_id_seq', 48, true);


--
-- Name: status_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.status_id_seq', 3, true);


--
-- Name: sub_organisasi_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sub_organisasi_id_seq', 7, true);


--
-- Name: tapak_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tapak_id_seq', 9, true);


--
-- Name: tugasan_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tugasan_id_seq', 9, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 42, true);


--
-- Name: x_profil_tugasan_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.x_profil_tugasan_id_seq', 121, true);


--
-- Name: ejen ejen_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ejen
    ADD CONSTRAINT ejen_pkey PRIMARY KEY (id);


--
-- Name: ejen ejen_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ejen
    ADD CONSTRAINT ejen_unique UNIQUE (ip_address);


--
-- Name: hasil_imbasan hasil_imbasan_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hasil_imbasan
    ADD CONSTRAINT hasil_imbasan_pkey PRIMARY KEY (id);


--
-- Name: jenis_tugasan jenis_tugasan_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.jenis_tugasan
    ADD CONSTRAINT jenis_tugasan_pkey PRIMARY KEY (id);


--
-- Name: organisasi organisasi_kod_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organisasi
    ADD CONSTRAINT organisasi_kod_key UNIQUE (kod);


--
-- Name: organisasi organisasi_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organisasi
    ADD CONSTRAINT organisasi_pkey PRIMARY KEY (id);


--
-- Name: pelanggan pelanggan_kod_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pelanggan
    ADD CONSTRAINT pelanggan_kod_key UNIQUE (kod);


--
-- Name: pelanggan pelanggan_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pelanggan
    ADD CONSTRAINT pelanggan_pkey PRIMARY KEY (id);


--
-- Name: profil profil_kod_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.profil
    ADD CONSTRAINT profil_kod_key UNIQUE (kod);


--
-- Name: profil profil_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.profil
    ADD CONSTRAINT profil_pkey PRIMARY KEY (id);


--
-- Name: status status_kod_status_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.status
    ADD CONSTRAINT status_kod_status_key UNIQUE (kod_status);


--
-- Name: status status_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.status
    ADD CONSTRAINT status_pkey PRIMARY KEY (id);


--
-- Name: sub_organisasi sub_organisasi_kod_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sub_organisasi
    ADD CONSTRAINT sub_organisasi_kod_key UNIQUE (kod);


--
-- Name: sub_organisasi sub_organisasi_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sub_organisasi
    ADD CONSTRAINT sub_organisasi_pkey PRIMARY KEY (id);


--
-- Name: tapak tapak_kod_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tapak
    ADD CONSTRAINT tapak_kod_key UNIQUE (kod);


--
-- Name: tapak tapak_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tapak
    ADD CONSTRAINT tapak_pkey PRIMARY KEY (id);


--
-- Name: tugasan tugasan_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tugasan
    ADD CONSTRAINT tugasan_pkey PRIMARY KEY (id);


--
-- Name: x_profil_tugasan unique_profil_tugasan; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.x_profil_tugasan
    ADD CONSTRAINT unique_profil_tugasan UNIQUE (profil_id, tugasan_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: x_profil_tugasan x_profil_tugasan_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.x_profil_tugasan
    ADD CONSTRAINT x_profil_tugasan_pkey PRIMARY KEY (id);


--
-- Name: ix_organisasi_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_organisasi_id ON public.organisasi USING btree (id);


--
-- Name: ix_pelanggan_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_pelanggan_id ON public.pelanggan USING btree (id);


--
-- Name: ix_profil_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_profil_id ON public.profil USING btree (id);


--
-- Name: ix_sub_organisasi_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_sub_organisasi_id ON public.sub_organisasi USING btree (id);


--
-- Name: ix_tapak_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_tapak_id ON public.tapak USING btree (id);


--
-- Name: ix_tugasan_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_tugasan_id ON public.tugasan USING btree (id);


--
-- Name: ejen ejen_tapak_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ejen
    ADD CONSTRAINT ejen_tapak_fk FOREIGN KEY (tapak_id) REFERENCES public.tapak(id);


--
-- Name: ejen ejen_tugasan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ejen
    ADD CONSTRAINT ejen_tugasan_id_fkey FOREIGN KEY (tugasan_id) REFERENCES public.tugasan(id);


--
-- Name: hasil_imbasan fk_hasil_ejen; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hasil_imbasan
    ADD CONSTRAINT fk_hasil_ejen FOREIGN KEY (ejen_id) REFERENCES public.ejen(id) ON DELETE CASCADE;


--
-- Name: hasil_imbasan fk_hasil_profil_tugasan; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hasil_imbasan
    ADD CONSTRAINT fk_hasil_profil_tugasan FOREIGN KEY (profil_tugasan_id) REFERENCES public.x_profil_tugasan(id) ON DELETE CASCADE;


--
-- Name: tugasan fk_jenis; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tugasan
    ADD CONSTRAINT fk_jenis FOREIGN KEY (jenis_id) REFERENCES public.jenis_tugasan(id);


--
-- Name: x_profil_tugasan fk_xprofil_status; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.x_profil_tugasan
    ADD CONSTRAINT fk_xprofil_status FOREIGN KEY (status_id) REFERENCES public.status(id);


--
-- Name: organisasi organisasi_pelanggan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organisasi
    ADD CONSTRAINT organisasi_pelanggan_id_fkey FOREIGN KEY (pelanggan_id) REFERENCES public.pelanggan(id) ON DELETE CASCADE;


--
-- Name: profil profil_tapak_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.profil
    ADD CONSTRAINT profil_tapak_id_fkey FOREIGN KEY (tapak_id) REFERENCES public.tapak(id) ON DELETE CASCADE;


--
-- Name: sub_organisasi sub_organisasi_organisasi_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sub_organisasi
    ADD CONSTRAINT sub_organisasi_organisasi_id_fkey FOREIGN KEY (organisasi_id) REFERENCES public.organisasi(id) ON DELETE CASCADE;


--
-- Name: tapak tapak_sub_organisasi_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tapak
    ADD CONSTRAINT tapak_sub_organisasi_id_fkey FOREIGN KEY (sub_organisasi_id) REFERENCES public.sub_organisasi(id) ON DELETE CASCADE;


--
-- Name: users users_pelanggan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pelanggan_id_fkey FOREIGN KEY (pelanggan_id) REFERENCES public.pelanggan(id);


--
-- Name: x_profil_tugasan x_profil_tugasan_profil_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.x_profil_tugasan
    ADD CONSTRAINT x_profil_tugasan_profil_id_fkey FOREIGN KEY (profil_id) REFERENCES public.profil(id) ON DELETE CASCADE;


--
-- Name: x_profil_tugasan x_profil_tugasan_tugasan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.x_profil_tugasan
    ADD CONSTRAINT x_profil_tugasan_tugasan_id_fkey FOREIGN KEY (tugasan_id) REFERENCES public.tugasan(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict 5chd837JQzaLkk3H1g6lDhWI8fNAGR0WfhTSkltNUemdeDgN4xJUAX5UzoaVATo

