from itertools import permutations as perms
from pprint import pprint


def f(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    # assert len(a) == len(b)
    return tuple(b[i] for i in a)


def fAll(a: tuple[int, ...], b: set[tuple[int, ...]]) -> frozenset[tuple[int, ...]]:
    return frozenset(f(a, x) for x in b)


def slash(
    a: set[tuple[int, ...]], b: set[tuple[int, ...]]
) -> set[frozenset[tuple[int, ...]]]:
    return {fAll(x, b) for x in a}


def fAll2(
    a: set[tuple[int, ...]], b: set[tuple[int, ...]]
) -> frozenset[tuple[int, ...]]:
    return frozenset(f(x, y) for x in a for y in b)


def withletters(
    d: dict[frozenset[tuple[int, ...]], tuple[int, ...]]
) -> dict[tuple[str, ...], str]:
    return {
        tuple(sorted("".join(tuple(chr(65 + a) for a in x)) for x in k)): "".join(
            tuple(chr(65 + x) for x in v)
        )
        for k, v in d.items()
    }


def uebungsblatt3() -> None:
    D = {(0, 1, 2, 3), (1, 0, 3, 2), (2, 3, 0, 1), (3, 2, 1, 0)}
    S3 = set(perms(range(3)))
    S4 = set(perms(range(4)))
    S4_D = slash(S4, D)
    # pprint(S4_D)
    S4_Dt = tuple(S4_D)
    S3t = tuple(S3)
    # phi = {S4_Dt[i]: S3t[i] for i in range(len(S3))}
    # print(phi)
    L = tuple(perms(range(6)))
    # print(l)
    for phi in ({S4_Dt[l[i]]: S3t[i] for i in l} for l in L):
        ok = True
        for g1, g2 in ((g1, g2) for g1 in S4_D for g2 in S4_D):
            if phi[fAll2(g1, g2)] != f(phi[g1], phi[g2]):
                ok = False
            # else:
            #     print(phi[fAll2(g1, g2)], f(phi[g1], phi[g2]))
            # print(phi[fAll2(g1, g2)], f(phi[g1], phi[g2]))
        print("#" if ok else "-", end="")
        if ok:
            print("Found a solution:")
            pprint(tuple(sorted(withletters(phi).items(), key=lambda a: a[1])))
            # break


def uebungsblatt4() -> None:
    S3 = {(0, 1, 2, 3), (1, 0, 3, 2), (2, 3, 0, 1), (3, 2, 1, 0)}
    # S3 = set(perms(range(5)))
    Z3 = set(x for x in S3 if all(f(x, y) == f(y, x) for y in S3))
    print(Z3, len(Z3))


def main():
    uebungsblatt4()


if __name__ == "__main__":
    main()
