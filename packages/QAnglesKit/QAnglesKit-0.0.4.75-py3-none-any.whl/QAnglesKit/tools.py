import io
import base64
import json
import pkgutil
import matplotlib.pyplot as plt
import pandas as pd
import requests
from QAnglesKit.auth import AuthManager

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

        if data is None:
            # Capture the current Matplotlib figure
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            base64_image = base64.b64encode(buf.read()).decode("utf-8")

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
            print("00")
            data_type = data_payload["type"]  # Extract "type" from data_payload
            data_value = data_payload["value"]
            print("Simulation ID Type Before:", type(simulationid), "Value:", simulationid)
            simulationid = str(simulationid)
            print("Simulation ID Type After:", type(simulationid), "Value:", simulationid)
 
           
            payload = {
                "QAcustomerID": QAcustomerID,
                "SimulationID": str(simulationid),
                "data_value": data_value,
                "data_type":data_type
            }
            print("555",payload)
            headers = {"Content-Type": "application/json"}
            response = session.post(cls._save_url, json=payload, headers=headers)

            print("11")
            if response.status_code == 200:
                response_json = response.json() 
                print("Response JSON:", json.dumps(response_json, indent=4))
                print("112",response_json.get("Details")) 
                return response_json.get("Details")
            print(f"Failed to save data: {response.status_code}, {response.text}")
        except requests.RequestException as e:
            print(f"Error saving data: {e}")

        return None
