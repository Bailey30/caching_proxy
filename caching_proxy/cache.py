from typing import List, Tuple

# Define a custom type for a tuple containing two strings
EndpointData = Tuple[str, str]

# Define a custom type for a list of such tuples
EndpointBucket = List[EndpointData]


class Cache:
    size: int
    buckets: List[EndpointBucket]

    def __init__(self, size=100) -> None:
        self.size = size
        self.buckets = [[] for _ in range(size)]

    def hash_function(self, key) -> int:
        """
        Creates an index key for the item being added or searched for.
        In theory is evenly distributes items throughout the buckets.
        """
        sum_of_chars = 0
        for char in key:
            sum_of_chars += ord(char)

        return sum_of_chars % self.size

    def put(self, key, value) -> None:
        hash_index = self.hash_function(key)
        bucket = self.buckets[hash_index]

        # Check for an existing value to update.
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        # Adding a new value to hash table.
        self.buckets[hash_index].append((key, value))

    def get(self, key) -> str | None:
        hash_index = self.hash_function(key)
        bucket = self.buckets[hash_index]

        # Search for a value in the bucket.
        found = next(((k, v) for (k, v) in bucket if k == key), None)

        return found[0] if found else None

    def print_map(self) -> None:
        print("Hash map contents:")
        for index, bucket in enumerate(self.buckets):
            print(f"Bucket {index}: {bucket}")

    def clear(self) -> None:
        self.buckets = [[] for _ in range(self.size)]
