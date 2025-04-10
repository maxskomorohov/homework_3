import time
import functools
import asyncio

# Функція визначення простих чисел
def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False

    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


# Функція для розділення діапазону чисел на рівні частини
def divide_range(start, end, thread_count):
    # Кількість чисел в діапазоні
    range_size = end - start + 1

    # Кількість чисел в кожному потоці при цілочисельному діленні
    step_size = range_size // thread_count

    # Залишок, що потрібно рівномірно поділити між потоками
    remainder = range_size % thread_count

    # Список для зберігання діапазонів для кожного потоку
    ranges = []

    for i in range(thread_count):
        # Визначення початкового числа для діапазону, що обчислюється
        thread_start = start + i * step_size + min(i, remainder)

        # Визначаємо кінець діапазону для потоку
        # Якщо це останній потік, додаємо залишок
        thread_end = thread_start + step_size + (1 if i < remainder else 0) - 1

        # Для останнього потоку оновлюємо кінець діапазону, щоб він не перевищував кінцеву точку
        if i == thread_count - 1:
            thread_end = end

        # Додаємо цей діапазон в список
        ranges.append((thread_start, thread_end))

    return ranges

# print(divide_range(1, 99, 10))
# print(divide_range(1, 50, 3))


# Декоратор для вимірювання часу синхронної функції
def measure_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Функція {func.__name__} виконується за {end_time - start_time:.4f} секунд")
        return result
    return wrapper

# Декоратор для вимірювання часу асинхронної функції
def async_measure_time(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        print(f"Функція {func.__name__} виконується за {end_time - start_time:.4f} секунд")
        return result
    return wrapper