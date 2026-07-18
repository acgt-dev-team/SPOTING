--
-- PostgreSQL database dump
--

-- \restrict 0lyzu7xI8i62JQZf76ITLt5TSMDEfMJE19VPrwaEE3rQCUUvkpgUJs92nqRtktA

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

-- CREATE TABLE public.hasil_imbasan (
--     id bigint NOT NULL,
--     profil_tugasan_id bigint NOT NULL,
--     ejen_id bigint NOT NULL,
--     hasil json NOT NULL,
--     created_at timestamp without time zone DEFAULT now()

-- );


CREATE TABLE public.hasil_imbasan (
    id bigint NOT NULL,
    profil_tugasan_id bigint NOT NULL,
    ejen_id bigint NOT NULL,
    hasil json NOT NULL,
    created_at timestamp without time zone DEFAULT now(),
    prev_hash TEXT,
    row_hash TEXT
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
-- to change table name to public.akaun


-- CREATE TABLE public.akaun (
--     id integer NOT NULL,
--     id_akaun character varying(32) NOT NULL,
--     kata_laluan character varying(32) NOT NULL,
--     nama_akaun character varying(64),
--     peranan character varying(20) DEFAULT 'pengguna'::character varying NOT NULL,
--     cipta_pada timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
--     pelanggan_id integer,
--     aktif boolean DEFAULT true,
--     tukar_kata_laluan boolean DEFAULT true,
--     emel character varying,
--     no_telefon character varying
-- );

-- ALTER TABLE public.akaun akaun TO postgres;

-- CREATE SEQUENCE public.akaun_id_seq
--     AS integer
--     START WITH 1
--     INCREMENT BY 1
--     NO MINVALUE
--     NO MAXVALUE
--     CACHE 1;


-- ALTER SEQUENCE public.akaun_id_seq OWNER TO postgres;

-- --
-- -- Name: akaun_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
-- --

-- ALTER SEQUENCE public.akaun_id_seq OWNED BY public.akaun.id;


CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(24) NOT NULL,
    password character varying(255) NOT NULL,
    role character varying(20) DEFAULT 'user'::character varying NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    pelanggan_id integer,
    nama character varying,
    aktif boolean DEFAULT true,
    force_password_change boolean DEFAULT true,
    deleted_at timestamp without time zone,
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
-- Name: auth_sessions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_sessions (
    id integer NOT NULL,
    token_hash character varying(64) NOT NULL,
    user_id integer NOT NULL,
    created_at timestamp without time zone NOT NULL,
    expires_at timestamp without time zone NOT NULL,
    revoked_at timestamp without time zone
);


ALTER TABLE public.auth_sessions OWNER TO postgres;

--
-- Name: auth_sessions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_sessions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.auth_sessions_id_seq OWNER TO postgres;

--
-- Name: auth_sessions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_sessions_id_seq OWNED BY public.auth_sessions.id;


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


-- COPY public.users (id, username, password, role, created_at, pelanggan_id, nama, aktif, force_password_change, deleted_at, email, phone) FROM stdin;
-- 1	hangtuah01	pbkdf2_sha256$600000$SY/ljhCoZ7kF0J0qMxn4WA==$MA1Hl0OMA+7XvzCHVHsaIGBjOvnWsrD71/ME6ptxJyg=	super admin	2026-05-10 10:43:34.926637	1	Super Admin	t	f	\N	\N	\N
-- 2	hangjebat01	pbkdf2_sha256$600000$t3u19N4vkuclnlx8Im0VGw==$YPW2J2dMoYhvCmH3Z3Xj/q8kVVJYBE6exzG0cw1x8L0=	super admin	2026-05-10 10:43:34.926637	1	Super Admin	t	f	\N	\N	\N
-- 3	hanglekiu01	pbkdf2_sha256$600000$XbGr9OHccg1Nvy7TAWq4+w==$R0JPkwiVzLhLpaHM6FeGwZaJ/N/KN90Ln1t/Kh+SAyk=	super admin	2026-05-10 10:43:34.926637	1	Super Admin	t	f	\N	\N	\N
-- \.

--
-- Name: x_profil_tugasan_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.x_profil_tugasan_id_seq OWNED BY public.x_profil_tugasan.id;


--
-- Name: hasil_imbasan id; Type: DEFAULT; Schema: public; Owner: postgres


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


-- Name: akaun id; Type: DEFAULT; Schema: public; Owner: postgres
--

-- * ALTER TABLE ONLY public.akaun ALTER COLUMN id SET DEFAULT nextval('public.akaun_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: auth_sessions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_sessions ALTER COLUMN id SET DEFAULT nextval('public.auth_sessions_id_seq'::regclass);


--
-- Name: x_profil_tugasan id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.x_profil_tugasan ALTER COLUMN id SET DEFAULT nextval('public.x_profil_tugasan_id_seq'::regclass);


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
-- Name: auth_sessions auth_sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_sessions
    ADD CONSTRAINT auth_sessions_pkey PRIMARY KEY (id);


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


CREATE INDEX ix_auth_sessions_id ON public.auth_sessions USING btree (id);
CREATE UNIQUE INDEX ix_auth_sessions_token_hash ON public.auth_sessions USING btree (token_hash);
CREATE INDEX ix_auth_sessions_user_id ON public.auth_sessions USING btree (user_id);
CREATE INDEX ix_auth_sessions_expires_at ON public.auth_sessions USING btree (expires_at);


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
-- Name: auth_sessions auth_sessions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_sessions
    ADD CONSTRAINT auth_sessions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


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

-- \unrestrict 0lyzu7xI8i62JQZf76ITLt5TSMDEfMJE19VPrwaEE3rQCUUvkpgUJs92nqRtktA

