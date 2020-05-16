--
-- Auto generated at 2020/05/04 13:12:42
--
-- Resources:
--   * prefecture
--   * city

-- DROP TABLE IF EXISTS prefecture ;
CREATE TABLE IF NOT EXISTS prefecture (
  "prefecture_code" CHAR(2) PRIMARY KEY,
  "prefecture_name" VARCHAR(5) NOT NULL,
  "prefecture_type" CHAR(1) NOT NULL CHECK ("prefecture_type" IN ('都', '道', '府', '県')),
  "prefecture_name_kana" VARCHAR(10) NOT NULL,
  "prefecture_name_kana_large" VARCHAR(10) NOT NULL,
  "prefecture_name_roman_full" VARCHAR(15) NOT NULL,
  "prefecture_name_roman" VARCHAR(10) NOT NULL
) ;

COMMENT ON COLUMN "prefecture"."prefecture_code" IS 'Prefecture code with zero-padding two digits.' ;
COMMENT ON COLUMN "prefecture"."prefecture_name" IS 'Prefecture name in Japanese' ;
COMMENT ON COLUMN "prefecture"."prefecture_type" IS 'Prefecture type in Japanese' ;
COMMENT ON COLUMN "prefecture"."prefecture_name_kana" IS 'Prefecture name in Japanese Katakana' ;
COMMENT ON COLUMN "prefecture"."prefecture_name_kana_large" IS 'Prefecture name in Japanese Katakana with all large characters' ;
COMMENT ON COLUMN "prefecture"."prefecture_name_roman_full" IS 'Prefecture name in Japanese roman representation with type suffix' ;
COMMENT ON COLUMN "prefecture"."prefecture_name_roman" IS 'Prefecture name in Japanese roman representation' ;


-- DROP TABLE IF EXISTS city ;
CREATE TABLE IF NOT EXISTS city (
  "prefecture_code" CHAR(2) NOT NULL,
  "prefecture_name" VARCHAR(5) NOT NULL,
  "city_code" CHAR(5) PRIMARY KEY,
  "city_name" VARCHAR(20) NOT NULL,
  "city_type" CHAR(1) NOT NULL CHECK ("city_type" IN ('市', '区', '町', '村')),
  "city_name_level" INTEGER NOT NULL CHECK ("city_name_level" BETWEEN 1 AND 2),
  "city_name_with_space" VARCHAR(20) NOT NULL,
  "city_name_kana" VARCHAR(20) NOT NULL,
  "city_name_kana_large" VARCHAR(20) NOT NULL,
  "city_name_roman" VARCHAR(50) NOT NULL
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
