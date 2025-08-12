
CREATE TABLE public.contribution (
    purchase_id character varying NOT NULL,
    product_id character varying NOT NULL,
    contribution_factor double precision NOT NULL
);
ALTER TABLE public.contribution OWNER TO postgres;

CREATE TABLE public.products (
    product_id character varying NOT NULL,
    product_name character varying NOT NULL,
    material_id character varying NOT NULL,
    plant_id character varying NOT NULL
);
ALTER TABLE public.products OWNER TO postgres;

CREATE TABLE public.purchase_emissions (
    purchase_id character varying NOT NULL,
    emissions_value double precision NOT NULL
);
ALTER TABLE public.purchase_emissions OWNER TO postgres;

CREATE TABLE public.purchases (
    purchase_id character varying NOT NULL,
    purchase_name character varying,
    material_id character varying NOT NULL,
    country_of_origin_id character varying NOT NULL,
    quantity double precision NOT NULL,
    quantity_unit character varying NOT NULL
);
ALTER TABLE public.purchases OWNER TO postgres;


COPY public.contribution (purchase_id, product_id, contribution_factor) FROM stdin;
PU11	PR11	1
PU13	PR11	0.5
PU12	PR12	1
PU13	PR12	0.5
PU21	PR21	1
PU32	PR32	1
PU43	PR41	1
\.

COPY public.products (product_id, product_name, material_id, plant_id) FROM stdin;
PR11	Acetone Manchester	M1	PL1
PR12	Acetone Scranton	M1	PL2
PR21	Butene Manchester	M2	PL1
PR32	Chlorine Scranton	M3	PL2
PR41	Diorite Manchester	M4	PL1
\.

COPY public.purchase_emissions (purchase_id, emissions_value) FROM stdin;
PU11	1
PU12	2
PU13	3
PU21	4
PU32	5
\.

COPY public.purchases (purchase_id, purchase_name, material_id, country_of_origin_id, quantity, quantity_unit) FROM stdin;
PU11	Acetone from Argentina	M1	AR	100	kg
PU12	Acetone from Belgium	M1	BE	50	kg
PU13	Acetone from Croatia	M1	HR	200	kg
PU21	Butene from Argentina	M2	AR	10000	g
PU43	Diorite from Croatia	M3	HR	100	kg
PU32	\N	M3	BE	100	kg
\.

ALTER TABLE ONLY public.contribution
    ADD CONSTRAINT contribution_pkey PRIMARY KEY (purchase_id, product_id);

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (product_id);

ALTER TABLE ONLY public.purchase_emissions
    ADD CONSTRAINT purchase_emissions_pkey PRIMARY KEY (purchase_id);

ALTER TABLE ONLY public.purchases
    ADD CONSTRAINT purchases_pkey PRIMARY KEY (purchase_id);
