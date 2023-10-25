
gap :: (Char, Char) -> Int -> String -> Int

gap _ gaplen (_:rest)
    | (gaplen < 0 || length rest <= gaplen)
 = 0

gap (c1, c2) gaplen (first:rest) =
    ( if first == c1 && rest !! gaplen == c2 then 1 else 0 )
    + gap (c1, c2) gaplen rest

-- Alternative: --
-- gap (c1, c2) gaplen (first:rest)
--     | (gaplen < 0 || length rest <= gaplen)
--  = 0
--     | (first == c1 && rest !! gaplen == c2)
--  = 1 + gap (c1, c2) gaplen rest
--     | otherwise
--  = gap (c1, c2) gaplen rest

distance1 :: String -> String -> Float

distance1 "" "" = 0
distance1 s1 s2 =
   fromIntegral (sum [(if e1 `notElem` s2 then 1 else 0) | e1 <- s1]
                  + sum [(if e2 `notElem` s1 then 1 else 0) | e2 <- s2])
                / fromIntegral (length s1 + length s2)
-- Alternative: --
-- distance1 s1 s2 = fromIntegral (length (filter (`notElem` s2) s1) + length (filter (`notElem` s1) s2)) / fromIntegral (length s1 + length s2)    

distance2 :: String -> String -> Float

distance2 "" "" = 0
distance2 s1 s2 =
   fromIntegral (sum [(if e1 `notElem` ['0'..'9'] then 1 else 0) | e1 <- s1]
                   + sum [(if e2 `notElem` ['0'..'9'] then 1 else 0) | e2 <- s2])
                / fromIntegral (length s1 + length s2)