
newtype CountryCode = CountryCode Integer
    deriving (Show, Eq)

toCountryCode :: Integer -> CountryCode
toCountryCode cc
    | cc < 0
 = error "Negative country code"
    | otherwise
 = CountryCode cc

newtype PhoneNo = PhoneNo Integer
    deriving (Show, Eq)

toPhoneNo :: Integer -> PhoneNo
toPhoneNo pn
    | pn < 0
 = error "Negative phone number"
    | otherwise
 = PhoneNo pn

data PhoneType = WorkLandline | PrivateMobile | WorkMobile | Other
  deriving (Show, Eq, Read, Enum)

data Phone = Phone
  { phoneType :: PhoneType
  , countryCode :: CountryCode
  , phoneNo :: PhoneNo
  }
  deriving (Show, Eq)

readPhone :: String -> String -> String -> [Integer] -> Phone
readPhone phonetypestr countrycodestr phonenostr ccodelist =
   Phone { phoneType = phoneType, countryCode = countryCode, phoneNo = toPhoneNo phoneNoInt }

 where phoneType | phonetypestr `elem` map show [WorkLandline .. Other]
        = read phonetypestr
                 | phonetypestr == ""
        = error "Missing phone type"
                 | otherwise
        = error "Incorrect phone type"

       countryCode | countryCodeInt `elem` ccodelist
        = toCountryCode countryCodeInt
                   | otherwise
        = error "Unknown country code"

       countryCodeInt | cleanedCountryCode == ""
        = error "Missing country code"
                      | otherwise
        = case reads cleanedCountryCode of
            [(cc, "")] -> cc
            _ -> error "Incorrect country code"

       cleanedCountryCode | Just rest <- removePrefix "00" countrycodestr
        = rest
                          | Just rest <- removePrefix "+" countrycodestr
        = rest
                          | otherwise
        = countrycodestr

       removePrefix "" str = Just str
       removePrefix _ "" = Nothing
       removePrefix (x:xs) (y:ys)
        | x == y = removePrefix xs ys
        | otherwise = Nothing

       phoneNoInt | [(pn, "")] <- reads phonenostr
        = pn
                  | otherwise
        = error "Incorrect phone number"

data PhoneBookEntry = PhoneBookEntry { name :: String , phone :: Phone } deriving (Eq, Show)
type PhoneBook = [PhoneBookEntry]

findEntries :: String -> PhoneBook -> PhoneBook
findEntries findName = filter (\entry -> findName == name entry)

addEntry :: String -> String -> String -> String -> [Integer] -> PhoneBook -> PhoneBook
addEntry findName pt cc pn ccs originalBook
    | any entryExists originalBook
 = originalBook
    | otherwise
 = newEntry : originalBook
 where entryExists entry = (findName == name entry) && (phoneNo (phone entry) == phoneNo (phone newEntry))
       newEntry = PhoneBookEntry { name = findName, phone = readPhone pt cc pn ccs }

emptyBook :: PhoneBook
emptyBook = []