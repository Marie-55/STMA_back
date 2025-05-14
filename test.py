import requests
import json

def debug_api_call():
    try:
        response = requests.get('https://stma-back.onrender.com/api/stats/123')
        
        # Print raw response details
        print("Status Code:", response.status_code)
        print("Response Headers:", response.headers)
        print("Raw Response:", response.text)
        
        # Try parsing JSON only if we have content
        if response.text.strip():
            return response.json()
        else:
            print("Empty response received")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {str(e)}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON parsing failed: {str(e)}")
        print(f"Response content: {response.text}")
        return None

# Test the API call
result = debug_api_call()
print("Parsed result:", result)
