gap :: (Char, Char) -> Int -> String -> Int

gap _ gaplength (_:rest)
    | (gaplength < 0 || length rest <= gaplength)
 = 0

gap (c1, c2) gaplen (first:rest) =
    ( if first == c1 && rest !! gaplen == c2 then 1 else 0 )
    + gap (c1, c2) gaplen rest
