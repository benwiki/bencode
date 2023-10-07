from typing import Callable
from functools import partial


def suppress(f: Callable, ignore: tuple) -> Callable:
    def g():
        try:
            f()
        except (ignore):
            return None
        else:
            return f()
    return g

#    def g(*args, **kwargs):
#        if len(ignore) > 0:
#            for i in ignore:
#                try:
#                    f()
#                except i:
#                    return None
#                else:
#                    return f()
#    return g

m=2


if __name__ == "__main__":
    def foo(n: int) -> int:
        return 35 // n

    print(suppress(partial(foo, 1), ())())
    assert suppress(partial(foo, 1), ())() == 35 == foo(1)
    suppress(partial(foo, 0), (ZeroDivisionError,))()
    #suppress(partial(foo, 0), ())()
    def c():
    	global m
    	m -= 1
    	return 1 / m
    suppress(c, (ZeroDivisionError,))()