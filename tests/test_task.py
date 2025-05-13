import requests

BASE_URL = "http://127.0.0.1:5000/api/tasks"
task= {
        "category": "Study ",
        "title":"Security project",
        "deadline": "2025-04-01",  #how the date should be entered--> will be converted to a datetime format when task is created (model)
        "duration": 5,
        "is_scheduled": False, #are flase by default but just for the sake of demo :)
        "is_synched": False,
        "priority": "High",
        "to_reschedule": False,
        "status":"Done"
}

def test_create_task(t):
    response = requests.post(f"{BASE_URL}/write/add", json=t)
    print(f"Response: {response.status_code}, {response.text}")
    return response

def test_get_task():
    response = requests.get(f"{BASE_URL}/read/all")
    print(f"Response: {response.status_code}, {response.text}")
    return response

def test_update_task(id,status):
    response = requests.patch(json=f"{BASE_URL}/update/status/{id}/{status}",url=f"{BASE_URL}/update/status/{id}/{status}")
    print(f"Response: {response.status_code}, {response.text}")
    return response

def test_delete_task(id):
    response = requests.delete(json=f"{BASE_URL}/delete/{id}",url=f"{BASE_URL}/delete/{id}",)
    print(f"Response: {response.status_code}, {response.text}")
    return response

if __name__ == "__main__":
    #r_task= test_create_task(task)
    #r_task= test_get_task()
    #r_task= test_update_task(1,"In progress")
    r_task= test_delete_task(3)
    print(r_task)
