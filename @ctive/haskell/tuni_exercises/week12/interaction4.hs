-- A type the describes the state of the program (the sums of given positive and negative values)
data SumState = SumState { possum :: Integer, negsum :: Integer } deriving (Show)

-- Data type describing input commands (and the data for the command in case of IntInput)
data InputEvent = NoCmd | QuitCmd | SumCmd | IntInput Integer
    deriving (Show)

-- Data type describing output events (and the data to output in case of Printout)
data OutputEvent = NoAction | Quit | Printout String deriving (Show)

-- A function that calculates the new program state based on the current state and user input
-- now returns the new state and output event
update :: SumState -> InputEvent -> (SumState, OutputEvent)
update state (IntInput input) | input >= 0 = (state { possum = (possum state) + input }, Printout ("Positive: " ++ show input))
                              | otherwise  = (state { negsum = (negsum state) + input }, Printout ("Negative: " ++ show input))
update state SumCmd = (state, Printout ("sum of positives now: " ++ show (possum state) ++ "\n" ++
                                        "sum of negatives now: " ++ show (negsum state)) )
update state QuitCmd = (state, Quit)
update state NoCmd = (state, NoAction)

-- The state of the program when it starts
initialstate :: SumState
initialstate = SumState { possum = 0, negsum = 0 }

-- Interpreting user input with error recognition
-- returns "Just (interpreted value)" if string can be interpreted as requested type
-- returns "Nothing" otherwise (string couldn't be read as a value of requested type)
readMaybe :: (Read a) => String -> Maybe a
readMaybe st = case reads st of [(x,"")] -> Just x
                                _ -> Nothing

-- Produce input events: read a line from user, handle possible errors and produce
-- an InputEvent describing the input
createInputEvent :: IO InputEvent
createInputEvent = do
    putStrLn "Give an integer, 'sum', or 'quit'"
    line <- getLine
    case line of
            "quit" -> return QuitCmd
            "sum"  -> return SumCmd
            _      -> do -- Everything else should be an integer
                let maybevalue = readMaybe line -- attempt to interpret string as an integer
                case maybevalue of
                    Just value -> return (IntInput value)
                    Nothing -> do
                        putStrLn $ show line ++ " is not an acceptable input"
                        return NoCmd -- Produce "NoCmd" to mark no action on error


-- The (recursive) event loop, with current program state as the parameter
-- read input event, update program state, react on the produced output event, and loop again
-- stop recursion and produce final state on output event "Quit"
eventLoop :: SumState -> IO SumState
eventLoop state =
    do
        inputevent <- createInputEvent
        let (newstate, outputevent) = update state inputevent
        case outputevent of
             Quit -> return state -- quit loop, produce final state
             (Printout outputstr) -> do
                putStrLn outputstr
                eventLoop newstate -- Recurse with new state to create a loop
             _ -> do
                eventLoop newstate -- Recurse with new state to create a loop

main = eventLoop initialstate
