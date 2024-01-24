
module Phone_book_tree (
    PhoneBook(..),
    Name,
    addEntry,
    findEntries,
    emptyBook
) where

import Phone_type2 (Phone(..), readPhone)

type Name = String
data PhoneBook =
      Empty
    | Node String [Phone] PhoneBook PhoneBook
    deriving (Show,Eq)

addEntry :: Name -> String -> String -> String -> [Integer] -> PhoneBook -> PhoneBook
addEntry newName phonetype ccode phonenum ccodelist Empty
    = Node newName [newPhone] Empty Empty
    where
    newPhone = readPhone phonetype ccode phonenum ccodelist

addEntry newName phonetype ccode phonenum ccodelist originalNode@(Node name phones left right)
    | newName == name && any (samePhone newPhone) phones
 = originalNode
    | newName == name
 = Node name (newPhone : phones) left right
    | newName < name
 = Node name phones (addEntry newName phonetype ccode phonenum ccodelist left) right
    | otherwise
 = Node name phones left (addEntry newName phonetype ccode phonenum ccodelist right)
    where
    newPhone = readPhone phonetype ccode phonenum ccodelist

samePhone :: Phone -> Phone -> Bool
samePhone (Phone phoneType1 countryCode1 phoneNo1) (Phone phoneType2 countryCode2 phoneNo2) =
    phoneType1 == phoneType2 && countryCode1 == countryCode2 && phoneNo1 == phoneNo2

findEntries :: Name -> PhoneBook -> [Phone]
findEntries _ Empty = []
findEntries query (Node name phones left right)
    | query == name = phones
    | query < name = findEntries query left
    | otherwise = findEntries query right

emptyBook :: PhoneBook
emptyBook = Empty