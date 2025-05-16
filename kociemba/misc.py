def rotate_right(arr, left, right):
    temp = arr[right]
    for i in range(right, left, -1):
        arr[i] = arr[i-1]
    arr[left] = temp


def rotate_left(arr, left, right):
    temp = arr[left]
    for i in range(left, right):
        arr[i] = arr[i+1]
    arr[right] = temp


def c_nk(n, k):
    if n < k:
        return 0
    if k > n // 2:
        k = n - k
    s, i, j = 1, n, 1
    while i != n - k:
        s *= i
        s //= j
        i -= 1
        j += 1
    return s
