import threading
from util_funcs import *

# Обчислення діапазону в одному потоці
def find_primes_single_thread(start, end):
    return [i for i in range(start, end + 1) if is_prime(i)]

# print(find_primes_single_thread(1, 10))
# print(find_primes_single_thread(1, 100))

start_time = time.time()
find_primes_single_thread(1, 100000)
end_time = time.time()
total_time = end_time - start_time
print(f"Функція find_primes_single_thread виконується за {total_time:.6f} секунд")



# Обчислення діапазону в декілька потоків
@measure_time
def find_primes_multi_thread(start, end, thread_count):

    # Отримання діапазонів
    ranges = divide_range(start, end, thread_count)

    threads = []
    results = []

    # Клас для блокування змінної для спільного доступу
    lock = threading.Lock()

    def thread_task(start, end):
        result = find_primes_single_thread(start, end)
        # Блокування змінної для спільного доступу
        with lock:
            results.append(result)

    # Запуск потоків
    for n in ranges:
        thread = threading.Thread(target=thread_task, args=(n[0], n[1]))
        threads.append(thread)
        thread.start()

    # Групування потоків для очікування виконання кожного з них
    for thread in threads:
        thread.join()

    # Об'єднання результатів з декількох списків
    primes = [prime for sublist in results for prime in sublist]
    return primes

find_primes_multi_thread(0, 100000, 10)


@async_measure_time
async def find_primes_asyncio(start, end, thread_count):

    # Отримання діапазонів
    ranges = divide_range(start, end, thread_count)

    tasks = []
    results = []

    # Асинхронная задача для каждого диапазона
    async def thread_task(start, end):
        result = find_primes_single_thread(start, end)
        results.append(result)

    # Запуск всех асинхронных задач
    for n in ranges:
        task = asyncio.create_task(thread_task(n[0], n[1]))
        tasks.append(task)

    # Ожидание завершения всех задач
    await asyncio.gather(*tasks)

    # Объединение всех результатов в один список
    primes = [prime for sublist in results for prime in sublist]
    return primes

async def main():
    primes = await find_primes_asyncio(1, 100000, 10)


asyncio.run(main())
