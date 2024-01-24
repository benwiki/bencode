
newtype CountryCode = CountryCode Integer
    deriving (Eq)

instance Show CountryCode where
    show (CountryCode cc) = "+" ++ show cc

toCountryCode :: Integer -> CountryCode
toCountryCode cc
    | cc < 0
 = error "Negative country code"
    | otherwise
 = CountryCode cc

newtype PhoneNo = PhoneNo Integer
    deriving (Eq)

instance Show PhoneNo where
    show (PhoneNo pn) = show pn 

toPhoneNo :: Integer -> PhoneNo
toPhoneNo pn
    | pn < 0
 = error "Negative phone number"
    | otherwise
 = PhoneNo pn

data PhoneType = WorkLandline | PrivateMobile | WorkMobile | Other
  deriving (Show, Eq, Read, Enum)

data Phone = Phone
  { phoneType :: Maybe PhoneType
  , countryCode :: Maybe CountryCode
  , phoneNo :: PhoneNo
  }
  deriving (Eq)

instance Show Phone where
    show (Phone Nothing Nothing pn) = show pn
    show (Phone Nothing (Just cc) pn) = show cc ++ " " ++ show pn
    show (Phone (Just pt) Nothing pn) = show pn ++ " (" ++ show pt ++ ")"
    show (Phone (Just pt) (Just cc) pn) = show cc ++ " " ++ show pn ++ " (" ++ show pt ++ ")"

fromPhoneNo :: PhoneNo -> Integer
fromPhoneNo (PhoneNo pn) = pn

readPhoneType :: String -> Maybe PhoneType
readPhoneType str
    | str `elem` map show [WorkLandline .. Other]
 = Just $ read str
    | otherwise
 = Nothing

readCountryCode :: String -> [Integer] -> Maybe CountryCode
readCountryCode str ccodelist
    | null str
 = Nothing
    -- | countryCodeInt `elem` ccodelist
    | otherwise
 = Just $ toCountryCode countryCodeInt
--  = error "Unknown country code"

 where countryCodeInt = case reads cleanedCountryCode of
            [(cc, "")] -> cc
            _ -> error "Incorrect country code"

       cleanedCountryCode | Just rest <- removePrefix "00" str
        = rest
                          | Just rest <- removePrefix "+" str
        = rest
                          | otherwise
        = str

       removePrefix "" str = Just str
       removePrefix _ "" = Nothing
       removePrefix (x:xs) (y:ys)
        | x == y = removePrefix xs ys
        | otherwise = Nothing

readPhoneNo :: String -> PhoneNo
readPhoneNo str
    | [(pn, "")] <- reads str
 = toPhoneNo pn
    | otherwise
 = error "Incorrect phone number"

readPhone :: String -> String -> String -> [Integer] -> Phone
readPhone phonetypestr countrycodestr phonenostr ccodelist =
   Phone { phoneType = readPhoneType phonetypestr
         , countryCode = readCountryCode countrycodestr ccodelist
         , phoneNo = readPhoneNo phonenostr
         }

data PhoneBookEntry = PhoneBookEntry { name :: String, phone :: Phone } deriving (Eq)

instance Show PhoneBookEntry where
    show (PhoneBookEntry name phone) = show phone

type PhoneBook = [PhoneBookEntry]

findEntries :: String -> PhoneBook -> PhoneBook
findEntries searchName = filter (\entry -> searchName == name entry)

addEntry :: String -> String -> String -> String -> [Integer] -> PhoneBook -> PhoneBook
addEntry newName phonetype ccode phonenum ccodelist currentbook =
    let newPhone = readPhone phonetype ccode phonenum ccodelist
        entryExists entry = (newName == name entry) && (phoneNo (phone entry) == phoneNo newPhone)
    in if any entryExists currentbook
       then currentbook -- Entry already exists; return the original phone book
       else PhoneBookEntry { name = newName, phone = newPhone } : currentbook

emptyBook :: PhoneBook
emptyBook = []

data InputEvent = InvalidCmd String | QuitCmd | AddCmd String String String String | FindCmd String
    deriving (Show)


data OutputEvent = PrintError String | Quit | PrintStr String
    deriving (Show)

processMaybe :: String -> Maybe InputEvent
processMaybe str = interpretString (words str)

-- interpretString ("add":name:phone_type:country_code:phone_no) = Just $ AddCmd name phone_type country_code phone_no
-- interpretString ("find":name:[""]) = Just $ FindCmd name
interpretString :: [String] -> Maybe InputEvent
interpretString lst
    | length lst == 5 && head lst == "add" = Just $ AddCmd (lst !! 1) (lst !! 2) (lst !! 3) (lst !! 4)
    | length lst == 2 && head lst == "find" = Just $ FindCmd (lst !! 1)
    | otherwise = Nothing

createInputEvent :: IO InputEvent
createInputEvent = do
    line <- getLine
    case line of
            "quit" -> return QuitCmd
          
            _      -> do -- Everything else should be an integer
                let maybevalue = processMaybe line -- attempt to interpret string as an integer
                case maybevalue of
                    Just value -> return value
                    Nothing -> do
                        --putStrLn $ show line ++ " is not an acceptable input"
                        return $ InvalidCmd line -- Produce "InvalidCmd" to mark no action on error


update :: PhoneBook -> InputEvent -> (PhoneBook, OutputEvent)
update state (InvalidCmd str) = 
    let command = "> " ++ str
        prResult = command ++ "\nCannot do that"
        in (state, PrintStr prResult)
update state QuitCmd = (state, Quit)
update state (AddCmd name phone_type country_code phone_no) = 
    let command = "> add " ++ unwords [name,phone_type, country_code, phone_no]
        prResult = command ++ "\nDone"
        in (addEntry name phone_type country_code phone_no [] state, PrintStr prResult)
update state (FindCmd name) = 
    let command = "> find " ++ name
        prResult = command ++ "\n" ++ show (findEntries name state)
        in (state, PrintStr prResult)


eventLoop :: PhoneBook -> IO PhoneBook
eventLoop state = do

    inputevent <- createInputEvent
    let (newstate, outputevent) = update state inputevent
    case outputevent of
        Quit -> do
            putStrLn "> quit\nbye" -- quit loop
            return state
        (PrintStr str) -> do
            putStrLn str
            eventLoop newstate
        

main = do
  putStrLn "Welcome to phone book application"
  eventLoop emptyBook
