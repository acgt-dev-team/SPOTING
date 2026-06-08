--
-- PostgreSQL database dump
--

\restrict F0KTy7meKSgd1jzW2fJ1Q042qpo9Z1KekMmW90UEpI0uBmnbqaYEW9fnlSvFfMI

-- Dumped from database version 16.14 (Ubuntu 16.14-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.14 (Ubuntu 16.14-0ubuntu0.24.04.1)

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
5	127.0.0.1	2026-05-21 04:24:04.059804	1	7
\.


--
-- Data for Name: hasil_imbasan; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.hasil_imbasan (id, profil_tugasan_id, ejen_id, hasil, created_at) FROM stdin;
6	84	5	[{"cbom_data": {"algorithm": "RSA", "file_type": "certificate", "issuer": "Test CA", "key_size": "2048", "path": "C:/test.pem", "subject": "localhost"}}]	2026-05-21 13:36:13.736245
7	100	5	[{"cbom_data": {"algorithm": "RSA", "file_type": "certificate", "issuer": "Test CA", "key_size": "2048", "path": "C:/test.pem", "subject": "localhost"}}]	2026-05-21 21:58:52.925164
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
2	1	ORG002	Jabatan Kastam Malaysia		t	2026-05-10 11:23:59.357145	2026-05-10 11:23:59.357145	Pn Suhaila Ibrahim	Pegawai Tadbir F 42
3	1	ORG003	Jabatan Sukarelawan Negara (RELA)	Ibu Pejabat D2 Putrajaya	t	2026-05-15 13:57:54.169094	2026-05-15 13:57:54.169094	Masidon Jumaili	Pegawai Tadbir F28
1	1	ORG001	Jabatan Imigresen Malaysia	Pegawai di Ibu Pejabat Putrajaya	t	2026-05-10 10:45:42.444154	2026-05-10 10:45:42.444154	Jamil Bin Borhan	Pegawai Tadbir F28
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
19	1	PRF018	Imbasan Server MyIMMS	Server MyIMMS kecuali mainframe	t	2026-05-20 13:16:40.360118	2026-05-20 13:16:40.360118	SCHEDULED	t	DEFAULT	EXCEL	2026-05-27 00:00:00	telah dijadualkan	f	\N	\N
1	1	PRF001	PC Windows di Kaunter dan Back Office	Imbasan PC Windows	t	2026-05-10 10:50:55.603496	2026-05-10 10:50:55.603496	SCHEDULED	t	DEFAULT	EXCEL	2026-05-31 23:30:00	execution completed	f	\N	\N
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
5	Server Security Audit	UDP	10.0.0.1	10.0.0.20	2026-05-10 10:53:32.706769	TGS002	Audit keselamatan pelayan dalaman.	t	2026-05-10 10:53:32.706769	1
6	Data Center Monitoring	ICMP	172.16.0.1	172.16.0.10	2026-05-10 10:53:32.706769	TGS003	Pemantauan pusat data.	t	2026-05-10 10:53:32.706769	1
7	Test	TCP	127.0.0.1	127.0.0.1	2026-05-19 18:49:40.223736	TEST001	test	t	2026-05-19 18:49:40.223736	2
4	Network Scan Office A	TCP	192.168.0.10	192.168.1.13	2026-05-10 10:53:32.706769	TGS001	Imbasan rangkaian pejabat utama.	t	2026-05-10 10:53:32.706769	1
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, password, role, created_at, pelanggan_id, nama, aktif, force_password_change, email, phone) FROM stdin;
1	superadmin	123456	super admin	2026-05-10 10:43:34.926637	1	Super Admin	t	f	\N	\N
8	jam.saidin	0V2f8vOq4*NG	admin	2026-05-14 05:18:06.969107	\N	Jamilus Saidin	t	t	\N	\N
18	micheal.jackson	iYwtgbMg93$!	admin	2026-05-28 15:36:24.824159	\N	Michael Jackson	t	f	\N	\N
20	abang.zakaria	123456	admin	2026-05-30 11:05:22.464335	\N	Abang Zakaria Abang Johari	t	f	\N	\N
2	hassan.bakri	IKD%R4tJct&a	admin	2026-05-10 10:43:34.926637	1	Hassan Bakri	t	t	\N	\N
\.


--
-- Data for Name: x_profil_tugasan; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.x_profil_tugasan (profil_id, tugasan_id, jadualkan_pada, selesai_pada, id, status_id) FROM stdin;
21	6	\N	\N	70	1
2	6	\N	\N	22	1
21	7	\N	\N	71	1
27	6	\N	\N	72	1
27	7	\N	\N	73	1
28	4	\N	\N	74	1
28	5	\N	\N	75	1
7	4	\N	\N	23	3
28	6	\N	\N	76	1
28	7	\N	\N	77	1
7	5	\N	\N	24	3
7	6	\N	\N	25	3
30	6	\N	\N	78	1
30	7	\N	\N	79	1
13	7	\N	\N	38	3
8	4	\N	\N	26	3
14	7	\N	\N	39	3
8	5	\N	\N	27	3
18	6	\N	\N	49	3
8	6	\N	\N	28	3
18	7	\N	\N	48	3
18	5	\N	\N	50	3
18	4	\N	\N	51	3
19	4	\N	\N	52	1
19	5	\N	\N	53	1
19	6	\N	\N	54	1
19	7	\N	\N	55	1
15	7	\N	\N	40	4
15	4	\N	\N	41	4
15	5	\N	\N	42	4
15	6	\N	\N	43	4
16	7	\N	\N	44	4
32	6	\N	\N	83	3
16	6	\N	\N	45	4
22	6	\N	\N	60	4
22	7	\N	\N	61	4
17	6	\N	\N	46	3
17	7	\N	\N	47	3
32	7	\N	\N	84	3
23	4	\N	\N	62	3
23	5	\N	\N	63	3
35	4	\N	\N	93	3
23	6	\N	\N	64	3
23	7	\N	\N	65	3
33	4	\N	\N	85	4
35	5	\N	\N	94	3
24	6	\N	\N	66	3
33	5	\N	\N	86	4
24	7	\N	\N	67	3
33	6	\N	\N	87	4
35	6	\N	\N	95	3
25	6	\N	\N	68	3
33	7	\N	\N	88	4
25	7	\N	\N	69	3
35	7	\N	\N	96	4
34	4	\N	\N	89	4
34	5	\N	\N	90	4
34	6	\N	\N	91	4
34	7	\N	\N	92	4
36	4	\N	\N	97	3
36	5	\N	\N	98	3
36	6	\N	\N	99	3
36	7	\N	\N	100	3
1	4	\N	\N	6	4
1	5	\N	\N	80	4
1	6	\N	\N	81	4
1	7	\N	\N	82	4
\.


--
-- Name: ejen_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ejen_id_seq', 5, true);


--
-- Name: hasil_imbasan_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.hasil_imbasan_id_seq', 7, true);


--
-- Name: jenis_tugasan_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.jenis_tugasan_id_seq', 3, true);


--
-- Name: organisasi_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.organisasi_id_seq', 4, true);


--
-- Name: pelanggan_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pelanggan_id_seq', 3, true);


--
-- Name: profil_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.profil_id_seq', 36, true);


--
-- Name: status_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.status_id_seq', 3, true);


--
-- Name: sub_organisasi_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sub_organisasi_id_seq', 4, true);


--
-- Name: tapak_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tapak_id_seq', 5, true);


--
-- Name: tugasan_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tugasan_id_seq', 7, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 20, true);


--
-- Name: x_profil_tugasan_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.x_profil_tugasan_id_seq', 100, true);


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

\unrestrict F0KTy7meKSgd1jzW2fJ1Q042qpo9Z1KekMmW90UEpI0uBmnbqaYEW9fnlSvFfMI

