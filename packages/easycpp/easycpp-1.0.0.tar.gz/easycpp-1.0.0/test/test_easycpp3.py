#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 测试多段c++代码,以及so (必须先运行test/test_easycpp.py)
import sys, os
import timeit
from ctypes import POINTER, c_int, byref

#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "easycpp")))
from easycpp import easycpp
import easycpp as esp


esp.debugon()
cpp1 = easycpp('''
#include <vector>
using namespace std;

extern "C" int sieve1(int n, int *end);

int sieve1(int n, int *end) {
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


''', '/tmp', 'sieve1;', "g++ -O3 -g -shared -fPIC")

cpp2 = easycpp('''
#include <vector>
using namespace std;

extern "C" int sieve2(int n);

int sieve2(int n) {
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

# 测试使用现有so
cpp3 = easycpp('test/easycpp_8da973ce2166f141c895cc95818c29f9.so')



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

print(f'cpp1: sieve({n})')
rmax = c_int()   # 创建一个 c_int 变量，用于传递给函数
rn = cpp1.sieve1(n, byref(rmax))
print(f'count:{rn} bigest:{rmax}')

print(f'cpp2: sieve({n})')
rn = cpp2.sieve2(n)
print(f'count:{rn}')

print(f'cpp3(so): sieve({n})')
rn = cpp3.sieve(n)
print(f'count:{rn}')

