import threading
import hazelcast

def increment_key_pessimistic():
    client = hazelcast.HazelcastClient()
    my_map = client.get_map("my-map3").blocking()
    my_map.put_if_absent("key", 0)
    for _ in range(10000):
        try:
            my_map.lock("key")
            value = my_map.get("key")
            value += 1
            my_map.put("key", value)
        finally:
            my_map.unlock("key")
    client.shutdown()

if __name__ == "__main__":
    threads = []
    for i in range(3):
        thread = threading.Thread(target=increment_key_pessimistic)
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
