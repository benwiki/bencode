maxhr :: Float -> Float
maxhr age = if age > 40
    then 207 - 0.7 * age
    else 220 - age

points :: Int -> [(Int, Int)]
points z = [ (x, y) | x <- [-z..z], y <- [-z..z], abs x + abs y <= z ]

headOrLast :: [String] -> Char -> [String]
headOrLast strings char = [ s | s <- strings, not (null s), head s == char || last s == char ]

main = putStrLn(show (headOrLast ["cucc", "gucc", "hucg"] 'g'))