credits :: (Char, Int) -> (Char, Int) -> Int

credits c1 c2
     | c1 == ('s', 14) || c2 == ('s', 14)
 = 14

credits (s1, a) (s2, b)
     | abs (a-b) == 1 && s1 == s2
 = 8

credits (_, a) (_, b)
     | a == b
 = 6

credits (_, a) (_, b)
     | abs (a-b) == 1
 = 4

credits (s1, _) (s2, _)
     | s1 == s2
 = 2

credits a b = 0

-----------------------

intToChar 1 = 'a'
intToChar x = succ $ intToChar $ x-1

charsDivisibleBy :: Int -> [Char]
charsDivisibleBy 0 = []
charsDivisibleBy n = [ intToChar x | x <- [1..26], x `mod` n == 0 ]

unique [] = []
unique (x:xs) = x : filter (x /=) (unique xs)

charsProductOf :: [Int] -> [Char]
charsProductOf nums = unique [ intToChar x | x <- [1..26], a <- nums, b <- nums, a < b && a * b == x ]