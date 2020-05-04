-- Import records from CSV files

\COPY prefecture FROM '/data/datasets/address-jp/prefecture.csv' WITH ( FORMAT CSV, HEADER TRUE, NULL '' )

\COPY city FROM '/data/datasets/address-jp/city.csv' WITH ( FORMAT CSV, HEADER TRUE, NULL '' )
