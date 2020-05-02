-- Table definitions on PostgreSQL

-- DROP TABLE city_block;
CREATE TABLE city_block (
    prefecture      VARCHAR(200),
    city            VARCHAR(200),
    town            VARCHAR(200),
    field           VARCHAR(200),
    city_block      VARCHAR(200),
    csnum           SMALLINT,
    csx             DOUBLE PRECISION NOT NULL,
    csy             DOUBLE PRECISION NOT NULL,
    latitude        DOUBLE PRECISION NOT NULL,
    longitude       DOUBLE PRECISION NOT NULL,
    house_display   SMALLINT NOT NULL,
    main_city_block SMALLINT NOT NULL,
    update_before   SMALLINT NOT NULL,
    update_after    SMALLINT NOT NULL
);

COMMENT ON TABLE city_block IS '街区レベル位置情報参照情報';
COMMENT ON COLUMN city_block.prefecture IS '都道府県名';
COMMENT ON COLUMN city_block.city IS '市区町村名 - 郡部は郡名、政令指定都市の区名も含む。';
COMMENT ON COLUMN city_block.town IS '大字・町丁目名 - 町丁目の数字は漢数字';
COMMENT ON COLUMN city_block.field IS '小字・通称名';
COMMENT ON COLUMN city_block.city_block IS '街区符号・地番 - 原則として半角整数（一部漢字等あり）';
COMMENT ON COLUMN city_block.csnum IS '座標系番号 - 平面直角座標系の座標系番号（1～19：半角整数）';
COMMENT ON COLUMN city_block.csx IS 'Ｘ座標';
COMMENT ON COLUMN city_block.csy IS 'Ｙ座標';
COMMENT ON COLUMN city_block.latitude IS '緯度';
COMMENT ON COLUMN city_block.longitude IS '経度';
COMMENT ON COLUMN city_block.house_display IS '住居表示フラグ - 1：住居表示実施、0：住居表示未実施';
COMMENT ON COLUMN city_block.main_city_block IS '代表フラグ - 1つの街区符号が複数の代表点に対応付けられる場合などに、そのうちの1つに便宜的に代表フラグを立てています。1：代表する、0：代表しない';
COMMENT ON COLUMN city_block.update_before IS '更新前履歴フラグ - 2007年度および2008年度データに含まれるフラグを立てています。 1：新規作成、2：名称変更、3：削除、0：変更なし';
COMMENT ON COLUMN city_block.update_after IS '更新後履歴フラグ - 2009年度以降のデータに含まれるフラグを立てています。 1：新規作成、2：名称変更、3：削除、0：変更なし';

-- DROP TABLE town;
CREATE TABLE town (
    prefecture_code   CHAR(2) NOT NULL,
    prefecture        VARCHAR(200) NOT NULL,
    city_code         CHAR(5) NOT NULL,
    city              VARCHAR(200) NOT NULL,
    town_code         CHAR(12) NOT NULL,
    town              VARCHAR(200) NOT NULL,
    latitude          DOUBLE PRECISION NOT NULL,
    longitude         DOUBLE PRECISION NOT NULL,
    original_resource SMALLINT NOT NULL,
    type_code         SMALLINT NOT NULL
);

COMMENT ON TABLE town IS '大字・町丁目レベル位置参照情報';
COMMENT ON COLUMN town.prefecture_code IS '都道府県コード';
COMMENT ON COLUMN town.prefecture IS '都道府県名';
COMMENT ON COLUMN town.city_code IS '市区町村コード';
COMMENT ON COLUMN town.city IS '市区町村名 - （郡部は郡名，政令指定都市の区名も含む）';
COMMENT ON COLUMN town.town_code IS '大字町丁目コード（JIS市区町村コード＋独自7桁）';
COMMENT ON COLUMN town.town IS '大字町丁目名 - （町丁目の数字は漢数字）';
COMMENT ON COLUMN town.latitude IS '緯度';
COMMENT ON COLUMN town.longitude IS '経度';
COMMENT ON COLUMN town.original_resource IS '原典資料コード - 大字・町丁目位置参照情報作成における原典資料を表すコード。1：自治体資料、2：街区レベル位置参照情報、3：1/25000地形図、0：その他資料';
COMMENT ON COLUMN town.type_code IS '大字・字・丁目区分コード - 1：大字、2：字、3：丁目、0：不明（通称）';
