"""
TODO: Find a real package to do this with, don't roll your own!!
"""

import random
import math


# NOTE: In the future (3.10), can use built-in statistics.correlation
# from statistics import correlation
def correlation(x, y):
    # Assume len(x) == len(y)
    n = len(x)
    sum_x = float(sum(x))
    sum_y = float(sum(y))
    sum_x_sq = sum(xi * xi for xi in x)
    sum_y_sq = sum(yi * yi for yi in y)
    psum = sum(xi * yi for xi, yi in zip(x, y))
    num = psum - (sum_x * sum_y / n)
    den = pow((sum_x_sq - pow(sum_x, 2) / n) * (sum_y_sq - pow(sum_y, 2) / n), 0.5)
    if den == 0:
        return 0
    return num / den


def binconf(p, N, c=0.95):
    """
    Calculate binomial confidence interval based on the number of positive and
    negative events observed.

    Parameters
    ----------
    p: int
      number of positive events observed
    N: int
      number of total events observed
    c : optional, [0,1]
      confidence percentage. e.g. 0.95 means 95% confident the probability of
      success lies between the 2 returned values

    Returns
    -------
    theta_low  : float
      lower bound on confidence interval
    theta_high : float
      upper bound on confidence interval
    """
    p, N = float(p), float(N)

    if N == 0.0:
        return (0.0, 1.0)

    p = p / N
    z = normcdfi(1 - 0.5 * (1 - c))

    a1 = 1.0 / (1.0 + z * z / N)
    a2 = p + z * z / (2 * N)
    a3 = z * math.sqrt(p * (1 - p) / N + z * z / (4 * N * N))

    return (a1 * (a2 - a3), a1 * (a2 + a3))


def erfi(x):
    """Approximation to inverse error function"""
    a = 0.147  # MAGIC!!!
    a1 = math.log(1 - x * x)
    a2 = 2.0 / (math.pi * a) + a1 / 2.0

    return sign(x) * math.sqrt(math.sqrt(a2 * a2 - a1 / a) - a2)


def sign(x):
    if x < 0:
        return -1
    if x == 0:
        return 0
    if x > 0:
        return 1


def normcdfi(p, mu=0.0, sigma2=1.0):
    """Inverse CDF of normal distribution"""
    if mu == 0.0 and sigma2 == 1.0:
        return math.sqrt(2) * erfi(2 * p - 1)
    else:
        return mu + math.sqrt(sigma2) * normcdfi(p)


def safe_sample(group, n):
    if len(group) < n:
        return group
    return random.sample(group, n)
