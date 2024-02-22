import random

array_size = 100

# 生成一个长度为10的整型数组
array = [random.randint(1, 1000) for _ in range(array_size)]
#print('array:', array)

#
split_size = int(0.9 * len(array))
print("split_size:", split_size)
print('---------------------------')

#
subarray1 = array[:split_size]
subarray2 = array[split_size:]

#
print('subarray1:', subarray1)
print('---------------------------')
print('subarray2:', subarray2)
print('---------------------------')

#exit()

#
context_size = 8
x = subarray1[:context_size]
y = subarray1[1:context_size + 1]

#
for t in range(context_size):
    context = x[:t +1]
    target = y[t]
    print(f'{t} context: {context} target: {target}')




