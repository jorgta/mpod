BEGIN;

CREATE TABLE "data_publarticle" (
    "id" integer NOT NULL PRIMARY KEY,
    "title" varchar(255) NOT NULL,
    "authors" varchar(255) NOT NULL,
    "journal" varchar(127) NOT NULL,
    "year" integer,
    "volume" varchar(6),
    "issue" integer,
    "first_page" integer,
    "last_page" integer,
    "reference" varchar(14) NOT NULL,
    "pages_number" integer
)
;
CREATE TABLE "data_property" (
    "id" integer NOT NULL PRIMARY KEY,
    "tag" varchar(255) NOT NULL,
    "name" varchar(255) NOT NULL,
    "description" varchar(511) NOT NULL,
    "tensor_dimensions" varchar(10) NOT NULL,
    "units" varchar(25) NOT NULL,
    "units_detail" varchar(60) NOT NULL
)
;
CREATE TABLE "data_experimentalparcond" (
    "id" integer NOT NULL PRIMARY KEY,
    "tag" varchar(255) NOT NULL,
    "name" varchar(255) NOT NULL,
    "description" varchar(511) NOT NULL,
    "units" varchar(25) NOT NULL,
    "units_detail" varchar(60) NOT NULL
)
;
CREATE TABLE "data_datafile_property" (
    "id" integer NOT NULL PRIMARY KEY,
    "datafile_id" integer NOT NULL,
    "property_id" integer NOT NULL REFERENCES "data_property" ("id"),
    UNIQUE ("datafile_id", "property_id")
)
;
CREATE TABLE "data_datafile" (
    "code" integer NOT NULL PRIMARY KEY,
    "filename" varchar(13) NOT NULL,
    "cod_code" integer,
    "phase_generic" varchar(255),
    "phase_name" varchar(255) NOT NULL,
    "chemical_formula" varchar(255) NOT NULL,
    "publication_id" integer NOT NULL REFERENCES "data_publarticle" ("id")
)
;
CREATE INDEX "data_datafile_8564e1ab" ON "data_datafile" ("publication_id");
COMMIT;
