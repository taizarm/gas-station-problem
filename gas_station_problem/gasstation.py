def construct_array_diff(n, strArr):
    array_diff = [None] * n

    for i in range(1, n+1):
        gc = strArr[i]

        gc_split = gc.split(':')

        array_diff[i-1] = int(gc_split[0]) - int(gc_split[1])

    return array_diff


def GasStation(strArr):

    try:
        n = int(strArr[0])

        array_diff = construct_array_diff(n, strArr)

    except:
        return 'invalid input'

    smallest_index = 0
    sum = 0
    i = 0
    count = 0

    while count != n and smallest_index < n:
        sum += array_diff[i % n]

        if sum < 0:
            smallest_index += 1
            i = smallest_index
            sum = 0
            count = 0
        else:
            i += 1
            count += 1

    if smallest_index >= n:
        return 'impossible'
    else:
        return smallest_index + 1
