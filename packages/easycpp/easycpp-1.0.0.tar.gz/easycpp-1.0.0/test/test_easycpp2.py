#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 带参数使用
import sys, os
import timeit
from ctypes import POINTER, c_int, byref

#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "easycpp")))
import easycpp


easycpp.debugon()
cpp = easycpp.easycpp('''
#include <vector>
using namespace std;

extern "C" int sieve(int n, int *end);

int sieve(int n, int *end) {
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
    *end = rmax;
    return rn;
}


''', '/tmp', 'sieve;', "g++ -O3 -g -shared -fPIC")

# 如果需要可以定义函数的参数类型和返回值类型
#cpp.sieve.argtypes = [c_int, POINTER(c_int)]
#cpp.sieve.restype = c_int


def pysieve(n):
    # 初始化一个布尔值列表，所有数默认是质数（True）
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False  # 0 和 1 不是质数

    # 从 2 开始筛选所有质数
    for i in range(2, int(n ** 0.5) + 1):  # 只需要筛到 sqrt(n)
        if is_prime[i]:  # 如果当前数是质数
            for j in range(i * i, n + 1, i):  # 从 i^2 开始，标记所有 i 的倍数
                is_prime[j] = False

    # 返回所有质数
    primes = [i for i in range(2, n + 1) if is_prime[i]]
    return len(primes), primes[-1]



n = 10**6

print(f'python:sieve({n})')
rn, rmax = pysieve(n)
print(f'count:{rn} bigest:{rmax}')

print(f'cpp: sieve({n})')
rmax = c_int()   # 创建一个 c_int 变量，用于传递给函数
rn = cpp.sieve(n, byref(rmax))
print(f'count:{rn} bigest:{rmax}')


print(f'python:sieve({n})')
execution_times = timeit.repeat('l=pysieve(n)', setup='from __main__ import n,pysieve', repeat=5, number=1)
for i, exec_time in enumerate(execution_times, 1):
    print(f"第 {i} 次执行时间: {exec_time*1000000} 微秒")

print(f'cpp: sieve({n})')
execution_times = timeit.repeat('l=cpp.sieve(n,byref(rmax))', setup='from __main__ import n,cpp,rmax,byref', repeat=5, number=1)
for i, exec_time in enumerate(execution_times, 1):
    print(f"第 {i} 次执行时间: {exec_time*1000000} 微秒")
