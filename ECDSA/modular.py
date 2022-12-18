class InverseModularError(Exception):
    pass


def gcd(a, b):
    s, old_s = 0, 1
    t, old_t = 1, 0
    r, old_r = b, a

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_r, old_s, old_t


def modexp(base, exp, n):

    if base == 0:
        return 0

    intermediate = 1
    b = base
    e = exp

    while e != 0:
        if e % 2 != 0:
            intermediate = (intermediate * b) % n

        e /= 2
        b = (b * b) % n

    return intermediate


def invmod(a, m):

    g, x, y = gcd(a, m)
    if g != 1:
        raise InverseModularError('The modular inverse does not exist')
    else:
        return x % m
