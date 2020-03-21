DROP TABLE server_info IF EXISTS;
CREATE TABLE server_info (
  id INTEGER NOT NULL PRIMARY KEY,
  name varchar(255) NOT NULL,
  kind varchar(31) NOT NULL,
  url varchar(255) NOT NULL,
  defaults varchar(255),
  responseClass varchar(255)
);
CREATE INDEX server_info_name ON server_info(name);
