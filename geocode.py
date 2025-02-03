import pandas as pd
import requests
import time
import logging
import tkinter as tk
import urllib.parse

# Set up logging for debugging
logging.basicConfig(level=logging.INFO)

# OpenCage API key
API_KEY = 'fa48827b4e014ce992b69e8cfe52808e'
BASE_URL = 'https://api.opencagedata.com/geocode/v1/json'


def get_coordinates(address):
    # Properly encode the address for the API request
    encoded_address = urllib.parse.quote(address)
    params = {
        'key': API_KEY,
        'q': encoded_address,
        'limit': 1
    }
    try:
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            if data['results']:
                result = data['results'][0]
                return result['geometry']['lat'], result['geometry']['lng']
            else:
                logging.warning(f"No results for address: {address}")
                return None, None
        else:
            # Log the error details for better debugging
            logging.error(f"Error {response.status_code} for address: {address}")
            logging.error(f"Response content: {response.content}")
            return None, None
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed for address: {address} with error: {e}")
        return None, None
    finally:
        time.sleep(1)  # Delay to avoid hitting rate limits; adjust if needed


def show_coordinates(address, lat, lng):
    """
    Displays the address and coordinates in a pop-up window.
    :param address: The address being looked up.
    :param lat: The latitude of the address.
    :param lng: The longitude of the address.
    """
    # Create a new Tkinter window
    root = tk.Tk()
    root.title("Coordinates")

    # Display address
    address_label = tk.Label(root, text=f"Address: {address}", font=("Helvetica", 12))
    address_label.pack(pady=10)

    # Display coordinates
    coordinates_label = tk.Label(root, text=f"Latitude: {lat}, Longitude: {lng}", font=("Helvetica", 12))
    coordinates_label.pack(pady=10)

    # Add a close button
    close_button = tk.Button(root, text="Close", command=root.destroy)
    close_button.pack(pady=10)

    root.mainloop()


data = [
    {"id": 0, "name": "Western Governors University", "address": "4001 South 700 East"},
    {"id": 1, "name": "International Peace Gardens", "address": "1060 Dalton Ave S"},
    {"id": 2, "name": "Sugar House Park", "address": "1330 2100 S"},
    {"id": 3, "name": "Taylorsville-Bennion Heritage City Gov Off", "address": "1488 4800 S"},
    {"id": 4, "name": "Salt Lake City Division of Health Services", "address": "177 W Price Ave"},
    {"id": 5, "name": "South Salt Lake Public Works", "address": "195 W Oakland Ave"},
    {"id": 6, "name": "Salt Lake City Streets and Sanitation", "address": "2010 W 500 S"},
    {"id": 7, "name": "Deker Lake", "address": "2300 Parkway Blvd"},
    {"id": 8, "name": "Salt Lake City Ottinger Hall", "address": "233 Canyon Rd"},
    {"id": 9, "name": "Columbus Library", "address": "2530 S 500 E"},
    {"id": 10, "name": "Taylorsville City Hall", "address": "2600 Taylorsville Blvd"},
    {"id": 11, "name": "South Salt Lake Police", "address": "2835 Main St"},
    {"id": 12, "name": "Council Hall", "address": "300 State St"},
    {"id": 13, "name": "Redwood Park", "address": "3060 Lester St"},
    {"id": 14, "name": "Salt Lake County Mental Health", "address": "3148 S 1100 W"},
    {"id": 15, "name": "Salt Lake County United Police Dept", "address": "3365 S 900 W"},
    {"id": 16, "name": "West Valley Prosecutor", "address": "3575 W Valley Central Station bus Loop"},
    {"id": 17, "name": "Housing Auth. of Salt Lake County", "address": "3595 Main St"},
    {"id": 18, "name": "Utah DMV Administrative Office", "address": "380 W 2880 S"},
    {"id": 19, "name": "Third District Juvenile Court", "address": "410 S State St"},
    {"id": 20, "name": "Cottonwood Regional Softball Complex", "address": "4300 S 1300 E"},
    {"id": 21, "name": "Holiday City Office", "address": "4580 S 2300 E"},
    {"id": 22, "name": "Murray City Museum", "address": "5025 State St"},
    {"id": 23, "name": "Valley Regional Softball Complex", "address": "5100 South 2700 West"},
    {"id": 24, "name": "City Center of Rock Springs", "address": "5383 South 900 East #104"},
    {"id": 25, "name": "Rice Terrace Pavilion Park", "address": "600 E 900 South"},
    {"id": 26, "name": "Wheeler Historic Farm", "address": "6351 South 900 East"},
    {"id": 27, "name": "3365 S 900 W", "address": "3365 S 900 W, Salt Lake City, UT"},
    {"id": 28, "name": "2300 Parkway Blvd", "address": "2300 Parkway Blvd, West Valley City, UT"},
    {"id": 29, "name": "410 S State St", "address": "410 S State St, Salt Lake City, UT"},
    {"id": 30, "name": "5383 South 900 East #104", "address": "5383 South 900 East #104, Murray, UT"},
    {"id": 31, "name": "1060 Dalton Ave S", "address": "1060 Dalton Ave S, Salt Lake City, UT"},
    {"id": 32, "name": "2835 Main St", "address": "2835 Main St, Salt Lake City, UT"},
    {"id": 33, "name": "1330 2100 S", "address": "1330 2100 S, Salt Lake City, UT"},
    {"id": 34, "name": "300 State St", "address": "300 State St, Salt Lake City, UT"},
    {"id": 35, "name": "410 S State St", "address": "410 S State St, Salt Lake City, UT"},
    {"id": 36, "name": "233 Canyon Rd", "address": "233 Canyon Rd, Salt Lake City, UT"},
    {"id": 37, "name": "600 E 900 South", "address": "600 E 900 South, Salt Lake City, UT"},
    {"id": 38, "name": "1488 4800 S", "address": "1488 4800 S, Salt Lake City, UT"},
    {"id": 39, "name": "3148 S 1100 W", "address": "3148 S 1100 W, Salt Lake City, UT"},
    {"id": 40, "name": "177 W Price Ave", "address": "177 W Price Ave, Salt Lake City, UT"}
]

# Convert list of dictionaries to dataframe
df = pd.DataFrame(data)

# coordinates for each address
df['latitude'], df['longitude'] = zip(*df['address'].apply(get_coordinates))

# filter out rows where coordinates are none
df_valid = df.dropna(subset=['latitude', 'longitude'])

# Save the updated dataframe to new CSV
output_file = 'locations_with_coordinates.csv'
df_valid.to_csv(output_file, index=False)

# check file creation
print(f"CSV file '{output_file}' created successfully with {len(df_valid)} entries.")
if __name__ == "__main__":
    lat, lng = get_coordinates("2530 S 500 E")
    print(f"Coordinates: {lat}, {lng}")