# %% Basic case
import concurrent.futures
import multiprocessing

shared_dict = dict()

def init_globals(shared):
    global shared_dict
    shared_dict = shared

def update_globals(key, value):
    global shared_dict
    shared_dict[key] = value
    print(f"Updated shared_dict with {key}: {value}")

def main():
    global shared_dict
    manager = multiprocessing.Manager()
    shared_dict = manager.dict()

    with concurrent.futures.ProcessPoolExecutor(max_workers=4, initializer=init_globals, initargs=(shared_dict,)) as exc:
        futures = [exc.submit(update_globals, f'key_{i}', f'val_{i}') for i in range(10)]

        for future in concurrent.futures.as_completed(futures):
            future.result()

    print(f'Final global result: {shared_dict}')

if __name__ == '__main__':
    main()

# %% Check that the old method does not work still
import concurrent.futures
import multiprocessing

shared_dict_update = dict()
shared_dict_read =  {"jack": "lambert"}

def init_globals(shared):
    global shared_dict_update
    shared_dict_update = shared

def update_globals(key, value):
    global shared_dict_update, shared_dict_read
    shared_dict_update[key] = value
    print(f"Updated shared_dict with {key}: {value}")
    print(f'Reading from global "shared_dict_read": {shared_dict_read}')

def main():
    global shared_dict_update
    manager = multiprocessing.Manager()
    shared_dict_update = manager.dict()

    with concurrent.futures.ProcessPoolExecutor(max_workers=4, initializer=init_globals, initargs=(shared_dict_update,)) as exc:
        futures = [exc.submit(update_globals, f'key_{i}', f'val_{i}') for i in range(10)]

        for future in concurrent.futures.as_completed(futures):
            future.result()

    print(f'Final global result: {shared_dict_update}')

if __name__ == '__main__':
    main()

# %% Do we need a global at all 
# %% Nesting two process pools vs thread pool
import time
import concurrent.futures
import multiprocessing

shared_dict = dict()

def init_globals(shared):
    global shared_dict
    shared_dict = shared

def update_globals_again(key, value):
    global shared_dict
    shared_dict[key] = value
    print(f"Updated shared_dict with {key}: {value}")

def update_globals_pool(key, value):
    global shared_dict
    with concurrent.futures.ProcessPoolExecutor(max_workers=4, initializer=init_globals, initargs=(shared_dict,)) as exc:
        futures = [exc.submit(update_globals_again, f'{key}_{j}', f'{value}_{j}') for j in range(10)]
        for future in concurrent.futures.as_completed(futures):
            future.result()

def update_globals_thread(key, value):
    global shared_dict
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as exc:
        futures = [exc.submit(update_globals_again, f'{key}_{j}', f'{value}_{j}') for j in range(10)]
        for future in concurrent.futures.as_completed(futures):
            future.result()

def main():
    global shared_dict
    manager = multiprocessing.Manager()
    shared_dict = manager.dict()

    with concurrent.futures.ProcessPoolExecutor(max_workers=4, initializer=init_globals, initargs=(shared_dict,)) as exc:
        futures = [exc.submit(update_globals_thread, f'key_{i}', f'val_{i}') for i in range(10)]

        for future in concurrent.futures.as_completed(futures):
            future.result()

    print(f'Final global result: {shared_dict}')

if __name__ == '__main__':
    s_time = time.time()
    main()
    print(f'Total time: {time.time() - s_time}')

# %% Just using thread pools so I dont need to create manager
import time
import concurrent.futures

shared_dict = dict()

def update_globals_again(key, value):
    global shared_dict
    shared_dict[key] = value
    print(f"Updated shared_dict with {key}: {value}")


def update_globals_thread(key, value):
    global shared_dict
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as exc:
        futures = [exc.submit(update_globals_again, f'{key}_{j}', f'{value}_{j}') for j in range(10)]
        for future in concurrent.futures.as_completed(futures):
            future.result()

def main():
    global shared_dict
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as exc:
        futures = [exc.submit(update_globals_thread, f'key_{i}', f'val_{i}') for i in range(10)]
        for future in concurrent.futures.as_completed(futures):
            future.result()

    print(f'Final global result: {shared_dict}')

if __name__ == '__main__':
    s_time = time.time()
    main()
    print(f'Total time: {time.time() - s_time}')

# %%
