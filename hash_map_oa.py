from DA_SC_OA import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Adds a key value pair to the hash map
        """
        if self.table_load() >= 0.5:
            self.resize_table(self.get_capacity() * 2)
        hash = self._hash_function(key)
        index = hash % self._capacity
        initial_index = index
        j = 1
        while self._buckets[index] is not None:
            if self._buckets[index].is_tombstone is True:
                self._buckets[index] = HashEntry(key, value)
                self._size += 1
                self._buckets[index].is_tombstone = False
                return
            if self._buckets[index].key == key:
                self._buckets[index].value = value
                return
            else:
                index = (initial_index + j**2) % self.get_capacity()
                j += 1
        self._buckets[index] = HashEntry(key, value)
        self._size += 1

    def table_load(self) -> float:
        """
        Returns the table load
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns how many empty buckets are in the hash map
        """
        empty_buckets = self.get_capacity()
        for bucket in range(self.get_capacity()):
            if self._buckets[bucket] is not None:
                empty_buckets -= 1
        return empty_buckets

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the table if the table load is >= 0.5
        """
        if new_capacity >= self._size:
            old_table = self.get_keys_and_values()
            self._buckets = DynamicArray()
            self._size = 0
            if self._is_prime(new_capacity):
                self._capacity = new_capacity
            else:
                self._capacity = self._next_prime(new_capacity)
            for bucket in range(self.get_capacity()):
                self._buckets.append(None)
            for node in range(old_table.length()):
                key, value = old_table[node]
                self.put(key, value)

    def get(self, key: str) -> object:
        """
        Returns the value of an element in the hash map, otherwise returns None
        """
        if self.contains_key(key):
            for index in range(self.get_capacity()):
                if self._buckets[index] is not None:
                    if self._buckets[index].key == key:
                        if self._buckets[index].is_tombstone is True:
                            return None
                        else:
                            return self._buckets[index].value
        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns whether an element with the requested key exists in the table
        """
        for index in range(self.get_capacity()):
            if self._buckets[index] is not None:
                if self._buckets[index].key == key:
                    if self._buckets[index].is_tombstone is True:
                        return False
                    else:
                        return True
        return False

    def remove(self, key: str) -> None:
        """
        Removes a key, value pair from the table
        """
        if self.contains_key(key):
            for index in range(self.get_capacity()):
                if self._buckets[index] is not None:
                    if self._buckets[index].key == key:
                        if self._buckets[index].is_tombstone is False:
                            self._size -= 1
                            self._buckets[index].is_tombstone = True

    def clear(self) -> None:
        """
        Clears the hash map
        """
        self._buckets = DynamicArray()
        self._size = 0
        for bucket in range(self.get_capacity()):
            self._buckets.append(None)

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a DynamicArray containing all the key and value pairs
        """
        keys_values = DynamicArray()
        for index in range(self._buckets.length()):
            if self._buckets[index] is not None and self._buckets[index].is_tombstone is False:
                keys_values.append((self._buckets[index].key, self._buckets[index].value))
        return keys_values

    def __iter__(self):
        """
        Allows iteration through the hash map
        """
        self._index = 0

        return self

    def __next__(self):
        """
        Sets the index to point to the next element
        """
        if self._index >= self._buckets.length() or self._buckets[self._index] is None:
            raise StopIteration
        bucket = self._buckets[self._index]
        self._index += 1
        return bucket
