import hazelcast

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
queue = client.get_queue("queue").blocking()

for i in range(100):
    queue.offer(i)
    print(f"Produce {i}")
