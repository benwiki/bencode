module Dates (
      Month(..),
      toMonth,
      fromMonth,
      Day(..),
      toDay,
      fromDay,
      Year(..),
      toYear,
      fromYear,
      Date(..),
      Weekday,
      leapYear,
      makeMaybeDate,
      correctDate,
      makeDate,
      nextDate ) where

-- Note: this is not a complete implementation for dates.
-- This is just an example giving enough stuff for the Calendar exercise


data Month = Month Integer deriving (Eq, Show, Ord)

toMonth :: Integer -> Month
toMonth x
 | x < 1 = error "Minimum month number is 1"
 | x > 12 = error "Maximum month number is 12"
 | otherwise = Month x

fromMonth :: Month -> Integer
fromMonth (Month i) = i -- Pattern match i out

data Day = Day Integer deriving (Eq, Show, Ord)

toDay :: Integer -> Day
toDay x
 | x < 1 = error "Minimum day number is 1"
 | x > 31 = error "Maximum day number is 31"
 | otherwise = Day x

fromDay :: Day -> Integer
fromDay (Day i) = i

data Year = Year Integer deriving (Eq, Show, Ord, Read)

toYear :: Integer -> Year
toYear x
 | x == 0 = error "No year 0"
 | otherwise = Year x

fromYear :: Year -> Integer
fromYear (Year x) = x

data Date = Date { year :: Year, month :: Month, day :: Day } deriving (Eq, Ord)

data Weekday = Monday | Tuesday | Wednesday | Thursday | Friday | Saturday | Sunday

-- A function to check if a year is a leap year

leapYear (Year y)
 | mod y 400 == 0 = True
 | mod y 100 == 0 = False
 | mod y 4 == 0 = True
 | otherwise = False



makeMaybeDate :: Integer -> Integer -> Integer -> Maybe Date
makeMaybeDate y m d
 | y == 0 = Nothing
 | elem m [1,3,5,7,8,10,12] && d >=1 && d <= 31 = makeJustDate y m d
 | elem m [4,6,9,11] && d >=1 && d <= 30 = makeJustDate y m d
 | m==2 && d >= 1 && d <= 28 = makeJustDate y m d
 | leapYear (toYear y) && m==2 && d==29 = makeJustDate y m d
 | otherwise = Nothing
 where makeJustDate y m d = Just Date {year = toYear y, month = toMonth m, day = toDay d}



-- A function to check if a given date (y,m,d) is correct

correctDate :: Integer -> Integer -> Integer -> Bool
correctDate 0 _ _ = False
correctDate y m d
 | (elem m [1,3,5,7,8,10,12]) && (elem d [1..31]) = True
 | (elem m [4,6,9,11]) && (elem d [1..30]) = True
 | (m==2) && (elem d [1..28]) = True
 | (leapYear (toYear y)) && (m==2) && (d==29) = True
 | otherwise = False


makeDate :: Integer -> Integer -> Integer -> Date
makeDate y m d
 | correctDate y m d = Date { year = toYear y, month = toMonth m, day = toDay d }
 | otherwise = error "not correct combination of integers for year, month and day"


-- As an example, a function that, given a date, calculates the next date

nextDate :: Date -> Date
nextDate date
 | correctDate y m (d+1) = Date { year = year date, month = month date, day = toDay (d+1) }
 | correctDate y (m+1) 1 = Date { year = year date, month = toMonth (m+1), day = toDay 1 }
 | y == (-1) = Date { year = toYear 1, month = toMonth 1, day = toDay 1 }
 | otherwise = Date { year = toYear (y+1), month = toMonth 1, day = toDay 1 }
 where y = fromYear $ year date
       m = fromMonth $ month date
       d = fromDay $ day date

-- Show a date in ISO date format
instance Show Date where
    show x = yyyy ++ "-" ++ mm ++ "-" ++ dd
        where   dd = if d < 10 then "0" ++ show d else show d
                    where d = fromDay $ day x
                mm = if m < 10 then "0" ++ show m else show m
                    where m = fromMonth $ month x
                yyyy = show $ fromYear (year x)
