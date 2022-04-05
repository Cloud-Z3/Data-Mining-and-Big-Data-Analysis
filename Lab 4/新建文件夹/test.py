nums = [4, 1, 5, 2, 9, 6, 8, 7]
sorted_nums = sorted(enumerate(nums), key=lambda x: x[1])
idx = [i[0] for i in sorted_nums]
nums = [i[1] for i in sorted_nums]
print(idx)
print(nums)
