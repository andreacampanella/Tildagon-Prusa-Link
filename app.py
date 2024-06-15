import app
import requests
from events.input import Buttons, BUTTON_TYPES

class Prusa_Link(app.App):
    def __init__(self):
        # Initialize button states
        self.button_states = Buttons(self)
        self.api_key = "WMzXwaZ7eMbrdQ4"
        self.api_url = "http://192.168.0.204:80/api/job"
        self.data = None
        print("App initialized")

    def update(self, delta):
        # Check if the CANCEL button is pressed to minimize the app
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            print("CANCEL button pressed")
            self.button_states.clear()
            self.minimise()
        
        # Fetch data from API
        self.fetch_data()

    def fetch_data(self):
        print("Fetching data from API")
        try:
            headers = {"X-Api-Key": self.api_key}
            response = requests.get(self.api_url, headers=headers)
            print(f"HTTP Response Status Code: {response.status_code}")
            if response.status_code == 200:
                self.data = response.json()
                print("Data fetched successfully:", self.data)
            else:
                self.data = {"error": "Failed to fetch data"}
                print("Failed to fetch data")
        except Exception as e:
            self.data = {"error": str(e)}
            print("Exception occurred while fetching data:", e)

    def draw(self, ctx):
        print("Drawing on canvas")
        ctx.save()
        # Fill the background with black color
        ctx.rgb(0, 0, 0).rectangle(-120, -120, 240, 240).fill()
        ctx.rgb(0, 1, 0)
        
        if self.data:
            print("Data available for drawing")
            if "error" in self.data:
                print("Error in data:", self.data['error'])
                ctx.move_to(-100, 0).text(f"Error: {self.data['error']}")
            else:
                state = self.data.get("state", "Unknown")
                job_info = self.data.get("job") or {}
                progress_info = self.data.get("progress") or {}
                
                job_file = job_info.get("file") or {}
                job_name = job_file.get("name", "Unknown")
                estimated_time = job_info.get("estimatedPrintTime", "N/A")
                print_time_left = progress_info.get("printTimeLeft", "N/A")
                completion = progress_info.get("completion", 0)
                
                print(f"State: {state}, Job: {job_name}, Estimated Time: {estimated_time}, Time Left: {print_time_left}, Completion: {completion}%")
                
                ctx.move_to(-100, 40).text(f"State: {state}")
                ctx.move_to(-100, 20).text(f"Job: {job_name}")
                ctx.move_to(-100, 0).text(f"Est. Time: {estimated_time} sec")
                ctx.move_to(-100, -20).text(f"Time Left: {print_time_left} sec")
                ctx.move_to(-100, -40).text(f"Completion: {completion}%")
        else:
            print("No data available, showing fetching message")
            ctx.move_to(-100, 0).text("Fetching data...")

        ctx.restore()

__app_export__ = Prusa_Link
