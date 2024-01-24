import qualified Data.Map.Strict as Map
import Data.Char (isAlphaNum)
import Data.Maybe (fromMaybe)

encode :: Int -> String -> String
encode shift = map (charmap Map.!)
  where charlist = ['0'..'9'] ++ ['A'..'Z'] ++ ['a'..'z']
        listlength = length charlist
        shiftedlist = take listlength . drop (shift `mod` listlength) . cycle $ charlist
        charmap = Map.fromList $ zip charlist shiftedlist

decode :: Int -> String -> String
decode shift = encode (negate shift)

readMaybe :: Read a => String -> Maybe a
readMaybe st = case reads st of [(x, "")] -> Just x
                                _ -> Nothing

data InputEvent = InvalidCmd String | QuitCmd | ValidCmd String Int String
    deriving Show

data OutputEvent = PrintError String | Quit | PrintStr String
    deriving Show

update :: InputEvent -> OutputEvent
update (InvalidCmd str) = PrintError str
update QuitCmd = Quit
update (ValidCmd code num text) =
    let action = if code == "encode" then encode else decode
        command = unwords [code, show num, text]
        result = unwords $ map (action num) (words text)
    in PrintStr (command ++ "\n" ++ result)

interpretString :: [String] -> Maybe InputEvent
interpretString ("quit":_) = Just QuitCmd
interpretString (code:num:text)
  | code `elem` ["encode", "decode"], Just n <- readMaybe num =
      Just $ ValidCmd code n (unwords text)
interpretString _ = Nothing

createInputEvent :: String -> InputEvent
createInputEvent line = fromMaybe (InvalidCmd line) (interpretString (words line))

eventLoop :: IO ()
eventLoop = do
    line <- getLine
    let inputevent = createInputEvent line
        outputevent = update inputevent
    case outputevent of
        Quit -> putStrLn "> quit\nbye"
        PrintStr command -> do
            putStrLn $ "> " ++ command
            eventLoop
        PrintError str -> do
            putStrLn $ "> " ++ str
            putStrLn "I cannot do that"
            eventLoop

main :: IO ()
main = eventLoop
