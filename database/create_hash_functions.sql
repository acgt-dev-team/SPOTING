-- delete foreign key constraints
ALTER TABLE public.hasil_imbasan DROP CONSTRAINT fk_hasil_ejen 
ALTER TABLE public.hasil_imbasan DROP CONSTRAINT fk_hasil_profil_tugasan;

-- insert genesis record
INSERT INTO public.hasil_imbasan (id, profil_tugasan_id, ejen_id, hasil, prev_hash, row_hash) VALUES (1, 1, 1, '{"key": "value", "status": "success"}','', '');

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