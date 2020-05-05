--
-- Resources:
--   * geo_grid_lv4
--

-- DROP TABLE IF EXISTS geo_grid_lv4 ;
CREATE TABLE IF NOT EXISTS geo_grid_lv4 (
  "gid" INTEGER NOT NULL UNIQUE,
  "mesh_level4" CHAR(9) NOT NULL UNIQUE,
  "city_code" CHAR(5) NOT NULL,
  "geom" GEOGRAPHY(MULTIPOLYGON) NOT NULL UNIQUE
) ;

COMMENT ON TABLE "geo_grid_lv4" IS 'Grid code at level 4 and geometry' ;

COMMENT ON COLUMN "geo_grid_lv4"."gid" IS 'ID sequence' ;
COMMENT ON COLUMN "geo_grid_lv4"."mesh_level4" IS 'Mesh ID of 500m square' ;
COMMENT ON COLUMN "geo_grid_lv4"."city_code" IS 'JIS city code' ;
COMMENT ON COLUMN "geo_grid_lv4"."geom" IS 'Geometry as GeoJSON' ;
