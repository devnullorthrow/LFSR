from functools import reduce
import getopt
import random
import sys
import time

current_millis_time = lambda: int(round(time.time() * 1000))

def flat_list(sequence, q):
    if type(sequence[0]) is int:
        return sequence
    elif type(sequence[0]) is list:
        return [reduce(lambda i, j: (i * q) + j, item) for item in sequence]
    else:
        raise TypeError

def LFSR(P, S, M, N, K):
    """
    K sequence
    N elements
    M values of the LFSR sequence
    P polynom
    S initial state
    """
    def lfsr_internal():
        seq, state_next = [S[-1]], S
        for j in range(K ** len(S) - 2):
            state0 = sum([i * j for i, j in zip(state_next, P[1:])]) % K
            state_next = [state0] + state_next[:-1]
            seq += [state_next[-1]]
        return seq

    assert len(P) > 1 and len(P) - 1 == len(S)
    s = lfsr_internal()
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

    sec = LFSR([1, 1, 0, 1, 1], [0, 0, 0, 1], count, count, 2)

    mod = count * count
    seed = current_millis_time() % mod
    seed = seed + count if seed < count else seed
    print(seed)

    print("sequence =", sec)
    array = flat_list(sec, seed)
    print("rand password =", ''.join(str(current) for current in array))
