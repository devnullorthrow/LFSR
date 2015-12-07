from functools import reduce
from fractions import Fraction
from cmath import rect, pi
import getopt
import random
import sys


def flat_list(s, q):
    if type(s[0]) is int:
        return s
    elif type(s[0]) is list:
        return [reduce(lambda i, j: (i * q) + j, e) for e in s]
    else:
        raise TypeError


def xac(s, q=None, d=None, n=None):
    return xcc(s, s, q, d, n)


def xcc(s1, s2, q=None, d=None, n=None):

    def cc(s1, s2):
        assert type(s1[0]) == type(s2[0])
        if type(s1[0]) is list:
            s3 = [[(j - i) % q for i, j in zip(u, v)] for u, v in zip(s1, s2)]
            s4 = [reduce(lambda x, y: (x * q) + y, e) for e in s3]
            z = sum(rect(1, 2 * pi * i / q) for i in s4) / len(s1)
        elif type(s1[0]) is int:
            z = sum(rect(1, 2 * pi * (j - i) / q) for i, j in zip(s1, s2)) / len(s1)
        else:
            raise TypeError
        zr, zi = round(z.real, n), round(z.imag, n)
        if abs(zi % 1) < 10 ** -n:
            if abs(zr - round(zr)) < 10 ** -n:
                return int(zr)
            elif Fraction(z.real).limit_denominator().denominator <= d:
                return Fraction(z.real).limit_denominator()
            else:
                return zr
        else:
            return complex(zr, zi)

    q = 2 if q is None else q
    d = 30 if d is None else d
    n = 3 if n is None else n
    assert len(s1) == len(s2)
    return [cc(s1, s2[i:] + s2[:i]) for i in range(len(s1))]


def LFSR(P, S, M, N, K):
    """
    K sequence
    N elements
    M values of the LFSR sequence
    P polynom
    S initial state
    """
    def LFSR2():
        seq, st = [S[-1]], S
        for j in range(K ** len(S) - 2):
            st0 = sum([i * j for i, j in zip(st, P[1:])]) % K
            st = [st0] + st[:-1]
            seq += [st[-1]]
        return seq

    assert len(P) > 1 and len(P) - 1 == len(S)
    s = LFSR2()
    L = len(s)
    assert M <= L
    return [s[i % L] if M == 1 else (s[i % L:] + s[:i % L])[:M] for i in range(N)]


def get_rand_basis(count):
    return random.randint(1, count)


if __name__ == "__main__":

    optlist = None
    args = None

    try:
        optlist, args = getopt.getopt(sys.argv[1:], 'x', ['count='])
    except getopt.GetoptError as err:
        # print help information and exit:
        print >> sys.stderr, 'option not recognized'
        sys.exit(2)

    if (optlist is None or not len(optlist)) or (optlist[0][1] is None):
        print >> sys.stderr, "Please, check input arguments - file not exist"
        exit(2)
    count = int(optlist[0][1])

    if count is 0:
        print sys.stderr, "You are required empty sequence"
        exit(4)

    basis = get_rand_basis(count)
    print(basis)
    sec = LFSR([1, 1, 0, 1, 1], [0, 0, 0, 1], basis, count, 2)
    print("sequence =", sec)
    print("sequence =", flat_list(sec, 2))
