import numpy as np

def npsum():
    a = np.array([0, 1, 2, 3, 4])
    b = np.array([9, 8, 7, 6, 5])
    c = a ** 2 + b ** 3
    return c

print(npsum())


### 1

import numpy as np

# Create a NumPy array
arr = np.array([[1, 2, 3], [4, 5, 6]])

# Show various properties
print("Array:\n", arr)
print("\nNumber of dimensions (ndim):", arr.ndim)
print("Shape of the array (shape):", arr.shape)
print("Total number of elements (size):", arr.size)
print("Data type of elements (dtype):", arr.dtype)
print("Size of each element (itemsize):", arr.itemsize, "bytes")
'''
Number of dimensions (ndim): 2
Shape of the array (shape): (2, 3)
Total number of elements (size): 6
Data type of elements (dtype): int32
Size of each element (itemsize): 4 bytes
'''

### 2

import numpy as np

result = np.concatenate([
    np.arange(16).reshape(4, 4),          # 1D array reshaped to (4, 4), be aware of what each 4 means,ndim 2-page;3-book
    np.ones((4, 4)),                      # Shape (4, 4)
    np.full((4, 4), 7),                   # Shape (4, 4), filled with 7
    np.eye(4),                            # Shape (4, 4), identity matrix
    np.linspace(0, 1, 16).reshape(4, 4)   # 1D array reshaped to (4, 4); linspace can also have endpoint=False
], axis=0) # axis default is 0

print(result)


### 3 

# 多维数组的索引和切片： 索引用逗号，切片用冒号； 建议用a = np.arange(24).reshape((2,3,4)) 来练习

a = np.random.rand(16) > 0.5
a = np.random.rand(16)
a[np.where(a >0.5)]

'''
I want to combine the following functions or usages into a single line of code to demonstrate all the concepts at once, so I can better memorize them: 
np.arange(), np.ones(), np.full(), np.eye(), np.linspace(), and np.concatenate().
'''