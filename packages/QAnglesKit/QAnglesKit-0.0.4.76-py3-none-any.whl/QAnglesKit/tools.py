import io
import base64
import json
import pkgutil
import matplotlib.pyplot as plt
import pandas as pd
import requests
from QAnglesKit.auth import AuthManager
import os

class qanglestools:
    _config_loaded = False
    _save_url = None

    @classmethod
    def _load_config(cls):
        """Load API URL from config.json once."""
        if not cls._config_loaded:
            config_data = pkgutil.get_data("QAnglesKit", "config.json")
            if config_data is None:
                raise FileNotFoundError("config.json not found in package.")
            
            config = json.loads(config_data.decode("utf-8"))
            cls._save_url = config["simulation_save_url"]  # Adjust key as per your config.json
            
            if not AuthManager._login_url:
                AuthManager.initialize(config["login_url"])
            
            cls._config_loaded = True

    @classmethod
    def save(cls, simulationid, data=None):
        """Store images, tables, or text using authentication."""
        cls._load_config()
        AuthManager.check_authentication()

        credentials = AuthManager.get_credentials()
        QAcustomerID = credentials.get("customer_id")
        userID = credentials.get("userid")

        if data is None or isinstance(data, plt.Figure):
            # Capture the current Matplotlib figure
            fig = data if isinstance(data, plt.Figure) else plt.gcf()
            
            temp_filename = "temp_plot.png"  # Temporary file to save the image
            fig.savefig(temp_filename, format='png', dpi=300)  # Save the figure
            
            # Read the image file and encode it in base64
            with open(temp_filename, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode("utf-8")

            # Remove the temp file after encoding
            os.remove(temp_filename)  
            
            # Close the figure to prevent overlapping issues
            plt.close(fig)  
            # Use the provided figure or the current one
            
            
            data_payload = {
                "type": "image",
                "value": base64_image
            }
        elif isinstance(data, pd.DataFrame):
            # Convert Pandas DataFrame to JSON
            data_payload = {
                "type": "table",
                "value": data.to_json()
            }
        elif isinstance(data, str):
            # Store plain text
            data_payload = {
                "type": "text",
                "value": data
            }
        else:
            # Store unknown data as JSON
            data_payload = {
                "type": "unknown",
                "value": json.dumps(data)
            }

        # Send data via authenticated API request
        try:
            session = AuthManager.get_session()
            
            data_type = data_payload["type"]  # Extract "type" from data_payload
            data_value = data_payload["value"]
            
 
           
            payload = {
                "QAcustomerID": QAcustomerID,
                "SimulationID": str(simulationid),
                "data_value": data_value,
                "data_type":data_type
            }
            
            headers = {"Content-Type": "application/json"}
            response = session.post(cls._save_url, json=payload, headers=headers)

            
            if response.status_code == 200:
                response_json = response.json()  
                return response_json.get("Details")
            print(f"Failed to save data: {response.status_code}, {response.text}")
        except requests.RequestException as e:
            print(f"Error saving data: {e}")

        return None
