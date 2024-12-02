import numpy as np  

a1 = np.array([1,2,3,4], dtype="uint32")
a2 = np.array([1,2,3,4.0])
b = np.array([[1,2,3,4],[5,6,7,8]])
print(b.size, b.shape, b.dtype, b[1,2], sep=", ")
# two's complement representation is widely used in computers for representing signed integers due to its simplicity and efficiency in arithmetic operations.
c = np.zeros((3, 4), dtype='uint32') + 3
d = np.ones((3, 4)) * 4
e = np.arange(12).reshape((3, 4))

f = c**2 + d**2 + e + np.random.randint(0, 5, (3, 4))

np.save("random.npy", f)
f = np.load("random.npy")


f = np.arange(24).reshape((4, 3, 2))
f[2, ...] = [[99, 99], [99, 99], [99, 99]]



"""
here:
We see that a[:2] returns the first two rows with an implied : for the second dimension, as the following line shows.




I may not be the strongest guy...but I've always been a whiz with numbers.

make a pass at


population-sample





 """