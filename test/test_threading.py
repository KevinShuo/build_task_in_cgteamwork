import concurrent.futures


def worker(num):
    print(f"Thread-{num} is running")
    return num


if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for i in range(11):
            future = executor.submit(worker, i)
            futures.append(future)

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            print(f"Thread-{result} is done")
