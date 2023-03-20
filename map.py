import hazelcast

def create_distribution_map(hz_client):
    map_size = 1000
    distributed_map = client.get_map("distributed-map")

    for i in range(map_size):
        distributed_map.set(i, f"value for {i}th key").result()

    get_future = distributed_map.get(int(map_size / 2))
    get_future.add_done_callback(lambda future: print(future.result()))

    print("Map size:", distributed_map.size().result())


if __name__ == "__main__":

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
    
    create_distribution_map(client)
    
    client.shutdown()
