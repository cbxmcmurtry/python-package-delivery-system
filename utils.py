import csv
from data_structures import HashTable


def load_package_file(file_name):
    packages = HashTable()
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            package_id = int(row[0])
            package_address = f"{row[1]}, {row[2]}, {row[3]} {row[4]}"

            package_data = {
                'address': row[1],
                'city': row[2],
                'state': row[3],
                'zip': row[4],
                'deadline': row[5],
                'weight': row[6],
                'note': row[7] if len(row) > 7 else '',
                'status': 'at hub',
                'delivery_time': None,
                'truck_number': None,
            }
            packages.insert(package_id, package_data)
    return packages
