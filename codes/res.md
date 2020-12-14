
--- 
Q1  D

--- 
Q2  B

--- 
Q3  D

--- 
Q4  D

--- 
Q5  E

--- 
Q6  A


## Part 2
Q1
```python
"tim"
['t', 'i', 'm', 'e']
```

--- 
Q2
```python
[3, 4]
[4, 5]
[1, 3, 5]
```

--- 
Q3
```python
5, [5, 1], ?
```

--- 
Q4
```python
foo = ('h', 'b', 'w', 's')
bar = ('h', 'b')
```

--- 
Q5
```python
1, 1, 2, 3, 5
```

--- 
Q6 ??

--- 
Q7:
```
# print(list(map(lambda x: x * x, foo)))
[1, 4, 9, 16]

# print(list(filter(lambda x: x % 2 == 0, foo)))
[2, 4]
```

--- 
Q8:

```python
# print(Parent.x, Child1.x, Child2.x, c1, c2)
1, 1, 1, 1, ?
 
# Child1.x = 2
# print(Parent.x, Child1.x, Child2.x, c1, c2)
1, 2, 1, 4, ?

# Parent.x = 3
# print(Parent.x, Child1.x, Child2.x, c1, c2)
3, ?, ?, ?, ?
```

--- 
Q9 ?

--- 
Q10 ?
```python
1
2
```

## Part 3
```python
from typing import List


def sol1(arr: List) -> int:
    sz = len(arr)
    if sz == 1: return arr[0]
    fst, lst = arr[0], arr[-1]

    if fst * lst == 0:
        return 0
    elif fst * lst > 0:
        return fst if fst > 0 else lst
    else:
        lo, hi = 0, sz - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if arr[mid] * arr[lo] * arr[hi] == 0: return 0
            if mid == lo or mid == hi:
                return arr[lo] if abs(arr[lo]) < abs(arr[hi]) else arr[hi]
            if arr[lo] * arr[mid] > 0:
                lo = mid
            if arr[hi] * arr[mid] > 0:
                hi = mid
        return 0


def sol2(arr: List) -> int:
    def partition(arr, lo, hi):
        i = lo - 1
        for j in range(lo, hi):
            if arr[j] <= arr[hi]:
                i = i + 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[hi] = arr[hi], arr[i + 1]
        return (i + 1)

    def qsort(arr, lo, hi):
        if lo < hi:
            pi = partition(arr, lo, hi)
            qsort(arr, lo, pi - 1)
            qsort(arr, pi + 1, hi)

    n = len(arr)
    qsort(arr, 0, n - 1)
    return arr[n // 2]


def sol3(k: int) -> int:
    dp = [0] * (k + 1)
    if k <= 2: return 1
    a, b = 1, 1
    for i in range(3, k + 1):
        c = a + b
        b, a = a, c
    return c


if __name__ == '__main__':
    arr = [-6, -5, -4, -3, 0, 4, 5, 6, 7]
    print(sol1(arr))
    print(sol2(arr))
    print(sol3(4))
```
