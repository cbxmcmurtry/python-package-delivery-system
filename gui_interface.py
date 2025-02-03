import tkinter as tk
from tkinter import ttk
import webbrowser


class PackageDeliveryApp(tk.Tk):
    def __init__(self, packages, trucks):
        super().__init__()
        self.title("Package Delivery System")
        self.geometry("1200x800")  # Adjust window size

        self.packages = packages
        self.trucks = trucks

        # Add See Map button
        self.map_button = ttk.Button(self, text="See Map", command=self.open_map)
        self.map_button.grid(row=4, column=0, columnspan=5, padx=10, pady=10)

        # Grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        # Package ID lookup
        self.label = ttk.Label(self, text="Enter Package ID:")
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.package_id_entry = ttk.Entry(self)
        self.package_id_entry.grid(row=0, column=1, padx=10, pady=10)

        self.lookup_button = ttk.Button(self, text="Lookup Package", command=self.lookup_package)
        self.lookup_button.grid(row=0, column=2, padx=10, pady=10)

        # Filter packages by status
        self.status_filter = ttk.Combobox(self, values=["All", "At Hub", "In Transit", "Delivered"])
        self.status_filter.set("All")
        self.status_filter.grid(row=0, column=3, padx=10, pady=10)
        self.status_filter.bind("<<ComboboxSelected>>", self.filter_packages)

        # Display all packages button
        self.all_packages_button = ttk.Button(self, text="Display All Packages", command=self.display_all_packages)
        self.all_packages_button.grid(row=0, column=4, padx=10, pady=10)

        # Summary panel
        self.summary_frame = ttk.Frame(self)
        self.summary_frame.grid(row=1, column=0, columnspan=5, padx=10, pady=10, sticky="ew")
        self.total_delivered_label = ttk.Label(self.summary_frame, text="Total Delivered: 0")
        self.total_delivered_label.grid(row=0, column=0, padx=10)
        self.total_miles_label = ttk.Label(self.summary_frame, text="Total Miles Traveled: 0.0")
        self.total_miles_label.grid(row=0, column=1, padx=10)

        # Result label for lookup results
        self.result_label = ttk.Label(self, text="", wraplength=800)
        self.result_label.grid(row=2, column=0, columnspan=5, padx=10, pady=10)

        # Treeview
        self.tree = ttk.Treeview(self, columns=("ID", "Address", "City", "State", "ZIP", "Deadline",
                                                "Weight", "Status", "Truck", "Delivery Time"), show='headings', height=15)
        self.tree.heading("ID", text="Package ID")
        self.tree.heading("Address", text="Address")
        self.tree.heading("City", text="City")
        self.tree.heading("State", text="State")
        self.tree.heading("ZIP", text="ZIP")
        self.tree.heading("Deadline", text="Deadline")
        self.tree.heading("Weight", text="Weight")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Truck", text="Truck Number")
        self.tree.heading("Delivery Time", text="Delivery Time")

        # Column configurations
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Address", width=200, anchor="w")
        self.tree.column("City", width=120, anchor="center")
        self.tree.column("State", width=50, anchor="center")
        self.tree.column("ZIP", width=60, anchor="center")
        self.tree.column("Deadline", width=100, anchor="center")
        self.tree.column("Weight", width=80, anchor="center")
        self.tree.column("Status", width=100, anchor="center")
        self.tree.column("Truck", width=80, anchor="center")
        self.tree.column("Delivery Time", width=100, anchor="center")

        self.tree.grid(row=3, column=0, columnspan=5, padx=10, pady=10, sticky='nsew')

        # Set up and display all packages and summary
        self.update_summary()
        self.display_all_packages()

    def lookup_package(self):
        package_id = self.package_id_entry.get().strip()
        if package_id.isdigit():
            package_data = self.packages.lookup(int(package_id))
            if package_data:
                result_text = (
                    f"Package {package_id} found:\n"
                    f"Address: {package_data['address']}\n"
                    f"City: {package_data['city']}\n"
                    f"State: {package_data['state']}\n"
                    f"ZIP: {package_data['zip']}\n"
                    f"Deadline: {package_data['deadline']}\n"
                    f"Weight: {package_data['weight']}\n"
                    f"Status: {package_data['status']}\n"
                    f"Delivery Time: {package_data['delivery_time']}\n"
                    f"Truck Number: {package_data['truck_number']}\n"
                )
                self.result_label.config(text=result_text)
                # Call show_coordinates function with the retrieved address and coordinates
                # show_coordinates(package_data['address'], lat, lng)
            else:
                self.result_label.config(text="Package not found.")
        else:
            self.result_label.config(text="Please enter a valid package ID.")

    def display_all_packages(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for package_id, package_data in self.packages.all_packages():
            self.tree.insert("", "end", values=(
                package_id, package_data['address'], package_data['city'], package_data['state'],
                package_data['zip'], package_data['deadline'], package_data['weight'],
                package_data['status'], package_data['truck_number'], package_data['delivery_time']
            ))

    def filter_packages(self, event=None):
        selected_status = self.status_filter.get()
        for item in self.tree.get_children():
            self.tree.delete(item)
        for package_id, package_data in self.packages.all_packages():
            if selected_status == "All" or package_data['status'].lower() == selected_status.lower():
                self.tree.insert("", "end", values=(
                    package_id, package_data['address'], package_data['city'], package_data['state'],
                    package_data['zip'], package_data['deadline'], package_data['weight'],
                    package_data['status'], package_data['truck_number'], package_data['delivery_time']
                ))

    def update_summary(self):
        total_delivered = len([pkg for pkg_id, pkg in self.packages.all_packages() if pkg['status'].lower() == 'delivered'])
        total_miles = sum(truck.miles_traveled for truck in self.trucks)
        self.total_delivered_label.config(text=f"Total Delivered: {total_delivered}")
        self.total_miles_label.config(text=f"Total Miles Traveled: {total_miles:.2f} miles")

    def open_map(self):
        map_file = 'package_map.html'
        try:
            webbrowser.open(map_file)
        except Exception as e:
            self.result_label.config(text=f"Error opening map: {str(e)}")


def show_coordinates(address, lat, lng):
    root = tk.Tk()
    root.title("Coordinates")
    address_label = tk.Label(root, text=f"Address: {address}", font=("Helvetica", 12))
    address_label.pack(pady=10)
    coordinates_label = tk.Label(root, text=f"Latitude: {lat}, Longitude: {lng}", font=("Helvetica", 12))
    coordinates_label.pack(pady=10)
    close_button = tk.Button(root, text="Close", command=root.destroy)
    close_button.pack(pady=10)
    root.mainloop()


def run_gui(packages, trucks):
    app = PackageDeliveryApp(packages, trucks)
    app.mainloop()
