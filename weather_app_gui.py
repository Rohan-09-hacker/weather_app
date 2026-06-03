import tkinter as tk
from tkinter import messagebox
# Import the functions we built yesterday from your backend file
from weather_backend import get_user_location, get_weather_data

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pinnacle Weather Forecast")
        self.root.geometry("450x550")
        self.root.configure(bg="#1e1e2e")  # Modern dark theme background
        self.root.resizable(False, False)

        # --- Title Banner ---
        self.title_label = tk.Label(
            root, 
            text="⚡ SKYCAST WEATHER", 
            font=("Helvetica", 18, "bold"), 
            fg="#cdd6f4", 
            bg="#1e1e2e"
        )
        self.title_label.pack(pady=20)

        # --- Search Frame ---
        self.search_frame = tk.Frame(root, bg="#1e1e2e")
        self.search_frame.pack(pady=10)

        self.city_entry = tk.Entry(
            self.search_frame, 
            font=("Helvetica", 14), 
            width=18, 
            bd=0, 
            highlightthickness=1,
            highlightbackground="#45475a",
            bg="#313244",
            fg="#cdd6f4",
            insertbackground="#cdd6f4"
        )
        self.city_entry.grid(row=0, column=0, padx=10, ipady=4)
        self.city_entry.insert(0, "Enter city name...")
        self.city_entry.bind("<FocusIn>", self.clear_placeholder)

        self.search_button = tk.Button(
            self.search_frame, 
            text="Search", 
            font=("Helvetica", 11, "bold"),
            bg="#89b4fa", 
            fg="#11111b",
            activebackground="#b4befe",
            bd=0,
            command=self.fetch_manual_weather
        )
        self.search_button.grid(row=0, column=1, padx=5, ipady=4, ipadx=10)

        # --- Weather Display Card ---
        self.card = tk.Frame(root, bg="#313244", bd=0)
        self.card.pack(pady=25, padx=30, fill="both", expand=True)

        self.city_label = tk.Label(self.card, text="📍 Detecting Location...", font=("Helvetica", 18, "bold"), fg="#89b4fa", bg="#313244")
        self.city_label.pack(pady=(25, 5))

        self.temp_label = tk.Label(self.card, text="--°C", font=("Helvetica", 50, "bold"), fg="#a6e3a1", bg="#313244")
        self.temp_label.pack(pady=10)

        self.desc_label = tk.Label(self.card, text="Condition: --", font=("Helvetica", 13, "italic"), fg="#cdd6f4", bg="#313244")
        self.desc_label.pack(pady=5)

        self.humidity_label = tk.Label(self.card, text="Humidity: --%", font=("Helvetica", 12), fg="#bac2de", bg="#313244")
        self.humidity_label.pack(pady=5)

        # --- Auto-Load Local Weather on Startup ---
        self.load_auto_location()

    def clear_placeholder(self, event):
        if self.city_entry.get() == "Enter city name...":
            self.city_entry.delete(0, tk.END)

    def update_ui(self, weather_data):
        """Populates the GUI cards with fresh data dictionary."""
        if weather_data:
            self.city_label.config(text=f"📍 {weather_data['city']}")
            self.temp_label.config(text=f"{int(weather_data['temperature'])}°C")
            self.desc_label.config(text=f"{weather_data['description']}")
            self.humidity_label.config(text=f"💧 Humidity: {weather_data['humidity']}%")
        else:
            messagebox.showerror("Error", "City not found or API issue. Please try again.")

    def load_auto_location(self):
        """Triggers the IP location lookup and fetches weather automatically."""
        city = get_user_location()
        weather = get_weather_data(city)
        if weather:
            self.update_ui(weather)
        else:
            self.city_label.config(text="📍 Bangalore")
            # Fallback loading if initial IP check stumbles
            weather = get_weather_data("Bangalore")
            self.update_ui(weather)

    def fetch_manual_weather(self):
        """Runs when the user types a city name and clicks search."""
        city = self.city_entry.get().strip()
        if city and city != "Enter city name...":
            weather = get_weather_data(city)
            self.update_ui(weather)
        else:
            messagebox.showwarning("Warning", "Please enter a valid city name first!")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()