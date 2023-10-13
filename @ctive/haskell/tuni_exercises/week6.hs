validate :: String -> Bool

validate str = length str == 18
            && slice 0 1 str == "FI"
            && all digit (slice 2 17 str)
            && read (toDigitString (slice 4 17 str ++ slice 0 3 str)) `mod` 97 == 1

slice from to xs = take (to - from + 1) (drop from xs)

digit c = c `elem` ['0'..'9']

letterToNum :: Char -> Int
letterToNum c = fromEnum c - fromEnum 'A' + 10
toDigits :: [Char] -> [Int]
toDigits = map (\c -> (if not (digit c) then letterToNum c else read [c]) :: Int)
listOfNumsToStr :: [Int] -> String
listOfNumsToStr = concatMap show
toDigitString :: String -> String
toDigitString = listOfNumsToStr . toDigits

----------------------------

distance3 :: String -> String -> Float
distance3 x y = fromIntegral $ abs $ length x - length y

distanceFilter :: (String -> String -> Float) -> Float -> String -> [String] -> [String]
distanceFilter f d s = filter (\y -> f s y <= d)

convertToNum :: String -> Int
convertToNum (x:[]) = fromEnum (x) -48
convertToNum xs = (fromEnum (last xs)-48) + 10 * convertToNum(init xs) 
