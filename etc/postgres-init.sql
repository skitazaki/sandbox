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

CREATE SCHEMA IF NOT EXISTS ${SANDBOX_POSTGRES_DBNAME} AUTHORIZATION ${SANDBOX_POSTGRES_USERNAME};
