-- This example goes further than the video, and allows testing of IO by producing a list
-- of output events, which can be compared to expected output

-- A type the describes the state of the program (the sums of given positive and negative values)
data SumState = SumState { possum :: Integer, negsum :: Integer } deriving (Show)

-- Data type describing input commands (and the data for the command in case of IntInput)
data InputEvent = NoCmd | QuitCmd | SumCmd | IntInput Integer deriving (Show)

-- Data type describing output events (and the data to output in case of Printout)
-- now also derives Eq for comparing output events
data OutputEvent = NoAction | Quit | Printout String deriving (Show, Eq)

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

-- The (recursive) event loop, with current program state, a list of output events so far,
-- and a list of IO actions producing input events as parameters
-- read input event from IO action, update program state, react on the produced output event,
-- and loop again, adding the produced output event to the list of output events
-- stop recursion and produce the final list of output events on output event "Quit"
eventLoop :: SumState -> [OutputEvent] -> [IO InputEvent] -> IO [OutputEvent]
eventLoop _ outputlist [] = return outputlist -- No more events, stop recursion
eventLoop state outputlist (ioinputevent:restevents) =
    do
        inputevent <- ioinputevent
        let (newstate, outputevent) = update state inputevent
        let newoutputlist = outputlist ++ [outputevent]
        case outputevent of
             Quit -> return newoutputlist -- quit loop, produce final list of output events
             Printout outputstr -> do
                putStrLn outputstr
                eventLoop newstate newoutputlist restevents -- Recurse with new state + output and rest of events
             _ -> eventLoop newstate newoutputlist restevents -- Recurse with new state + output and rest of events

-- The main program creates a potentially *infinite* list of input events using createInputEvent
main = eventLoop initialstate [] $ repeat createInputEvent

-- Run the program with simulated fake IO actions producing predetermined input
testmain1 = eventLoop initialstate [] [return (IntInput 3), return (IntInput 5), return (SumCmd), return (QuitCmd)]

-- Run the program with simulated fake IO actions producing predetermined input,
-- check that the produced list of output events is what was expected
testmain2 = do
    let inputevents = [IntInput 3, SumCmd, QuitCmd]
    let expectedoutput = [Printout "Positive: 3",Printout "sum of positives now: 3\nsum of negatives now: 0",Quit]
    let ioinputevents = map return inputevents -- run inputevents through return to get fake IO actions
    outputevents <- eventLoop initialstate [] ioinputevents -- run the event loop
    putStrLn "Program finished."
    if outputevents == expectedoutput
       then putStrLn "Output matched with expected output"
       else putStrLn $ "Got output: " ++ show outputevents ++ ", expected " ++ show expectedoutput
