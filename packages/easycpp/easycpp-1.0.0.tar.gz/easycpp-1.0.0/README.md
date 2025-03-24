## Description

To use C/C++ conveniently in Python

## Functional Features

- **Support for embedding C++ functions in .py files**: It is convenient to use embedded C++ functions instead of Python functions to accelerate code execution.
- **Calling dynamic libraries**: Similar to ctypes.CDLL

## Dependencies

- Python >= 3.7
- pip

## Installation

```bash
$ pip install easycpp
```

## Usage Examples

Use the easycpp module to insert C++ code in a .py file. test.py:

```python
import sys, os
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


n = 10**6
rn = cpp.sieve(n)
print(f'count:{rn}')
```

2. Run like normal Python code:

```bash
$ python3 test.py
```

## Performance
Achieving a 20x speedup in prime number calculation.

output for test/testeasycpp.py:

```
python:sieve(1000000)
count:78498
cpp: sieve(1000000)
count:78498
python:sieve(1000000)
1. : 41969.04803393409  microseconds
2. : 40655.971970409155  microseconds
3. : 40405.491017736495  microseconds
4. : 40510.52400609478  microseconds
5. : 40443.39497340843  microseconds
cpp: sieve(1000000)
1. : 1861.8699978105724  microseconds
2. : 1843.6360405758023  microseconds
3. : 1847.2519586794078  microseconds
4. : 1861.9759939610958  microseconds
5. : 1847.1599905751646  microseconds
```

## Attention

Must specify parameter `func_signatures` on Windows.
