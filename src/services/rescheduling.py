from datetime import datetime
import requests
from src.config.base_url import BASE_URL

class ReschedulingService:
    def __init__(self, session_controller, task_controller):
        self.session_controller = session_controller
        self.task_controller = task_controller  # Add base URL

    def schedule_tasks(self, user_id):
        """Make API request to generate schedule"""
        try:
            # Prepare request data
            data = {
                "user_id": str(user_id)
            }
            
            # Make POST request to schedule generation endpoint
            response = requests.post(
                f"{BASE_URL}/schedule/generate",
                json=data
            )
            
            # Check response
            if response.status_code == 200:
                result = response.json()
                if result.get("status") == "success":
                    print(f"Schedule generated successfully for user {user_id}")
                    return True
                else:
                    print(f"Schedule generation failed: {result.get('message', 'Unknown error')}")
                    return False
            else:
                print(f"API request failed with status code: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"Error scheduling tasks: {str(e)}")
            return False