import csv
from datetime import datetime, timedelta
from gui_interface import run_gui
from data_structures import HashTable
from geocode import get_coordinates
import folium
import os

# Function to load address data from the address file
def load_address_file(file_name):
    addresses = {}
    with open(file_name, 'r') as file:
        for line in file:
            # Splits the line with commas to get index, name, and address
            parts = line.strip().split(',')
            index = int(parts[0])
            name = parts[1]
            address = parts[2]
            addresses[index] = f"{name}, {address}"
    return addresses

# Function to load package data from the package file into a hash table
def load_package_file(file_name):
    packages = HashTable()
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            package_id = int(row[0])
            package_data = {
                'address': row[1],
                'city': row[2],
                'state': row[3],
                'zip': row[4],
                'deadline': row[5],
                'weight': row[6],
                'note': row[7] if len(row) > 7 else '',
                'status': 'at hub',  # Starting status is set to 'at hub'
                'delivery_time': None,
                'truck_number': None,
            }
            packages.insert(package_id, package_data)
    return packages

# Function to load distances from the distance file into a matrix.
def load_distance_file(file_name):
    distances = []
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            # Convert each value to float.
            distances.append([float(x) if x else 0.0 for x in row])
    return distances

# Truck class to manage individual truck attributes and behaviors.
class Truck:
    def __init__(self, truck_id):
        self.truck_id = truck_id
        self.packages = []  # List of package IDs assigned to the truck
        self.current_location = 0  # Starting at the hub
        self.miles_traveled = 0.0
        self.time = datetime.strptime('08:00 AM', '%I:%M %p')  # Start time

    # Method to load a package onto the truck and assign truck numbers.
    def load_package(self, package_id):
        self.packages.append(package_id)
        package_data = packages.lookup(package_id)
        package_data['truck_number'] = self.truck_id

    # Method to deliver a package and update its status and delivery time.
    def deliver_package(self, package_id, delivery_time):
        self.packages.remove(package_id)
        package_data = packages.lookup(package_id)
        package_data['status'] = 'delivered'
        package_data['delivery_time'] = delivery_time

    # Method to move the truck to a new location, updating mileage and time.
    def travel_to(self, destination, distance):
        self.miles_traveled += distance
        travel_time = timedelta(hours=(distance / 18))  # Calculate travel time based on speed
        self.time += travel_time
        self.current_location = destination

    # Method to provide a status summary of the truck.
    def get_status(self):
        return f"Truck {self.truck_id}: {len(self.packages)} packages, {self.miles_traveled:.2f} miles traveled, current time: {self.time.strftime('%I:%M %p')}"

# Function to find the nearest location based on distances from the current location.
def get_nearest_location(current_location, remaining_locations, distances):
    nearest_location = None
    shortest_distance = float('inf')

    # Check remaining locations to find the closest one.
    for location in remaining_locations:
        if current_location >= len(distances) or location >= len(distances[current_location]):
            continue

        distance = distances[current_location][location]
        if distance < shortest_distance:
            shortest_distance = distance
            nearest_location = location

    return nearest_location, shortest_distance

# Function to optimize the delivery route.
def optimize_route(truck, distances, packages):
    remaining_packages = truck.packages[:]
    current_location = truck.current_location
    route = []

    # Loop through packages to find and add the nearest one to the route
    while remaining_packages:
        nearest_location = None
        shortest_distance = float('inf')
        next_package_id = None

        for pkg_id in remaining_packages:
            package_data = packages.lookup(pkg_id)
            package_address = package_data['address'].strip()

            # Find the matching address index in the address list
            destination_address_index = None
            for index, address in addresses.items():
                if package_address in address:
                    destination_address_index = index
                    break

            if destination_address_index is None:
                continue

            location, distance = get_nearest_location(current_location, [destination_address_index], distances)

            if location is not None and distance < shortest_distance:
                shortest_distance = distance
                next_package_id = pkg_id
                nearest_location = location

        if nearest_location is not None:
            route.append(next_package_id)
            remaining_packages.remove(next_package_id)
            current_location = nearest_location
        else:
            break

    truck.packages = route

# Function to simulate delivering all packages across all trucks.
def deliver_all_packages(trucks, packages, distances):
    total_miles_traveled = 0

    # Optimize route and deliver packages for each truck
    for truck in trucks:
        optimize_route(truck, distances, packages)

        while truck.packages:
            current_location = truck.current_location
            package_id = truck.packages[0]
            package_data = packages.lookup(package_id)

            package_address = package_data['address'].strip()
            destination_address_index = None
            for index, address in addresses.items():
                if package_address in address:
                    destination_address_index = index
                    break

            if destination_address_index is None:
                truck.packages.pop(0)
                continue

            nearest_location, distance = get_nearest_location(current_location, [destination_address_index], distances)

            # Check for the truck's mileage limit (140 miles)
            if total_miles_traveled + distance > 140:
                break

            truck.travel_to(nearest_location, distance)
            truck.deliver_package(package_id, truck.time.strftime('%I:%M %p'))
            total_miles_traveled += distance

# Function to create a map with markers for all package locations.
def create_map(packages):
    map_file = 'package_map.html'
    delivery_map = folium.Map(location=[40.7608, -111.8910], zoom_start=13)

    # Add markers for each package location
    for package_id, package_data in packages.all_packages():
        address = f"{package_data['address']}, {package_data['city']}, {package_data['state']} {package_data['zip']}"
        lat, lng = get_coordinates(address)
        if lat is not None and lng is not None:
            folium.Marker(
                [lat, lng],
                popup=f"Package {package_id}: {package_data['address']}"
            ).add_to(delivery_map)

    # Save the map to the HTML file
    delivery_map.save(map_file)

# Main section of the program
if __name__ == '__main__':
    # Load data files
    addresses = load_address_file('address file')
    packages = load_package_file('package file')
    distances = load_distance_file('distance file')

    # Set up trucks
    truck1 = Truck(1)
    truck2 = Truck(2)
    truck3 = Truck(3)
    trucks = [truck1, truck2, truck3]

    # Load packages onto trucks based on delivery notes and availability
    for package_id in range(1, 41):
        package_data = packages.lookup(package_id)
        if package_data:
            note = package_data['note'].lower()
            if 'truck 2' in note:
                truck2.load_package(package_id)
            elif 'truck 3' in note:
                truck3.load_package(package_id)
            else:
                if len(truck1.packages) < 16:
                    truck1.load_package(package_id)
                elif len(truck2.packages) < 16:
                    truck2.load_package(package_id)
                else:
                    truck3.load_package(package_id)

    # Generate and save the map
    create_map(packages)

    # Delivery simulation
    deliver_all_packages(trucks, packages, distances)

    # GUI launch
    run_gui(packages, trucks)
