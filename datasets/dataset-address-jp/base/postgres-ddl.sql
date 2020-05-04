--
-- Auto generated at 2020/05/04 13:12:42
--
-- Resources:
--   * prefecture
--   * city

-- DROP TABLE IF EXISTS prefecture ;
CREATE TABLE IF NOT EXISTS prefecture (
  "prefecture_code" VARCHAR(100),
  "prefecture_name" VARCHAR(100),
  "prefecture_type" VARCHAR(100),
  "prefecture_name_kana" VARCHAR(100),
  "prefecture_name_kana_large" VARCHAR(100),
  "prefecture_name_roman" VARCHAR(100)
) ;

COMMENT ON COLUMN "prefecture"."prefecture_code" IS 'Prefecture code with zero-padding two digits.' ;
COMMENT ON COLUMN "prefecture"."prefecture_name" IS 'Prefecture name in Japanese' ;
COMMENT ON COLUMN "prefecture"."prefecture_type" IS 'Prefecture type in Japanese' ;
COMMENT ON COLUMN "prefecture"."prefecture_name_kana" IS 'Prefecture name in Japanese Katakana' ;
COMMENT ON COLUMN "prefecture"."prefecture_name_kana_large" IS 'Prefecture name in Japanese Katakana with all large characters' ;
COMMENT ON COLUMN "prefecture"."prefecture_name_roman" IS 'Prefecture name in Japanese roman representation' ;


-- DROP TABLE IF EXISTS city ;
CREATE TABLE IF NOT EXISTS city (
  "prefecture_code" VARCHAR(100),
  "prefecture_name" VARCHAR(100),
  "city_code" VARCHAR(100),
  "city_name" VARCHAR(100),
  "city_type" VARCHAR(100),
  "city_name_level" VARCHAR(100),
  "city_name_with_space" VARCHAR(100),
  "city_name_kana" VARCHAR(100),
  "city_name_kana_large" VARCHAR(100),
  "city_name_roman" VARCHAR(100)
) ;

COMMENT ON COLUMN "city"."prefecture_code" IS 'Prefecture code with zero-padding two digits.' ;
COMMENT ON COLUMN "city"."prefecture_name" IS 'Prefecture name in Japanese' ;
COMMENT ON COLUMN "city"."city_code" IS 'City code with zero-padding two digits.' ;
COMMENT ON COLUMN "city"."city_name" IS 'City name in Japanese' ;
COMMENT ON COLUMN "city"."city_type" IS 'City type in Japanese' ;
COMMENT ON COLUMN "city"."city_name_level" IS 'Level of city name when it''s split' ;
COMMENT ON COLUMN "city"."city_name_with_space" IS 'City name in Japanese with white space' ;
COMMENT ON COLUMN "city"."city_name_kana" IS 'City name in Japanese Katakana' ;
COMMENT ON COLUMN "city"."city_name_kana_large" IS 'City name in Japanese Katakana with all large characters' ;
COMMENT ON COLUMN "city"."city_name_roman" IS 'City name in Japanese roman representation' ;
