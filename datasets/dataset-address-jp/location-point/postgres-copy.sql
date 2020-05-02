-- Import records from CSV files

\COPY city_block FROM '/data/datasets/address-jp/location-reference/locref-17.0a.csv' DELIMITER ',' CSV HEADER;

\COPY town FROM '/data/datasets/address-jp/location-reference/locref-12.0b.csv' DELIMITER ',' CSV HEADER;
