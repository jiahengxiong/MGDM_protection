import numpy as np
import random


def gen_request(lim_rate):
    request = []
    total_rate = 0
    i = 0
    rate_list = [100, 200, 300]

    while total_rate < lim_rate:
        src, dst = random.sample(range(1, 18), 2)
        if total_rate < lim_rate:
            rate = random.choice(rate_list)
            if total_rate + rate > lim_rate:
                rate = lim_rate - total_rate
            request.append((src, dst, rate, i + 1))
            total_rate += rate
            i = i + 1

    return request
