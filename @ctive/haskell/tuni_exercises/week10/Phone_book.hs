
module Phone_book
  ( PhoneBook,
    -- rest of exported stuff
    findEntries,
    addEntry,
    emptyBook
  )
where

import Phone_type2

data PhoneBookEntry = PhoneBookEntry { name :: String, phone :: Phone } deriving (Eq, Show)
type PhoneBook = [PhoneBookEntry]

findEntries :: String -> PhoneBook -> PhoneBook
findEntries searchName phonebook = filter (\entry -> searchName == name entry) phonebook

addEntry :: String -> String -> String -> String -> [Integer] -> PhoneBook -> PhoneBook
addEntry newName phonetype ccode phonenum ccodelist currentbook =
    let newPhone = readPhone phonetype ccode phonenum ccodelist
        entryExists entry = (newName == name entry) && (phoneNo (phone entry) == phoneNo newPhone)
    in if any entryExists currentbook
       then currentbook -- Entry already exists; return the original phone book
       else PhoneBookEntry { name = newName, phone = newPhone } : currentbook

emptyBook :: PhoneBook
emptyBook = []
