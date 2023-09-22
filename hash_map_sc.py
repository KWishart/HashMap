from DA_SC_OA import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        Adds a key, value pair to the hashmap
        """
        if self.table_load() >= 1.0:
            self.resize_table(self.get_capacity() * 2)
        hash = self._hash_function(key)
        index = hash % self._capacity
        for bucket in range(self._capacity):
            if self._buckets[bucket].contains(key):
                for node in self._buckets[bucket]:
                    if node.key == key:  # replace with new value
                        node.value = value
                        return
        self._buckets[index].insert(key, value)
        self._size += 1

    def empty_buckets(self) -> int:
        """
        Returns how many empty buckets are in the hash map
        """
        empty_buckets = self.get_capacity()
        for bucket in range(self.get_capacity()):
            if self._buckets[bucket].length() != 0:
                empty_buckets -= 1
        return empty_buckets

    def table_load(self) -> float:
        """
        Returns the table load
        """
        return self._size / self._capacity

    def clear(self) -> None:
        """
        Clears the hash map
        """
        self._buckets = DynamicArray()
        self._size = 0
        for bucket in range(self.get_capacity()):
            self._buckets.append(LinkedList())

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the table if the table load is >= 1
        """
        if new_capacity >= 1:
            old_table = self.get_keys_and_values()
            self._buckets = DynamicArray()
            self._size = 0
            if self._is_prime(new_capacity):
                self._capacity = new_capacity
            else:
                self._capacity = self._next_prime(new_capacity)
            for bucket in range(self.get_capacity()):
                self._buckets.append(LinkedList())
            for node in range(old_table.length()):
                key, value = old_table[node]
                self.put(key, value)

    def get(self, key: str):
        """
        Returns the value of an element in the hash table, otherwise returns None
        """
        if self.contains_key(key):
            for bucket in range(self._capacity):
                for node in self._buckets[bucket]:
                    if node.key == key:
                        return node.value
        else:
            return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the table contains the requested key, otherwise returns False
        """
        for bucket in range(self._capacity):
            if self._buckets[bucket].contains(key):
                return True
        return False

    def remove(self, key: str) -> None:
        """
        Removes a LinkedList node from the hash map if it exists
        """
        if self.contains_key(key):
            for bucket in range(self._capacity):
                for node in self._buckets[bucket]:
                    if node.key == key:
                        self._buckets[bucket].remove(key)
                        self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a DynamicArray containing all the key and value pairs stored in the table
        """
        keys_values = DynamicArray()
        for index in range(self._buckets.length()):
            if self._buckets[index].length() != 0:
                for node in self._buckets[index]:
                    keys_values.append((node.key, node.value))
        return keys_values


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Returns a tuple containing a DynamicArray of the mode value(s) in the table and the highest frequency
    """
    map = HashMap(da.length(), hash_function_1)
    frequency = 1
    modes = DynamicArray()
    for index in range(da.length()):
        if index == da.length() - 1:
            if da[index] != da[index - 1]:
                frequency = 1
            map.put(da[index], frequency)
        else:
            if da[index] == da[index + 1]:
                frequency += 1
            map.put(da[index], frequency)
            if da[index] != da[index + 1]:
                frequency = 1

    keys_vals = map.get_keys_and_values()

    # append mode(s) to Dynamic Array
    mode, frequency = keys_vals[0]
    if frequency == 1:
        modes.append(mode)
    for index in range(1, keys_vals.length()):
        mode2, frequency2 = keys_vals[index]
        if frequency == 1:
            modes.append(mode2)
        elif frequency > frequency2:
            modes.append(mode)
            return (modes, frequency)
        elif frequency == frequency2:
            modes.append(mode)
            modes.append(mode2)
            return (modes, frequency)
    return (modes, frequency)
