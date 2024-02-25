import threading
import hazelcast


def produce():
    client = hazelcast.HazelcastClient()
    queue = client.get_queue("myqueue")
    for i in range(100):
        queue.offer("value-" + str(i))
        print(f"Producer added value-"+str(i))
    queue.put(-1).result() #poison pill
    client.shutdown()


def consume(num):
    client = hazelcast.HazelcastClient()
    queue = client.get_queue("myqueue") 
    consumed_count = 0
    while consumed_count < 100: 
        head = queue.take().result()
        if head == -1:
            queue.put(-1).result()
            break
        print(f"Consumer number {num} consuming {head}")
        consumed_count += 1
    client.shutdown()


if __name__ == "__main__":
    threads = []
    producer = threading.Thread(target=produce)
    producer.start()
    for i in range(2):
        thread = threading.Thread(target=consume, args=(i+1, ))
        threads.append(thread)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    producer.join()