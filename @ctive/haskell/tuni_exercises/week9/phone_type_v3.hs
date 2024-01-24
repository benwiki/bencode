
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
    | countryCodeInt `elem` ccodelist
 = Just $ toCountryCode countryCodeInt
    | otherwise
 = error "Unknown country code"

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