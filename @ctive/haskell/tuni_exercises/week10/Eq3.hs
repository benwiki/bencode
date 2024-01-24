module Eq3 (Eq3((===))) where

import Bool3 (Bool3(..))

class Eq3 a where
  (===) :: a -> a -> Bool3

instance Eq3 Bool3 where
  True3  === True3  = True3
  False3 === False3 = True3
  True3  === False3 = False3
  False3 === True3  = False3
  _      === _      = Unk3

instance (Eq3 a) => Eq3 (Maybe a) where
  Just x  === Just y  = x === y
  Nothing === _       = Unk3
  _       === Nothing = Unk3
