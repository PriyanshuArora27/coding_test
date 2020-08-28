# This script is the solution for problem 2.
# Problem Statement below:

"""
Counting the pairs with k different from an integer list.
eg: list = [1, 3,5] and k = 2
expected: we will have 2 pairs: {(1,3), (3,5)}
Note: we also consider the negative numbers. You may only use Python
"""


def pairs(arr: list, k: int):
    int_set = set(arr)
    count = 0
    for x in arr:
        if x + k in int_set:
            print(f"{x} {x+k}")
            count += 1
        if x - k in int_set:
            count += 1
    return int(count / 2)


if __name__ == "__main__":
    my_array = list(
        map(
            int, input("Enter the list on which you want to obtain the pairs: ").split()
        )
    )
    diff = int(input("Enter the differnce that you want in the digits of pairs: "))
    pair_count = pairs(my_array, diff)
    print(f"The number of pairs that have the diffence of {diff} are: {pair_count}")
