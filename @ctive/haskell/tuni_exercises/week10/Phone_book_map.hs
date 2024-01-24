
module Phone_book_map
  ( PhoneBook,
    Name,
    -- rest of exported stuff
    findEntries,
    addEntry,
    emptyBook
  )
where
import Phone_type2
import qualified Data.Map as Map
type Name = String
type PhoneBook = Map.Map Name [Phone]

-- findEntries :: String -> PhoneBook -> PhoneBook
-- findEntries searchName phonebook = filter (\entry -> searchName == name entry) phonebook
findEntries :: Name -> PhoneBook -> [Phone]
-- findEntries searchName phonebook = 
    -- Map.elems $ Map.filterWithKey (\key _ -> key == searchName) phonebook
findEntries query book = concat [phoneNumber | (name, phoneNumber) <- Map.toList book, name == query]
-- findEntries :: Name -> PhoneBook -> [Phone]
-- findEntries name phonebook = 
--     let phoneBookMap = findEntries name phonebook
--     in concat $ Map.elems phoneBookMap


-- addEntry :: String -> String -> String -> String -> [Integer] -> PhoneBook -> PhoneBook
-- addEntry newName phonetype ccode phonenum ccodelist currentbook =
--     let newPhone = readPhone phonetype ccode phonenum ccodelist
--         entryExists entry = (newName == name entry) && (phoneNo (phone entry) == phoneNo newPhone)
--     in if any entryExists currentbook
--        then currentbook -- Entry already exists; return the original phone book
--        else PhoneBookEntry { name = newName, phone = newPhone } : currentbook

-- addEntry :: Name -> String -> String -> String -> [Integer] -> PhoneBook -> PhoneBook
-- addEntry newName phonetype ccode phonenum ccodelist currentbook =
--     let newPhone = readPhone phonetype ccode phonenum ccodelist
--         entryExists entry = (newName == name entry) && (phoneNo (phone entry) == phoneNo newPhone)
--     in if any entryExists currentbook
--        then currentbook -- Entry already exists; return the original phone book
--        else Map.insertWith (++) newName [newPhone] currentbook

-- addEntry :: Name -> String -> String -> String -> [Integer] -> PhoneBook -> PhoneBook
-- addEntry newName phonetype ccode phonenum ccodelist currentbook =
--     let newPhone = readPhone phonetype ccode phonenum ccodelist
--     in Map.insertWith (++) newName [newPhone] currentbook

addEntry :: String -> String -> String -> String -> [Integer] -> PhoneBook -> PhoneBook
addEntry newName phonetype ccode phonenum ccodelist currentbook =
    let newPhone = readPhone phonetype ccode phonenum ccodelist
    in case Map.lookup newName currentbook of
        Just existingPhones -> if not (any (samePhone newPhone) existingPhones)
                               then Map.insert newName (newPhone : existingPhones) currentbook
                               else currentbook
        Nothing             -> Map.insert newName [newPhone] currentbook

emptyBook :: PhoneBook
emptyBook = Map.empty

samePhone :: Phone -> Phone -> Bool
samePhone (Phone phoneType1 countryCode1 phoneNo1) (Phone phoneType2 countryCode2 phoneNo2) =
    phoneType1 == phoneType2 && countryCode1 == countryCode2 && phoneNo1 == phoneNo2

