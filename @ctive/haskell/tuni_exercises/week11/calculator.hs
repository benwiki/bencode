
calculate :: [String] -> [String]
calculate [] = []
calculate (x:xs) = case words x of
    [a, "+", b] -> process a (+) b : calculate xs
    [a, "-", b] -> process a (-) b : calculate xs
    [a, "*", b] -> process a (*) b : calculate xs
    _ -> errorMsg : calculate xs

process a op b = case (readMaybe a, readMaybe b) of
        (Just a, Just b) -> show (a `op` b)
        _ -> errorMsg

readMaybe :: (Read a) => String -> Maybe a
readMaybe str = case reads str of
                    [(x,"")] -> Just x
                    _ -> Nothing

errorMsg = "I cannot calculate that"