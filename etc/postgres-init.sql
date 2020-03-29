-- Create a user and a schema on PostgreSQL.
-- To substitute environmental variables on the fly, run a command below.
--
-- $ ( echo "cat <<EOF" ; grep -e "^--" -e "^$" -v postgres-init.sql ; echo EOF ) | sh
--
-- Example environmental variables are:
-- SANDBOX_POSTGRES_USERNAME=developer
-- SANDBOX_POSTGRES_PASSWORD=strong-password
-- SANDBOX_POSTGRES_DBNAME=sandbox

CREATE USER ${SANDBOX_POSTGRES_USERNAME} WITH PASSWORD '${SANDBOX_POSTGRES_PASSWORD}' CREATEDB;

CREATE DATABASE ${SANDBOX_POSTGRES_DBNAME} WITH OWNER ${SANDBOX_POSTGRES_USERNAME} ENCODING 'utf8';

\c ${SANDBOX_POSTGRES_DBNAME}

CREATE SCHEMA IF NOT EXISTS playground AUTHORIZATION ${SANDBOX_POSTGRES_USERNAME};

ALTER ROLE ${SANDBOX_POSTGRES_USERNAME} SET search_path TO playground;
