from typing import Callable, Iterable, Iterator, TypeVar


T = TypeVar('T')


def multiply(
        n: int,
        fn: Callable[..., T],
        args=None,
        kwargs=None
        ) -> Iterator[T]:
    match (args, kwargs):
        case (None, None):
            mod_fn = lambda _: fn()
        case (None, kwargs):
            mod_fn = lambda i: fn(**(kwargs[i]))
        case (args, None):
            mod_fn = lambda i: fn(*(args[i]))
        case (args, kwargs):
            mod_fn = lambda i: fn(*(args[i]))
        case _:
            raise RuntimeError("...")
    return (mod_fn(i) for i in range(n))


print(list(multiply(5, int, args=("123"))))
