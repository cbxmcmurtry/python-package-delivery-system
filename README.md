# Package Delivery System
## Overview
The Package Delivery System is a Python-based application designed to simulate and manage package deliveries using multiple trucks. The system optimizes delivery routes, tracks package statuses, and visualizes delivery locations on an interactive map. This project demonstrates a variety of programming concepts, including data structures, GUI development, API integration, and geolocation mapping.

### Features
* **Package Tracking:** Allows users to view the status and details of each package, including its location, delivery time, and assigned truck.
* **Route Optimization:** Utilizes distance calculations to find the most efficient route for each truck to minimize travel time and mileage.
* **Geolocation Mapping:** Integrates the OpenCage Geocoding API to fetch coordinates for addresses and displays them on an interactive map using Leaflet and Folium.
* **GUI Interface:** Built using Tkinter, the graphical interface provides an intuitive way for users to look up packages, filter by status, and see map visualizations.

### Technologies Used
* **Python:** Core programming language for developing the system.
* **Tkinter:** GUI toolkit used for creating the user interface.
* **OpenCage Geocoding API:** For retrieving latitude and longitude coordinates based on package addresses.
* **Folium & Leaflet:** For generating and displaying the interactive map.
* **Data Structures:** Custom hash table implementation for storing and managing package data.

### Project Structure
* **main.py:** The main file that loads data, initializes trucks, optimizes routes, and launches the GUI interface.
* **geocode.py:** Handles API requests to fetch geographical coordinates for package addresses.
* **gui_interface.py:** Defines the graphical interface for interacting with the package delivery system.
* **data_structures.py:** Implements the hash table used to store package data efficiently.
* **distance file, address file, package file:** Data files used to load package, address, and distance information.
