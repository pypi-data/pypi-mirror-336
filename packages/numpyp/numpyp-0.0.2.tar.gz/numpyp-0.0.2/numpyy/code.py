import pyperclip

def z_1_1():
    answer = f"""
# Переполнение
a = 1e308
b = 1e308
c = a * b  # Это может привести к переполнению, результат будет 'inf' (бесконечность)
print(c)
"""
    pyperclip.copy(answer)
    pyperclip.paste()

def z_1_2():
    answer = f"""
# Потеря точности
a = 0.1 + 0.2
b = 0.3
print(f'a = ', a, ', b = ', b, ', a == b: ',a == b')  # Ожидается True, но результат False
"""
    pyperclip.copy(answer)
    pyperclip.paste()

def z_1_3():
    answer = f"""
# Ошибка округления
a = 1.0000000000000001
b = 1.000000000000002
print(a + b)  # Ожидаем 2.0000000000000021, но результат может быть немного другим из-за округления
"""
    pyperclip.copy(answer)
    pyperclip.paste()

def z_1_4():
    answer = f"""
# Накопление ошибок
sum = 0.0
for i in range(100000):
    sum += 0.0001
print(sum)  # Может быть немного меньше 10, в зависимости от точности чисел"""
    pyperclip.copy(answer)
    pyperclip.paste()

def z_1_5():
    answer = f"""
# Потеря значимости
a = 1.0000000000000001
b = 1.0000000000000002
print(a + b)   # Очень маленькая разница, которая может быть искажена из-за ограниченной точности
"""
    pyperclip.copy(answer)
    pyperclip.paste()

def z_1_6():
    answer = f"""
def kahan_sum(x):
    s = 0.0
    c = 0.0
    for i in range(len(x)):
        y = x[i] - c
        t = s + y
        c = (t - s) - y
        s = t
    return s"""
    pyperclip.copy(answer)
    pyperclip.paste()

def z_1_7():
    answer = f"""
import numpy as np
import time
from numba import jit

n = 10**6

np.random.seed(42)
x = np.random.uniform(-1,1,n).astype(np.float32)

true_sum = np.sum(x, dtype=np.float64)

def naive_sum(x):
    s = np.float32(0.0)
    for i in range(len(x)):
        s += x[i]
    return s

@jit(nopython=True)
def kahan_sum(x):
    s = np.float32(0.0)
    c = np.float32(0.0)
    for i in range(len(x)):
        y = x[i] - c
        t = s + y
        c = (t - s) - y
        s = t
    return s

start = time.time()
d_sum = naive_sum(x)
time_naive = time.time() - start

start = time.time()
k_sum = kahan_sum(x)
time_kahan = time.time() - start

start = time.time()
np_sum = np.sum(x, dtype=np.float32)
time_numpy = time.time() - start

print("Ошибка в naive sum: ",d_sum - true_sum)
print("Ошибка в Kahan sum: ",k_sum - true_sum)
print("Ошибка в NumPy sum: ",np_sum - true_sum)

print("\nВремя выполнения:")
print(f"Naive sum: ", time_naive, "сек")
print(f"Kahan sum: ", time_kahan, "сек")
print(f"NumPy sum: ", time_numpy, "сек")"""
    pyperclip.copy(answer)
    pyperclip.paste()