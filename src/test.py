import numpy as np
#
# a = np.arange(12).reshape(3, 4)
# d = a
# a=np.delete(a, [0], axis=0)
#
# print('第一个数组：')
# print(a)
# print('\n')
#
# print('d:')
# # 这种方法b会随着a改变
# print(d)
# print('\n')


# m = [1, 2, 4, 7, 6]
# for i in range(len(m)):
#     if i >= 1 and m[i] - m[i-1] <= 1:
#         del m[i-1]
# print(m)
# print('b:')
# # 这种方法b会随着a改变
# b = a[1:, :]
# print(b)
#
# print('c:')
# # 这种方法c不会随着a改变
# c=np.delete(a, [1], axis=0)
# print(c)
# print('\n')
#
# a[2][0] = -1
# print('c:')
# print(c)
# print('\n')
# print('b:')
# print(b)

import numpy as np
from numpy.linalg import solve

a = np.mat([[154, 1], [256, 1]])  # 系数矩阵
b = np.mat([190, 470]).T  # 常数项列矩阵
x = solve(a, b)  # 方程组的解
print(x)
