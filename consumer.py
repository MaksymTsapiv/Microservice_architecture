import hazelcast
import sys

uuid = sys.argv[1]

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

while(True):
    head = queue.take()
    print(f"Consumer {uuid} consumes {head}")
