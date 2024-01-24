import qualified Data.Map as Map
import Dates

data InputEvent =
      QuitCmd
    | AddEvent String String Date
    | SearchEventByName String
    | SearchEventsByDate Date
    | SearchEventsByPlace String
    | ExceptionCmd String
    | InvalidCmd

data OutputEvent =
      Quit
    | PrintError
    | PrintStr String
    | PrintStrList [String]

data Event = Event { name :: String, place :: String, date :: Date }
    deriving (Eq, Ord)

type EventState = [Event]

printError = do
    putStrLn "I do not understand that. I understand the following:"
    putStrLn "*Event <name> happens at <place> on <date>"
    putStrLn "*Tell me about <eventname>"
    putStrLn "*What happens on <date>"
    putStrLn "*What happens at <place>"
    putStrLn "*Quit"

-- What happens on '2019-10-08'

toIntegerList :: String -> [Integer]
toIntegerList str = map read $ words $ map (\x -> if x == '-' then ' ' else x) str

toDateIntermediate :: [Integer] -> Maybe Date
toDateIntermediate [y, m, d] = makeMaybeDate y m d

toDate :: String -> Maybe Date
toDate str = toDateIntermediate $ toIntegerList str

isValidDate :: String -> Bool
isValidDate str = case toDate str of
    Just date -> True
    Nothing -> False

split sep str = case dropWhile (== sep) str of
    "" -> []
    s' -> w : split sep s''
        where (w, s'') = break (== sep) s'

-- Example event:
-- Event 'Event A' happens at 'Place A1' on '2001-02-02'

createInputEvent str = case split '\'' str of
    ["Event ", name, " happens at ", place, " on ", date] -> maybe (ExceptionCmd "Bad date") (AddEvent name place) (toDate date)
    ["Tell me about ", event] -> SearchEventByName event
    ["What happens on ", date] -> maybe (ExceptionCmd "Bad date") SearchEventsByDate (toDate date)
    ["What happens at ", place] -> SearchEventsByPlace place
    ["Quit"] -> QuitCmd
    _ -> InvalidCmd


addOrUpdateEvent :: Event -> EventState -> EventState
addOrUpdateEvent newEvent [] = [newEvent]
addOrUpdateEvent newEvent (e:events)
    | name newEvent == name e = newEvent : events
    | otherwise               = e : addOrUpdateEvent newEvent events

update :: EventState -> InputEvent -> (EventState, OutputEvent)
update state input = case input of
    QuitCmd -> (state, Quit)
    AddEvent name place date -> (addOrUpdateEvent (Event name place date) state, PrintStr "Ok")
    SearchEventByName name -> case events of
        [] -> (state, PrintStr "I do not know of such event")
        _ -> let event = head events in
              (state, PrintStr $ "Event " ++ name ++ " happens at " ++ place event ++ " on " ++ show (date event))
        where events = searchEventsByName name state
    SearchEventsByDate date -> case events of
        [] -> (state, PrintStr "Nothing that I know of")
        _ -> (state, PrintStrList $ map (\event -> "Event " ++ name event ++ " happens on " ++ show date) events)
        where events = searchEventsByDate date state
    SearchEventsByPlace place -> case events of
        [] -> (state, PrintStr "Nothing that I know of")
        _ -> (state, PrintStrList $ map (\event -> "Event " ++ name event ++ " happens at " ++ place) events)
        where events = searchEventsByPlace place state
    ExceptionCmd str -> (state, PrintStr str)
    InvalidCmd -> (state, PrintError)

-- find f lst = head $ filter f lst

searchEventsByName :: String -> EventState -> [Event]
searchEventsByName searchName = filter (\x -> name x == searchName)

searchEventsByDate :: Date -> EventState -> [Event]
searchEventsByDate searchDate = filter (\x -> date x == searchDate)

searchEventsByPlace :: String -> EventState -> [Event]
searchEventsByPlace searchPlace = filter (\x -> place x == searchPlace)

eventLoop :: EventState -> IO ()
eventLoop state = do
    line <- getLine
    putStrLn $ "> " ++ line
    let inputevent = createInputEvent line
        (newstate, outputevent) = update state inputevent
    case outputevent of
        Quit -> putStrLn "Bye"
        PrintStr str -> do
            putStrLn str
            eventLoop newstate
        PrintStrList strlist -> do
            mapM_ putStrLn strlist
            eventLoop newstate
        PrintError -> do
            printError
            eventLoop newstate

main :: IO ()
main = eventLoop []
