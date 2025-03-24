#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# simply use
import sys, os
import timeit

#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "easycpp")))
from easycpp import easycpp


cpp = easycpp('''
#include <vector>
using namespace std;

extern "C" int sieve(int n);

int sieve(int n) {
    vector<bool> prime(n + 1, true);
    prime[0] = prime[1] = false;

    for (int i = 2; i * i <= n; ++i) {
        if (prime[i]) {
            for (int j = i * i; j <= n; j += i) {
                prime[j] = false;
            }
        }
    }

    int rn = 0;
    int rmax = 0;
    for (int i = 2; i <= n; ++i) {
        if (prime[i]) rn++,rmax=i;
    }
    return rn;
}


''')


def pysieve(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False

    for i in range(2, int(n ** 0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False

    primes = [i for i in range(2, n + 1) if is_prime[i]]
    return len(primes)



n = 10**6

print(f'python:sieve({n})')
rn = pysieve(n)
print(f'count:{rn}')

print(f'cpp: sieve({n})')
rn = cpp.sieve(n)
print(f'count:{rn}')


print(f'python:sieve({n})')
execution_times = timeit.repeat('l=pysieve(n)', setup='from __main__ import n,pysieve', repeat=5, number=1)
for i, exec_time in enumerate(execution_times, 1):
    print(f"{i}. : {exec_time*1000000}  microseconds ")


print(f'cpp: sieve({n})')
execution_times = timeit.repeat('l=cpp.sieve(n)', setup='from __main__ import n,cpp', repeat=5, number=1)
for i, exec_time in enumerate(execution_times, 1):
    print(f"{i}. : {exec_time*1000000}  microseconds ")
