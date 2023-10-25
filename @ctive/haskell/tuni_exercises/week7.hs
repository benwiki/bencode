
clusters :: (String -> String -> Float) -> Float -> [String] -> [[String]]
clusters f d ss = map (\s -> filter (\x -> f x s <= d) ss) ss


{- Task:
Write a function commonSubstring :: String -> String -> String that, given two strings s1 and s2, computes a common “substring” of s1 and s2 as follows. The function finds the earliest common character c (a character closest to the head of either s1 or s2, and appearing in both sequences). The function removes c and all the characters before it in both strings, puts c in the output string, and continues.
If there are two candidates for the earliest common character, pick the one from s1.
For example:
commonSubstring "XabcdefgY" "abcdefgXY" produces "XY"
commonSubstring "abcdefgXY" "XabcdefgY" produces "abcdefgY"
Please note that the result is not what is normally meant by substring.
-}
commonSubstring :: String -> String -> String
commonSubstring _ "" = ""
commonSubstring "" _ = ""
commonSubstring s1 s2
    | head s1 `elem` s2
 = head s1 : commonSubstring (tail s1) (tail (dropWhile (/= head s1) s2))
    | head s2 `elem` s1
 = head s2 : commonSubstring (tail (dropWhile (/= head s2) s1)) (tail s2)
    | otherwise
 = commonSubstring (tail s1) (tail s2)


-- Alternative:
------------------------------------------------------------------------
-- commonSubstring :: String -> String -> String
-- commonSubstring _ "" = ""
-- commonSubstring "" _ = ""
-- commonSubstring (x:xs) s2
--     | x `elem` s2 = x : commonSubstring xs (tail (dropWhile (/= x) s2))
--     | otherwise = commonSubstring xs s2
