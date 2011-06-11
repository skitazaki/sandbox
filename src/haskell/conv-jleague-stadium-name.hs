import qualified System.IO.UTF8 as U

main = do cs <- U.getContents
          U.putStr $ unlines $ parse $ lines cs

parse :: [String] -> [String]
parse ss = map replace ss

replace :: String -> String
replace cs = join $ map rewrite $ split cs

split :: String -> [String]
split cs = words $ map csv2tsv cs
  where
    csv2tsv :: Char -> Char
    csv2tsv ',' = '\t'
    csv2tsv c = c

join :: [String] -> String
join ss = map space2csv $ unwords ss
  where
    space2csv :: Char -> Char
    space2csv ' ' = ','
    space2csv c = c

rewrite :: String -> String
rewrite "味スタ" = "味の素スタジアム"
rewrite "駒沢" = "駒沢陸上競技場"
rewrite "国立" = "国立競技場"
rewrite "ニンスタ" = "ニンジニアスタジアム"
rewrite "Ｋｓスタ" = "ケーズデンキスタジアム水戸"
rewrite "栃木SCグ" = "栃木県グリーンスタジアム"
rewrite "平塚" = "平塚競技場"
rewrite "本城" = "北九州市立本城陸上競技場"
rewrite "鳴門大塚" = "鳴門･大塚スポーツパークポカリスエットスタジアム"
rewrite "ニッパ球" = "ニッパツ三ツ沢球技場"
rewrite "長良川" = "岐阜メモリアルセンター長良川競技場"
rewrite "カンスタ" = "kankoスタジアム"
rewrite "ベアスタ" = "ベストアメニティスタジアム"
rewrite "正田スタ" = "正田醤油スタジアム群馬"
rewrite "西京極" = "京都市西京極総合運動公園陸上競技場兼球技場"
rewrite "とりスタ" = "とりぎんバードスタジアム"
rewrite "大銀ド" = "大分銀行ドーム"
rewrite "コンサドーレ札幌ド" = "札幌ドーム"
rewrite "フクアリ" = "フクダ電子アリーナ"
rewrite "_ロアッソ熊本" = "熊本県民総合運動公園陸上競技場 (KKWING)"
rewrite "_カターレ富山" = "富山県総合運動公園陸上競技場"
rewrite cs = cs

