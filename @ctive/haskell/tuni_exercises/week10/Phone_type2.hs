module Phone_type2
  ( Phone(..),
    PhoneType(..),
    CountryCode(..),
    PhoneNo(..),
    -- rest of exported stuff
    fromPhoneNo,
    toPhoneNo,
    readPhone
  )
where


data CountryCode = CountryCode Integer
  deriving (Show, Eq)

data PhoneNo = PhoneNo Integer
  deriving (Show, Eq)

data PhoneType = WorkLandline | PrivateMobile | WorkMobile | Other
  deriving (Show, Eq, Read)


data Phone = Phone
  { phoneType :: PhoneType
  , countryCode :: CountryCode
  , phoneNo :: PhoneNo
  }
  deriving (Show, Eq)

toCountryCode :: Integer -> CountryCode
toCountryCode cc
  | cc < 0 = error "Negative country code"
  | otherwise = CountryCode cc

toPhoneNo :: Integer -> PhoneNo
toPhoneNo pn
  | pn < 0 = error "Negative phone number"
  | otherwise = PhoneNo pn

stripPrefix' :: String -> String -> Maybe String
stripPrefix' [] str = Just str
stripPrefix' _ [] = Nothing
stripPrefix' (x:xs) (y:ys)
  | x == y = stripPrefix' xs ys
  | otherwise = Nothing

readPhone :: String -> String -> String -> [Integer] -> Phone
readPhone phonetypestr countrycodestr phonenostr ccodelist =
  let phoneType = case phonetypestr of
                    "WorkLandline" -> WorkLandline
                    "PrivateMobile" -> PrivateMobile
                    "WorkMobile" -> WorkMobile
                    "Other" -> Other
                    "" -> error "Missing phone type"
                    _ -> error "Incorrect phone type"

      cleanedCountryCode = case stripPrefix' "00" countrycodestr of
                            Just rest -> rest
                            Nothing -> case stripPrefix' "+" countrycodestr of
                                        Just rest -> rest
                                        Nothing -> countrycodestr
      countryCodeInt = case reads cleanedCountryCode of
                        [(cc, "")] -> cc
                        _ -> error "Incorrect country code"
      countryCode = if countryCodeInt `elem` ccodelist
                    then toCountryCode countryCodeInt
                    else error "Unknown country code"
      phoneNoInt = case reads phonenostr of
                    [(pn, "")] -> pn
                    _ -> error "Incorrect phone number"
  in Phone { phoneType = phoneType, countryCode = countryCode, phoneNo = toPhoneNo phoneNoInt }

fromPhoneNo :: PhoneNo -> Integer
fromPhoneNo (PhoneNo pn) = pn

