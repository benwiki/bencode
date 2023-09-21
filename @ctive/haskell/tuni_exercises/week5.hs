gap :: (Char, Char) -> Int -> String -> Int
gap (c1, c2) = gapHelper c1 + gapHelper c2
    where gapHelper _ _ "" _ = 0
          gapHelper c 0 str res = if c == head str then 1 + res else res
          gapHelper char gap (first:rest) =
              if char == first
              then gapHelper char (gap-1) rest
              else 