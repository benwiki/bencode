nextIsGreater :: [Int] -> [Int]
nextIsGreater [] = []
nextIsGreater [_] = []
nextIsGreater (first:rest) =
    if head rest > first
    then first : nextIsGreater rest
    else nextIsGreater rest
-- nextIsGreater ls = nextIsGreaterHelper ls []
    -- where nextIsGreaterHelper [] res = res
          -- nextIsGreaterHelper [_] res = res
          -- nextIsGreaterHelper (first:rest) res =
              -- nextIsGreaterHelper rest (if head rest > first
                  -- then first : res else res)

isDigit c = c `elem` "1234567890"

onlyDigits :: String -> Bool
onlyDigits "" = False
onlyDigits ls = all isDigit ls
