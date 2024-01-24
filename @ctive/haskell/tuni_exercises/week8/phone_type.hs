type CountryCode = Integer

type PhoneNo = Integer

data PhoneType = WorkLandline | PrivateMobile | WorkMobile | Other
  deriving (Show, Eq, Read)

data Phone = Phone
  { phoneType :: PhoneType
  , countryCode :: CountryCode
  , phoneNo :: PhoneNo
  }
  deriving (Show, Eq)

makePhone :: PhoneType -> CountryCode  -> PhoneNo -> Phone
makePhone pt cc pn
    | cc < 0
 = error "Negative country code"
    | pn < 0
 = error "Negative phone number"
    | otherwise
 = Phone pt cc pn