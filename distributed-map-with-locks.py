import threading
import hazelcast

def increment_key():
    client = hazelcast.HazelcastClient()
    my_map = client.get_map("my-map2").blocking()
    my_map.put_if_absent("key", 0)
    for _ in range(10000):
        value = my_map.get("key")
        value += 1
        my_map.put("key", value)
    client.shutdown()

if __name__ == "__main__":
    threads = []
    for i in range(3):
        thread = threading.Thread(target=increment_key)
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
