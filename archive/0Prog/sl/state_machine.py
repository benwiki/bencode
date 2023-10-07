from enum import Enum, auto
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Iterable
from dataclasses import dataclass


class Statea(Enum):
    INIT = auto()
    oneacc = auto()
    LIGHT_ON = auto()
    lightacc = auto()
    lighttap = auto()
    onetap = auto()
    SCREEN_ON = auto()
    screentap = auto()
    screenacc = auto()
    SCREEN_LIGHT_ON = auto()
    onontap = auto()
    ononacc = auto()


def MyState():
    state = Statea.INIT
    while True:
        state = next_state(state, input())


def next_state(state: Statea, input: str) -> Statea:
    match (state, input):

        case (state.INIT, "SENS_ACC"): return state.oneacc
        case (state.oneacc, "SENS_ACC"): return state.LIGHT_ON
        case (state.LIGHT_ON, "SENS_ACC"): return state.lightacc
        case (state.lightacc, "SENS_ACC"): return state.INIT

        case (state.INIT, "SENS_TAP"): return state.onetap
        case (state.onetap, "SENS_TAP"): return state.SCREEN_ON
        case (state.SCREEN_ON, "SENS_TAP"): return state.screentap
        case (state.screentap, "SENS_TAP"): return state.INIT

        case (state.LIGHT_ON, "SENS_TAP"): return state.lighttap
        case (state.lighttap, "SENS_TAP"): return state.SCREEN_LIGHT_ON
        case (state.SCREEN_ON, "SENS_ACC"): return state.screenacc
        case (state.screenacc, "SENS_ACC"): return state.SCREEN_LIGHT_ON

        case (state.SCREEN_LIGHT_ON, "SENS_TAP"): return state.onontap
        case (state.SCREEN_LIGHT_ON, "SENS_TAP"): return next_state(state.SCREEN_ON, "going off")
        case (state.SCREEN_LIGHT_ON, "SENS_ACC"): return state.ononacc
        case (state.SCREEN_LIGHT_ON, "SENS_ACC"): return next_state(state.SCREEN_ON, "going off")
        case (state.SCREEN_ON, "going off"): return state.INIT
    return state


S = Statea
INP = TypeVar('INP')
OUT = TypeVar('OUT')


@dataclass
class State(Generic[INP, OUT], ABC):
    def next(self, input: INP) -> 'State':
        return self

    @abstractmethod
    def output(self) -> OUT:
        ...


class S_Init(State[INP, OUT]):
    def next(self, input: INP) -> State:
        if input == "SENS_ACC":
            return S_After(["SENS_ACC"])
        elif input == "SENS_ACCSENS_ACC":
            return S_Light_On()
        elif input == "SENS_TAP":
            return S_After(["SENS_TAP"])
        elif input == "SENS_TAPSENS_TAP":
            return S_Screen_On()
        return self


@dataclass
class S_After(State[INP, OUT]):
    prefix: list[INP]

    def next(self, input: INP) -> State:
        self.prefix.append(input)
        if self.prefix == ["SENS_ACC", "SENS_ACC"]:
            return S_Light_On()
        elif self.prefix == ["SENS_TAP", "SENS_TAP"]:
            return S_Screen_On()
        elif self.prefix[-2:] == ["SENS_ACC", "SENS_ACC"] and "SENS_TAP" in self.prefix:
            return S_Screen_Light_On()
        elif self.prefix[-2:] == ["SENS_TAP", "SENS_TAP"] and "SENS_ACC" in self.prefix:
            return S_Screen_Light_On()
        return S_Init()


class S_Light_On(State[INP, OUT]):
    def next(self, input: INP) -> State:
        if input == "SENS_ACCSENS_ACC":
            return S_Init()
        elif input == "SENS_TAP":
            return S_After(["SENS_TAP"])
        elif input == "SENS_TAPSENS_TAP":
            return S_Screen_Light_On()
        return self


class S_Screen_On(State[INP, OUT]):
    def next(self, input: INP) -> State:
        if input == "SENS_ACC":
            return S_After(["SENS_ACC"])
        elif input == "SENS_ACCSENS_ACC":
            return S_Screen_Light_On()
        elif input == "SENS_TAPSENS_TAP":
            return S_Init()
        return self


class S_Screen_Light_On(State[INP, OUT]):
    def next(self, input: INP) -> State:
        if input == "SENS_ACC":
            return S_After(["SENS_ACC"])
        elif input == "SENS_ACCSENS_ACC":
            return S_Screen_Light_On()
        elif input == "SENS_TAPSENS_TAP":
            return S_Init()
        return self