class HashTable:
    def __init__(self, size=40):
        self.size = size
        self.table = [None] * size

    def _hash_function(self, key):
        return key % self.size

    def insert(self, package_id, package_data):
        index = self._hash_function(package_id)
        if self.table[index] is None:
            self.table[index] = []
        self.table[index].append((package_id, package_data))

    def lookup(self, package_id):
        index = self._hash_function(package_id)
        if self.table[index] is not None:
            for pair in self.table[index]:
                if pair[0] == package_id:
                    return pair[1]
        return None

    def all_packages(self):
        all_packages = []
        for bucket in self.table:
            if bucket is not None:
                for package in bucket:
                    all_packages.append(package)
        return all_packages
