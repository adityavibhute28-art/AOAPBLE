
def heapifyIterative(arr, n, i, key = lambda x: x, reversed=False):
    largest = i

    while True:
        left = 2 * i
        right = 2 * i + 1

        if left < n and (key(arr[left]) > key(arr[largest])) ^ reversed:
            largest = left
        
        if right < n and (key(arr[right]) > key(arr[largest])) ^ reversed:
            largest = right

        if (largest != i):
            arr[largest], arr[i] = arr[i], arr[largest]
            i = largest
        else:
            break

def heapSortIterative(arr, key = lambda x: x, reversed=False):
    n = len(arr)

    for i in range(n // 2, -1, -1):
        heapifyIterative(arr, n, i, key, reversed)


    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapifyIterative(arr, i, 0, key, reversed)