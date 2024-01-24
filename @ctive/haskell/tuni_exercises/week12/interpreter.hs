import qualified Data.Map

encode :: Int -> String -> String
encode shift = map (charmap Data.Map.!)
  where charlist = ['0'..'9'] ++ ['A'..'Z'] ++ ['a'..'z']
        listlength = length charlist
        shiftedlist = take listlength (drop (shift `mod` listlength) (cycle charlist))
        charmap = Data.Map.fromList $ zip charlist shiftedlist

decode :: Int -> String -> String
decode shift = encode (negate shift)

readMaybe :: (Read a) => String -> Maybe a
readMaybe st = case reads st of [(x,"")] -> Just x
                                _ -> Nothing

data InputEvent = InvalidCmd String | QuitCmd | ValidCmd String Int String
    deriving (Show)

data OutputEvent = PrintError String | Quit | PrintStr String
    deriving (Show)


update :: InputEvent -> OutputEvent
update (InvalidCmd str) = PrintError str
update QuitCmd = Quit
update (ValidCmd code num text) = 
    let command = "> " ++ unwords [code, show num, text]
    in case code of
    "encode" -> PrintStr (command ++ "\n" ++ (unwords $ map (encode num) (words text)))
    "decode" -> PrintStr (command ++ "\n" ++ (unwords $ map (decode num) (words text)))

processMaybe :: String -> Maybe InputEvent
processMaybe str = interpretString (words str)

interpretString [] = Nothing
interpretString [x] = Nothing
interpretString [x, y] = Nothing
interpretString (code:num:rest) = case code of
    "encode" -> interpret2 code (readMaybe num) (unwords rest)
    "decode" -> interpret2 code (readMaybe num) (unwords rest)
    _        -> Nothing

interpret2 code maybeNum rest = case maybeNum of
    Just n -> Just $ ValidCmd code n rest
    _      -> Nothing

createInputEvent :: IO InputEvent
createInputEvent = do
    line <- getLine
    case line of
            "quit" -> return QuitCmd
            _      -> do -- Everything else should be an integer
                let maybevalue = processMaybe line -- attempt to interpret string as an integer
                case maybevalue of
                    Just value -> return value
                    Nothing -> return (InvalidCmd line) -- Produce "NoCmd" to mark no action on error


eventLoop :: IO ()
eventLoop = do
    inputevent <- createInputEvent
    let outputevent = update inputevent
    case outputevent of
         Quit -> do
            putStrLn "> quit\nbye" -- quit loop
         (PrintStr str) -> do
            -- putStrLn $ "> " ++ command
            putStrLn str
            eventLoop -- Recurse to create a loop
         (PrintError str) -> do
            putStrLn $ "> " ++ str
            putStrLn "I cannot do that"
            eventLoop -- Recurse to create a loop

main = eventLoop