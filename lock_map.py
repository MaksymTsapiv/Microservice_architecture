import hazelcast
import threading

def update_without_lock(map):

    for _ in range(1000):
        value = map.get(key)

        map.put(key, value + 1)

    print(map.get(key))


def update_passimistic_lock(map):

    for _ in range(1000):
        map.lock(key)
        
        value = map.get(key)
        map.put(key, value + 1)
        
        map.unlock(key)

    print(map.get(key))
        

def update_optimistic_lock(map):

    for _ in range(1000):
        while(True):

            value = map.get(key)
            new_value = value + 1

            if (map.replace_if_same(key, value, new_value) == True):
                break

    print(map.get(key))


def multirun(func, args, nthreads):

    threads = []
    for _ in range(nthreads):
        t = threading.Thread(target=func, args=(args,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


if __name__ == "__main__":
    key = "1"

    client = hazelcast.HazelcastClient(
        cluster_name="dev",
        cluster_members=[
            "127.0.0.1:5701",
            "127.0.0.1:5702",
            "127.0.0.1:5703",
        ],

        lifecycle_listeners=[
            lambda state: print("Lifecycle event >>>", state),
        ]
    )

    print("Connected to cluster")

    distributed_map = client.get_map("distributed-map").blocking()
    distributed_map.put(key, 0)

    print("Run without lock:")
    multirun(update_without_lock, distributed_map, 3)
    distributed_map.put(key, 0)
    
    print("Run passimistic lock:")
    multirun(update_passimistic_lock, distributed_map, 3)
    distributed_map.put(key, 0)
    
    print("Run optimistic lock:")
    multirun(update_optimistic_lock, distributed_map, 3)
    
    print("All done")
    client.shutdown()
