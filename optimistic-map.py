import threading
import hazelcast

def increment_key_optimistic():
    client = hazelcast.HazelcastClient()
    my_map = client.get_map("my-map4").blocking()
    my_map.put_if_absent("key", 0)
    for _ in range(10000):
        while True:
            old_value = my_map.get("key")
            new_value = old_value
            new_value += 1
            if my_map.replace_if_same("key", old_value, new_value):
                break
    client.shutdown()

if __name__ == "__main__":
    threads = []
    for i in range(3):
        thread = threading.Thread(target=increment_key_optimistic)
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
