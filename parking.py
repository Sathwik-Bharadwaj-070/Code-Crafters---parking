import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class ParkingSpot:
    def __init__(self, spot_id):
        self.spot_id = spot_id
        self.is_available = True
        self.is_booked = False
        self.license_plate = ""

    def occupy(self, license_plate):
        self.is_available = False
        self.is_booked = True
        self.license_plate = license_plate

    def vacate(self):
        self.is_available = True
        self.is_booked = False
        self.license_plate = ""

    def get_vehicle_details(self):
        if self.is_booked:
            return f"Slot ID: {self.spot_id}\nLicense Plate: {self.license_plate}"
        else:
            return "This slot is currently vacant."

class ParkingLot:
    def __init__(self, num_spots):
        self.spots = [ParkingSpot(i) for i in range(1, num_spots+1)]

    def check_availability(self):
        available_spots = [spot.spot_id for spot in self.spots if spot.is_available and not spot.is_booked]
        return available_spots

    def park_vehicle(self, license_plate, vehicle_type):
        available_spots = self.check_availability()
        if available_spots:
            spot_id = available_spots[0]
            self.spots[spot_id - 1].occupy(license_plate)
            messagebox.showinfo("Success", f"Vehicle parked successfully at spot {spot_id}")
        else:
            messagebox.showerror("Error", "No available spots. Parking lot is full.")

    def release_spot(self, spot_id):
        self.spots[spot_id - 1].vacate()
        messagebox.showinfo("Success", f"Spot {spot_id} released successfully.")

    def find_vehicle(self, license_plate):
        for spot in self.spots:
            if spot.license_plate == license_plate:
                return f"Vehicle with license plate {license_plate} is parked at spot {spot.spot_id}."
        return f"No vehicle with license plate {license_plate} found in the parking lot."

class ParkingApp:
    def __init__(self, master):
        self.master = master
        self.parking_lot = ParkingLot(60)

        self.master.title("Park-o-Tron")

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.label = ttk.Label(master, text="Park-o-Tron", font=("Work Sans", 28))
        self.label.pack(pady=10)

        self.button_frame = ttk.Frame(master)
        self.button_frame.pack(pady=10)

        self.check_button = ttk.Button(self.button_frame, text="Check Availability", command=self.check_availability)
        self.check_button.pack(side=tk.LEFT, padx=5)

        self.park_button = ttk.Button(self.button_frame, text="Park Vehicle", command=self.park_vehicle)
        self.park_button.pack(side=tk.LEFT, padx=5)

        self.release_frame = ttk.Frame(master)
        self.release_frame.pack(pady=10)

        self.release_slot_entry = ttk.Entry(self.release_frame)
        self.release_slot_entry.pack(side=tk.LEFT, padx=5)

        self.release_slot_button = ttk.Button(self.release_frame, text="Release Specific Slot", command=self.release_specific_slot)
        self.release_slot_button.pack(side=tk.LEFT, padx=5)

        self.search_frame = ttk.Frame(master)
        self.search_frame.pack(pady=10)

        self.search_label = ttk.Label(self.search_frame, text="Search Vehicle by License Plate:")
        self.search_label.pack(side=tk.LEFT, padx=5)

        self.search_entry = ttk.Entry(self.search_frame)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        self.search_button = ttk.Button(self.search_frame, text="Search", command=self.search_vehicle)
        self.search_button.pack(side=tk.LEFT, padx=5)

        self.available_spots_text = tk.Text(master, height=7, width=40)
        self.available_spots_text.pack(pady=10)

        # Center the window
        self.center_window()

    def check_availability(self):
        available_spots = self.parking_lot.check_availability()
        if available_spots:
            self.available_spots_text.delete('1.0', tk.END)
            self.available_spots_text.insert(tk.END, f"Available spots: {available_spots}")
        else:
            self.available_spots_text.delete('1.0', tk.END)
            self.available_spots_text.insert(tk.END, "No available spots.")

    def park_vehicle(self):
        license_plate = simpledialog.askstring("License Plate", "Enter license plate number:")
        if not license_plate:
            messagebox.showerror("Error", "License plate number cannot be left blank.")
            return

        self.parking_lot.park_vehicle(license_plate, "")

    def release_specific_slot(self):
        spot_id = self.release_slot_entry.get()
        if not spot_id.isdigit():
            messagebox.showerror("Error", "Please enter a valid spot ID.")
            return
        spot_id = int(spot_id)
        if spot_id < 1 or spot_id > 60:
            messagebox.showerror("Error", "Please enter a spot ID between 1 and 60.")
            return

        self.parking_lot.release_spot(spot_id)

    def search_vehicle(self):
        license_plate = self.search_entry.get()
        if not license_plate:
            messagebox.showerror("Error", "Please enter a license plate number to search.")
            return

        result = self.parking_lot.find_vehicle(license_plate)
        messagebox.showinfo("Search Result", result)

    def center_window(self):
        width = self.master.winfo_reqwidth()
        height = self.master.winfo_reqheight()
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.master.geometry(f"+{x}+{y}")

def main():
    root = tk.Tk()
    app = ParkingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
